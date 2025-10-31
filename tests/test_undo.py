import os
import shutil
import tempfile
from pathlib import Path

import pytest

import src.config.consts
import src.config.exceptions
from src.utilities.undo import undo


class TestUndoCommand:
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)
        self.trash_path = Path(self.test_dir, '.trash')
        self.trash_path.mkdir()
        self.original = src.config.consts.TRASH_PATH
        src.config.consts.TRASH_PATH = self.trash_path
        
        self.original_history = src.config.consts.FOR_UNDO_HISTORY.copy()
        src.config.consts.FOR_UNDO_HISTORY.clear()
        
        yield
        
        src.config.consts.FOR_UNDO_HISTORY.clear()
        src.config.consts.FOR_UNDO_HISTORY.extend(self.original_history)
        
        src.config.consts.TRASH_PATH = self.original
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)

    def test_undo_with_flag(self):
        with pytest.raises(src.config.exceptions.IncorrectFlag):
            undo({'a'}, [])

    def test_undo_with_paths(self):
        with pytest.raises(src.config.exceptions.IncorrectInput):
            undo(set(), ['file.txt'])

    def test_undo_nothing_to_undo(self):
        with pytest.raises(src.config.exceptions.NothingToUndo):
            undo(set(), [])

    def test_undo_cp_file(self):
        source = Path(self.test_dir, 'source.txt')
        source.write_text('content')
        dest = Path(self.test_dir, 'dest.txt')
        dest.write_text('content')
        
        src.config.consts.FOR_UNDO_HISTORY.append(
            ('cp', set(), ['source.txt', 'dest.txt'])
        )
        undo(set(), [])
        
        assert not dest.exists()
        assert source.exists()

    def test_undo_cp_directory_r(self):
        source_dir = Path(self.test_dir, 'source_dir')
        source_dir.mkdir()
        Path(source_dir, 'file.txt').write_text('content')
        dest_dir = Path(self.test_dir, 'dest_dir')
        dest_dir.mkdir()
        Path(dest_dir, 'file.txt').write_text('content')
        
        src.config.consts.FOR_UNDO_HISTORY.append(
            ('cp', {'r'}, ['source_dir', 'dest_dir'])
        )
        undo(set(), [])
        
        assert not dest_dir.exists()
        assert source_dir.exists()

    def test_undo_cp_directory_recursive(self):
        source_dir = Path(self.test_dir, 'source_dir')
        source_dir.mkdir()
        Path(source_dir, 'file.txt').write_text('content')
        dest_dir = Path(self.test_dir, 'dest_dir')
        dest_dir.mkdir()
        Path(dest_dir, 'file.txt').write_text('content')
        
        src.config.consts.FOR_UNDO_HISTORY.append(
            ('cp', {'recursive'}, ['source_dir', 'dest_dir'])
        )
        undo(set(), [])
        
        assert not dest_dir.exists()
        assert source_dir.exists()

    def test_undo_mv_file(self):
        dest = Path(self.test_dir, 'dest.txt')
        dest.write_text('content')
        
        src.config.consts.FOR_UNDO_HISTORY.append(
            ('mv', set(), [['source.txt', 'dest.txt']])
        )
        undo(set(), [])
        
        assert Path(self.test_dir, 'source.txt').exists()
        assert Path(self.test_dir, 'source.txt').read_text() == 'content'
        assert not dest.exists()

    def test_undo_mv_files(self):
        dest1 = Path(self.test_dir, 'dest1.txt')
        dest1.write_text('content1')
        dest2 = Path(self.test_dir, 'dest2.txt')
        dest2.write_text('content2')
        
        src.config.consts.FOR_UNDO_HISTORY.append(
            ('mv', set(), [
                ['source1.txt', 'dest1.txt'],
                ['source2.txt', 'dest2.txt']
            ])
        )
        undo(set(), [])
        
        assert Path(self.test_dir, 'source1.txt').exists()
        assert Path(self.test_dir, 'source2.txt').exists()
        assert not dest1.exists()
        assert not dest2.exists()

    def test_undo_mv_file_already_exists(self, capsys):
        dest = Path(self.test_dir, 'dest.txt')
        dest.write_text('content')
        
        source = Path(self.test_dir, 'source.txt')
        source.write_text('exist content')
        
        src.config.consts.FOR_UNDO_HISTORY.append(
            ('mv', set(), [['source.txt', 'dest.txt']])
        )
        undo(set(), [])
        captured = capsys.readouterr()
        
        assert 'source.txt пропущен: уже существует' in captured.out
        assert dest.exists()

    def test_undo_rm_file(self):
        trash_file = Path(self.trash_path, 'file.txt')
        trash_file.touch()
        
        src.config.consts.FOR_UNDO_HISTORY.append(
            ('rm', set(), [[Path(self.test_dir, 'file.txt'), trash_file]])
        )
        undo(set(), [])
            
        assert Path(self.test_dir, 'file.txt').exists()
        assert not trash_file.exists()

    def test_undo_multiple_operations(self):
        dest1 = Path(self.test_dir, 'dest1.txt')
        dest1.write_text('content1')
        dest2 = Path(self.test_dir, 'dest2.txt')
        dest2.write_text('content2')
        
        src.config.consts.FOR_UNDO_HISTORY.append(
            ('cp', set(), ['source1.txt', 'dest1.txt'])
        )
        src.config.consts.FOR_UNDO_HISTORY.append(
            ('cp', set(), ['source2.txt', 'dest2.txt'])
        )
        undo(set(), [])
        
        assert not dest2.exists()
        assert dest1.exists()
        
        undo(set(), [])
        
        assert not dest1.exists()

    def test_undo_empties_history(self):
        dest = Path(self.test_dir, 'dest.txt')
        dest.write_text('content')
        
        src.config.consts.FOR_UNDO_HISTORY.append(
            ('cp', set(), ['source.txt', 'dest.txt'])
        )
        
        assert len(src.config.consts.FOR_UNDO_HISTORY) == 1
        undo(set(), [])
        assert len(src.config.consts.FOR_UNDO_HISTORY) == 0

    def test_undo_preserves_file_content(self):
        dest = Path(self.test_dir, 'dest.txt')
        dest.write_text('Content')
        
        src.config.consts.FOR_UNDO_HISTORY.append(
            ('mv', set(), [['source.txt', 'dest.txt']])
        )
        undo(set(), [])
        
        assert Path(self.test_dir, 'source.txt').read_text() == 'Content'

    def test_undo_rm_deleted_from_trash(self, capsys):
        trash_file = Path(self.trash_path, 'file.txt')
        
        src.config.consts.FOR_UNDO_HISTORY.append(
            ('rm', set(), [[Path(self.test_dir, 'file.txt'), trash_file]])
        )
        undo(set(), [])
        captured = capsys.readouterr()
        
        assert 'file.txt удален' in captured.out

    def test_undo_check_lifo(self):
        dest1 = Path(self.test_dir, 'dest1.txt')
        dest1.write_text('first')
        dest2 = Path(self.test_dir, 'dest2.txt')
        dest2.write_text('second')
        dest3 = Path(self.test_dir, 'dest3.txt')
        dest3.write_text('third')
        
        src.config.consts.FOR_UNDO_HISTORY.append(
            ('mv', set(), [['s1.txt', 'dest1.txt']])
        )
        src.config.consts.FOR_UNDO_HISTORY.append(
            ('mv', set(), [['s2.txt', 'dest2.txt']])
        )
        src.config.consts.FOR_UNDO_HISTORY.append(
            ('mv', set(), [['s3.txt', 'dest3.txt']])
        )
    
        undo(set(), [])
        assert Path(self.test_dir, 's3.txt').read_text() == 'third'
        assert dest2.exists()
        assert dest1.exists()
        
        undo(set(), [])
        assert Path(self.test_dir, 's3.txt').read_text() == 'third'
        assert Path(self.test_dir, 's2.txt').read_text() == 'second'
        assert dest1.exists()
        
        undo(set(), [])
        assert Path(self.test_dir, 's3.txt').read_text() == 'third'
        assert Path(self.test_dir, 's2.txt').read_text() == 'second'
        assert Path(self.test_dir, 's1.txt').read_text() == 'first'

    def test_undo_cp_nested_directory(self):
        dest_dir = Path(self.test_dir, 'dest_dir')
        dest_dir.mkdir()
        nested = Path(dest_dir, 'nested')
        nested.mkdir()
        Path(nested, 'file.txt').write_text('nested content')
        
        src.config.consts.FOR_UNDO_HISTORY.append(
            ('mv', {'r'}, [['source_dir', 'dest_dir']])
        )
        undo(set(), [])
        
        assert not dest_dir.exists()
        assert Path(self.test_dir, 'source_dir', 'nested', 'file.txt').read_text() == 'nested content'
