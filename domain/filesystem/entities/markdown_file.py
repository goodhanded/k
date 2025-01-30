from .file import File
from ..enums.ext import Ext

class MarkdownFile(File):
    
    @classmethod
    def required_extensions(cls):
        return [Ext.MD, Ext.MARKDOWN]