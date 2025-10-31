import os
import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

import src.config.consts
import src.config.exceptions
from src.utilities.rm import rm


class TestRmCommand:
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)
        self.trash_dir = tempfile.mkdtemp()
        self.original_trash = src.config.consts.TRASH_PATH
        src.config.consts.TRASH_PATH = self.trash_dir

        Path(self.test_dir, 'file1.txt').write_text('Content 1')
        Path(self.test_dir, 'file2.txt').write_text('Content 2')
        Path(self.test_dir, 'dir1').mkdir()
        Path(self.test_dir, 'dir1', 'nested.txt').write_text('Nested')
        Path(self.test_dir, 'dir2').mkdir()
        Path(self.test_dir, 'dir2', 'file.txt').write_text('File in dir2')

        yield

        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)
        shutil.rmtree(self.trash_dir)
        src.config.consts.TRASH_PATH = self.original_trash

    def test_rm_file(self):
        rm(set(), ['file1.txt'])

        assert not Path(self.test_dir, 'file1.txt').exists()
        assert Path(self.trash_dir, 'file1.txt').exists()

    def test_rm_files(self):
        rm(set(), ['file1.txt', 'file2.txt'])

        assert not Path(self.test_dir, 'file1.txt').exists()
        assert not Path(self.test_dir, 'file2.txt').exists()
        assert Path(self.trash_dir, 'file1.txt').exists()
        assert Path(self.trash_dir, 'file2.txt').exists()

    def test_rm_dir_with_flag_r(self):
        with patch('builtins.input', return_value='y'):
            rm({'r'}, ['dir1'])

        assert not Path(self.test_dir, 'dir1').exists()
        assert Path(self.trash_dir, 'dir1').exists()
        assert Path(self.trash_dir, 'dir1', 'nested.txt').read_text() == 'Nested'

    def test_rm_dir_with_flag_recursive(self):
        with patch('builtins.input', return_value='y'):
            rm({'recursive'}, ['dir1'])

        assert not Path(self.test_dir, 'dir1').exists()
        assert Path(self.trash_dir, 'dir1').exists()
        assert Path(self.trash_dir, 'dir1', 'nested.txt').read_text() == 'Nested'

    def test_rm_dir_decline(self):
        with patch('builtins.input', return_value='n'):
            rm({'r'}, ['dir1'])

        assert Path(self.test_dir, 'dir1').exists()

    def test_rm_dir_without_flag(self):
        with pytest.raises(src.config.exceptions.IsNotFile):
            rm(set(), ['dir1'])

    def test_rm_file_with_r_flag(self):
        with pytest.raises(src.config.exceptions.IsNotDirectory):
            rm({'r'}, ['file1.txt'])

    def test_rm_file_with_recursive_flag(self):
        with pytest.raises(src.config.exceptions.IsNotDirectory):
            rm({'recursive'}, ['file1.txt'])

    def test_rm_abs_path(self):
        abs_path = os.path.join(self.test_dir, 'file1.txt')
        rm(set(), [abs_path])

        assert not Path(abs_path).exists()
        assert Path(self.trash_dir, 'file1.txt').exists()

    def test_rm_relative_path(self):
        rm(set(), ['./file1.txt'])

        assert not Path(self.test_dir, 'file1.txt').exists()
        assert Path(self.trash_dir, 'file1.txt').exists()

    def test_rm_nested_file(self):
        rm(set(), ['dir1/nested.txt'])

        assert not Path(self.test_dir, 'dir1', 'nested.txt').exists()
        assert Path(self.trash_dir, 'nested.txt').exists()

    def test_rm_nonexist_file(self):
        with pytest.raises(src.config.exceptions.PathError):
            rm(set(), ['haha.txt'])

    def test_rm_without_paths(self):
        with pytest.raises(src.config.exceptions.IncorrectInput):
            rm(set(), [])

    def test_rm_incorrect_flag(self):
        with pytest.raises(src.config.exceptions.IncorrectFlag):
            rm({'a'}, ['file1.txt'])

    def test_rm_incorrect_flags(self):
        with pytest.raises(src.config.exceptions.IncorrectFlag):
            rm({'r', 'f'}, ['file1.txt'])

    def test_rm_current_directory(self):
        with pytest.raises(src.config.exceptions.TerminalException):
            with patch('builtins.input', return_value='y'):
                rm({'r'}, ['.'])

    def test_rm_parent_directory(self):
        subdir = Path(self.test_dir, 'subdir')
        subdir.mkdir()
        os.chdir(subdir)
        with pytest.raises(src.config.exceptions.TerminalException):
            with patch('builtins.input', return_value='y'):
                rm({'r'}, [self.test_dir])

    def test_rm_file_overwrite_trash(self):
        rm(set(), ['file1.txt'])
        Path(self.test_dir, 'file1.txt').write_text('New Content')
        rm(set(), ['file1.txt'])

        assert not Path(self.test_dir, 'file1.txt').exists()
        assert Path(self.trash_dir, 'file1.txt').read_text() == 'New Content'

    def test_rm_dir_overwrite_trash(self):
        with patch('builtins.input', return_value='y'):
            rm({'r'}, ['dir1'])
        
        Path(self.test_dir, 'dir1').mkdir()
        Path(self.test_dir, 'dir1', 'new_file.txt').write_text('New Content')
        
        with patch('builtins.input', return_value='y'):
            rm({'r'}, ['dir1'])
        
        assert not Path(self.test_dir, 'file1.txt', 'dir1').exists()
        assert Path(self.trash_dir, 'dir1', 'new_file.txt').exists()
        assert not Path(self.trash_dir, 'dir1', 'nested.txt').exists()

    def test_rm_permission_error(self, capsys):
        file_path = Path(self.test_dir, 'file1.txt')
        file_path.chmod(0o000)
        
        try:
            rm(set(), ['file1.txt'])
            captured = capsys.readouterr()
            assert 'Ошибка: нет прав на удаление' in captured.out
            assert Path(self.test_dir, 'file1.txt').exists()
        finally:
            file_path.chmod(0o644)

    def test_rm_partial_success(self, capsys):
        file_path = Path(self.test_dir, 'file2.txt')
        file_path.chmod(0o000)
        Path(self.test_dir, 'file3.txt').touch()
        
        try:
            rm(set(), ['file1.txt', 'file2.txt', 'file3.txt'])
            captured = capsys.readouterr()
            
            assert 'Ошибка: нет прав на удаление file2.txt' in captured.out
            assert not Path(self.test_dir, 'file1.txt').exists()
            assert not Path(self.test_dir, 'file3.txt').exists()
            assert Path(self.test_dir, 'file2.txt').exists()
        finally:
            file_path.chmod(0o644)

    def test_rm_nested_directory(self):
        nested = Path(self.test_dir, 'dir1', 'subdir')
        nested.mkdir()
        Path(nested, 'nested.txt').write_text('Nested Content')
        
        with patch('builtins.input', return_value='y'):
            rm({'r'}, ['dir1'])
        
        assert not Path(self.test_dir, 'dir1').exists()
        assert Path(self.trash_dir, 'dir1', 'subdir', 'nested.txt').exists()

    def test_rm_directory_with_many_files(self):
        many_files_dir = Path(self.test_dir, 'many_files')
        many_files_dir.mkdir()
        
        for i in range(50):
            Path(many_files_dir, f'file_{i}.txt').touch()
        
        with patch('builtins.input', return_value='y'):
            rm({'r'}, ['many_files'])
        
        assert not many_files_dir.exists()
        assert Path(self.trash_dir, 'many_files').exists()
        assert all(
            Path(self.trash_dir, 'many_files', f'file_{i}.txt').exists()
            for i in range(50)
        )

    def test_rm_with_parent_path(self):
        dir1 = Path(self.test_dir, 'dir1')
        os.chdir(dir1)
        rm(set(), ['../file1.txt'])

        assert not Path(self.test_dir, 'file1.txt').exists()
        assert Path(self.trash_dir, 'file1.txt').exists()

    def test_rm_removed_trash(self):
        shutil.rmtree(self.trash_dir) 
        rm(set(), ['file1.txt'])

        assert os.path.exists(self.trash_dir)
        assert Path(self.trash_dir, 'file1.txt').exists()
