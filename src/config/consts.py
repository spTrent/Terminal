import os
import shutil
from typing import Callable

from src.utilities import (
    archivers,
    cat,
    cd,
    cp,
    grep,
    history,
    ls,
    mkdir,
    mv,
    rm,
    touch,
    undo,
)

FOR_UNDO_HISTORY: list[list] = []
HISTORY_PATH: str = os.path.join(os.getcwd(), 'src/.history')
TRASH_PATH: str = os.path.join(os.getcwd(), 'src/.trash')
if os.path.exists(TRASH_PATH):
    shutil.rmtree(TRASH_PATH)
os.mkdir(TRASH_PATH)

UTILITIES: dict[str, Callable] = {
    'ls': ls.ls,
    'cd': cd.cd,
    'cat': cat.cat,
    'cp': cp.cp,
    'mv': mv.mv,
    'rm': rm.rm,
    'history': history.history,
    'undo': undo.undo,
    'zip': archivers.make_archive,
    'tar': archivers.make_archive,
    'unzip': archivers.unpack,
    'untar': archivers.unpack,
    'grep': grep.grep,
    'touch': touch.touch,
    'mkdir': mkdir.mkdir,
}
