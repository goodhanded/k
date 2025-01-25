from domain.notes import NoteCollection


from typing import Protocol


class NoteAssimilatorInterface(Protocol):
  def assimilate(self, todays_notes: NoteCollection):
    pass