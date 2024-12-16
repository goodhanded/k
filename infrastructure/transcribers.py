import time
import boto3
import requests
import subprocess
from datetime import datetime
from domain.protocols import TranscriptionServiceInterface
from domain.notes import Note

class AmazonTranscribe (TranscriptionServiceInterface):

  def __init__(self, bucket_name="goodhanded-voice-transcription", aws_path="/usr/local/bin/aws"):
    self.bucket_name = bucket_name
    self.aws_path = aws_path
    self.ensure_aws_credentials()

  """
  Ensures that the user has valid AWS credentials
  """
  def ensure_aws_credentials(self):
    try:
      subprocess.run([self.aws_path, "sts", "get-caller-identity"], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError:
      login_result = subprocess.run([self.aws_path, "sso", "login"], check=True)
      if login_result.returncode != 0:
        raise RuntimeError("AWS SSO Login failed. Cannot proceed without valid credentials.")

  """
  Transcribes a voice memo file using Amazon Transcribe
  """
  def transcribe(self, voice_memo) -> Note:

    print(f"Transcribing voice memo: {voice_memo.path}")

    self.upload_to_s3(voice_memo.path, self.bucket_name, voice_memo.name)
    
    s3_uri = f"s3://{self.bucket_name}/{voice_memo.name}"
    job_name = f"transcription_job_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    start_response = self.start_transcribe_job(job_name, s3_uri)

    if start_response['ResponseMetadata']['HTTPStatusCode'] != 200:
      raise Exception("Transcription job failed to start")

    status, transcript_file_uri = self.wait_for_transcription(job_name)

    if status == 'COMPLETED':
      transcription = self.get_transcription_text(transcript_file_uri)
      # Extract formatted date and time from the voice memo file name
      # file name format: daily_note_20241215_065752.wav
      date_string = voice_memo.name_without_extension.split('_')[2]
      time_string = voice_memo.name_without_extension.split('_')[3]
      date_time = datetime.strptime(f"{date_string}_{time_string}", '%Y%m%d_%H%M%S')
      date_time_formatted = date_time.strftime('%A, %B %d, %Y %I:%M %p')
      return Note(f"Transcription Recorded: {date_time_formatted}\n\n{transcription}")
    else:
      raise Exception("Transcription job failed")    

  """
  Uploads a file to an S3 bucket
  """
  def upload_to_s3(self, local_file, bucket_name, s3_key):
    s3 = boto3.client('s3')
    s3.upload_file(local_file, bucket_name, s3_key)

  """
  Starts a transcription job
  """
  def start_transcribe_job(self, job_name, s3_uri, media_format='wav', language_code='en-US'):
    transcribe = boto3.client('transcribe')
    response = transcribe.start_transcription_job(
      TranscriptionJobName=job_name,
      Media={'MediaFileUri': s3_uri},
      MediaFormat=media_format,
      LanguageCode=language_code
    )
    return response

  """
  Waits for a transcription job to complete
  """
  def wait_for_transcription(self, job_name):
    transcribe = boto3.client('transcribe')
    timeout = time.time() + 60*60 # 1 hour

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

  """
  Retrieves the text of a transcription
  """
  def get_transcription_text(self, transcript_uri):
    r = requests.get(transcript_uri)
    result = r.json()
    text = result['results']['transcripts'][0]['transcript']
    return text
