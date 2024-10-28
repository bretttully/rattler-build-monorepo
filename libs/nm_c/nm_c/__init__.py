from importlib.metadata import version
from pathlib import Path

__version__ = version(Path(__file__).parent.name)
