from .file import File
from ..enums.ext import Ext

class AudioFile(File):
    """
    Represents an audio file in the filesystem.

    Required extensions: mp3, wav, flac, aac
    """

    @classmethod
    def required_extensions(cls):
        """
        Returns a list of required file extensions
        """
        return [Ext.MP3, Ext.WAV, Ext.FLAC, Ext.AAC]