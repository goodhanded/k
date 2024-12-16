#!.env/bin/python3

import sys, os
from application.use_cases import TranscribeVoiceMemoUseCase, AssimilateTodaysNotesIntoVault
from domain.notes import VoiceMemo
from infrastructure.transcribers import AmazonTranscribe
from infrastructure.obsidian import ObsidianVault
from infrastructure.openai import Client as OpenAI
from infrastructure.note_assimilator import NoteAssimilator
from domain.config import Config
from domain.datetime import ymd
from domain.notes import NoteCollection
from adapters.prompts.transcripts import assimilation_prompt

if __name__ == "__main__":

  if len(sys.argv) < 2:
    print("Usage: assimilate_voice_memo.py <local_audio_file>")
    sys.exit(1)

  config = Config()
  openai = OpenAI(config.get("openai","api_key"))
  obsidian_vault = ObsidianVault(config.get("obsidian", "vault_path"))
  transcript_base_path = config.get("transcripts", "base_path")
  todays_transcripts_dir = os.path.join(transcript_base_path, *ymd())
  amazon_transcribe = AmazonTranscribe(config.get("transcripts","voice_memo_bucket"), config.get("aws","path"))
  transcribe = TranscribeVoiceMemoUseCase(transcription_service = amazon_transcribe).execute

  # Transcribe the voice memo
  os.makedirs(todays_transcripts_dir, exist_ok=True)
  voice_memo = VoiceMemo(sys.argv[1])
  current_transcript = transcribe(voice_memo)
  transcript_note_name = f"{voice_memo.name_without_extension}.md"
  transcript_path = os.path.join(todays_transcripts_dir, transcript_note_name)
  current_transcript.to_file(transcript_path)

  # Assimilate all of today's voice memo transcripts into the daily note
  todays_transcripts = NoteCollection.from_path(todays_transcripts_dir)
  assimilator = NoteAssimilator(openai)
  assimilate = AssimilateTodaysNotesIntoVault(assimilator).execute
  assimilate(todays_transcripts, obsidian_vault)
  print(f"Assimilated {len(todays_transcripts)} notes into today's daily note")