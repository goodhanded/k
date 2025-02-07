import time
import boto3
import requests
import subprocess
from datetime import datetime

from application.transcription import TranscriberProtocol
from domain.filesystem import Document, AudioFile


class AmazonTranscribe(TranscriberProtocol):

    def __init__(self, bucket_name: str, aws_path: str):
        self.bucket_name = bucket_name
        self.aws_path = aws_path
        self.ensure_aws_credentials()

    def ensure_aws_credentials(self):
        """
        Ensures that the user has valid AWS credentials
        """
        try:
            subprocess.run([self.aws_path, "sts", "get-caller-identity"], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError:
            login_result = subprocess.run([self.aws_path, "sso", "login"], check=True)
            if login_result.returncode != 0:
                raise RuntimeError("AWS SSO Login failed. Cannot proceed without valid credentials.")

    def transcribe(self, audio_file: AudioFile) -> Document:
        """
        Transcribes a voice memo file using Amazon Transcribe
        """

        print(f"Transcribing voice memo: {audio_file.path}")

        self.upload_to_s3(audio_file.path, self.bucket_name, audio_file.name)
        
        s3_uri = f"s3://{self.bucket_name}/{audio_file.name}"
        job_name = f"transcription_job_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        start_response = self.start_transcribe_job(job_name, s3_uri)

        if start_response['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise Exception("Transcription job failed to start")

        status, transcript_file_uri = self.wait_for_transcription(job_name)

        if status == 'COMPLETED':
            transcription = self.get_transcription_text(transcript_file_uri)
            # Extract formatted date and time from the voice memo file name
            # file name format: daily_note_20241215_065752.wav
            date_string = audio_file.name_without_extension.split('_')[2]
            time_string = audio_file.name_without_extension.split('_')[3]
            date_time = datetime.strptime(f"{date_string}_{time_string}", '%Y%m%d_%H%M%S')
            date_time_formatted = date_time.strftime('%A, %B %d, %Y %I:%M %p')
            return Document(f"Transcription Recorded: {date_time_formatted}\n\n{transcription}")
        else:
            raise Exception("Transcription job failed")

    def upload_to_s3(self, local_file, bucket_name, s3_key):
        s3 = boto3.client('s3')
        s3.upload_file(local_file, bucket_name, s3_key)

    def start_transcribe_job(self, job_name, s3_uri, media_format='wav', language_code='en-US'):
        transcribe = boto3.client('transcribe')
        response = transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': s3_uri},
            MediaFormat=media_format,
            LanguageCode=language_code
        )
        return response

    def wait_for_transcription(self, job_name):
        transcribe = boto3.client('transcribe')
        timeout = time.time() + 60*60  # 1 hour

        while True:
            if time.time() > timeout:
                raise TimeoutError("Transcription job timed out")

            response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
            status = response['TranscriptionJob']['TranscriptionJobStatus']

            if status == 'COMPLETED':
                uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
                return (status, uri)
            elif status == 'FAILED':
                raise Exception("Transcription job failed")

            time.sleep(5)

    def get_transcription_text(self, transcript_uri):
        r = requests.get(transcript_uri)
        result = r.json()
        text = result['results']['transcripts'][0]['transcript']
        return text
