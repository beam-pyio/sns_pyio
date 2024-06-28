# read version from installed package
from importlib.metadata import version
__version__ = version("sns_pyio")

from .snsio import SnsUploader

__all__ = [
    'SnsUploader',
    'SNSOptions'
]