from typing import Optional
from domain.notes import Note, NoteCollection

def assimilation_prompt(todays_transcript_content: str, daily_note_content: str) -> str:

  existing_content_section = f"""
There is no existing daily note content for today.
"""
  if daily_note_content.strip() != '':
    existing_content_section = f"""
Here is the existing daily note content for today:
===
{daily_note_content}
==="""

  prompt = f"""
You are an assistant who helps aggregate notes and transcripts for a user's personal knowledge management system.

{existing_content_section}

**Transcripts for Today:**

{todays_transcript_content}

**************************

Please use the information above to create a daily note for today, combining the content from the transcripts with any 
existing content in the daily note.

**Output Format Requirements:**

Return your answer as **only** a YAML formatted bulleted list containing the aggregated daily note content. Preserve
existing ideas from the daily note, but do not duplicate bullets even if there is duplication in the provided updates.

Example Format:

- Met with Mike
	- Expectations for my role
		- Kinsey is final word on my role
		- What's in scope?
		- What's not in scope?
	- Meeting next week
		- What is your impression of what we're doing/delivering next week in [[Denver]]?
	- Tech Stack -> Can we finalize this?
		- UI -> [[NextJs]]
		- APIs -> [[NodeJs]]
		- C++ 24 for mission critical
	- [[Budget Estimation]] -> 
		- How have you done this in the past? 
		- How much detail is required?
- Met with Tony
	- Talked about stuff
"""
  return prompt