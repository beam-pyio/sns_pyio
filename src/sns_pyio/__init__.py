# read version from installed package
from importlib.metadata import version
__version__ = version("sns_pyio")

from .options import SNSOptions
from .snsio import SnsUploader, SnsClient, IOStatus

__all__ = [
    'SnsUploader',
    'SNSOptions',
    'SnsClient',
    'IOStatus'
]

