"""Locate native tools on Windows, macOS and Linux without installing system packages."""
import os
import platform
import shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def find_tool(name,required=True):
    if name not in {'ffmpeg','ffprobe'}:raise ValueError(f'Unsupported runtime tool: {name}')
    windows=platform.system()=='Windows'
    local=ROOT/'tools/bin'/(name+'.exe' if windows else name)
    if local.is_file() and (windows or os.access(local,os.X_OK)):return str(local)
    found=shutil.which(name)
    if found:return found
    if required:
        raise FileNotFoundError(f'{name} is missing. Put a compatible executable under tools/bin or on PATH; see docs/SETUP.md.')
    return None
