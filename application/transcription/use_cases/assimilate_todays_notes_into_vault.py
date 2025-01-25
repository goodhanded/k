from application.intelligence import NoteVaultInterface
from domain.notes import NoteCollection
from application.intelligence import NoteAssimilatorInterface

class AssimilateTodaysNotesIntoVault:
  def __init__(self,
               assimilator: NoteAssimilatorInterface):
    self.assimilator = assimilator

  def execute(self, notes: NoteCollection, vault: NoteVaultInterface):
    return self.assimilator.assimilate(notes, vault)