import os
import shutil
import tempfile
from pathlib import Path

import pytest

import src.config.exceptions
from src.utilities.ls import ls


class TestLsCommand:
    """Набор тестов для команды ls."""

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

        Path(self.test_dir, 'file1.txt').touch()
        Path(self.test_dir, 'file2.py').touch()
        Path(self.test_dir, '.hidden_file').touch()
        Path(self.test_dir, 'subdir').mkdir()
        Path(self.test_dir, 'subdir', 'nested.txt').touch()

        yield

        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)

    def test_ls_without_arguments(self, capsys):
        ls(set(), [])
        captured = capsys.readouterr()

        assert '.hidden_file' not in captured.out
        assert 'file1.txt' in captured.out
        assert 'file2.py' in captured.out
        assert 'subdir' in captured.out

    def test_ls_with_relative_path(self, capsys):
        ls(set(), ['subdir'])
        captured = capsys.readouterr()

        assert 'nested.txt' in captured.out

    def test_ls_with_abs_path(self, capsys):
        ls(set(), [os.path.abspath('subdir')])
        captured = capsys.readouterr()

        assert 'nested.txt' in captured.out

    def test_ls_with_l_flag(self, capsys):
        ls({'l'}, [])
        captured = capsys.readouterr()

        assert 'file1.txt' in captured.out
        assert any(i in captured.out for i in '0123456789')
        assert 'rw' in captured.out
        assert any(
            i in captured.out
            for i in 'Jan Feb Mar Apr May Jun' + ' Jul Aug Sep Oct Nov Dec'
        )

    def test_ls_l_shows_file_size_relative(self, capsys):
        test_file = Path(self.test_dir, 'subdir', 'nested.txt')
        test_file.write_text('Hello World!')

        ls({'l'}, ['subdir'])
        captured = capsys.readouterr()

        assert 'nested.txt' in captured.out
        assert any(i in captured.out for i in '123456789')

    def test_ls_l_shows_file_size_abs(self, capsys):
        test_file = Path(self.test_dir, 'subdir', 'nested.txt')
        test_file.write_text('Hello World!')

        ls({'l'}, [os.path.abspath('subdir')])
        captured = capsys.readouterr()

        assert 'nested.txt' in captured.out
        assert any(i in captured.out for i in '123456789')

    def test_ls_nonexists_path(self):
        with pytest.raises(src.config.exceptions.PathError):
            ls(set(), ['haha'])

    def test_ls_file_instead_of_directory(self):
        with pytest.raises(src.config.exceptions.IsNotDirectory):
            ls(set(), ['file1.txt'])

    def test_ls_incorrect_flag(self):
        with pytest.raises(src.config.exceptions.IncorrectFlag):
            ls({'a'}, ['subdir'])

    def test_ls_incorrect_flags(self):
        with pytest.raises(src.config.exceptions.IncorrectFlag):
            ls({'l', 'a', 'f'}, [])

    def test_ls_with_tilde(self, capsys):
        ls(set(), ['~'])
        captured = capsys.readouterr()
        assert 'Terminal' in captured.out

    def test_ls_with_parent_directory(self, capsys):
        subdir = os.path.join(self.test_dir, 'subdir')
        os.chdir(subdir)

        ls(set(), ['..'])
        captured = capsys.readouterr()

        assert 'file1.txt' in captured.out

    def test_ls_with_current_directory_dot(self, capsys):
        ls(set(), ['.'])
        captured = capsys.readouterr()

        assert 'file1.txt' in captured.out

    def test_ls_empty_directory(self, capsys):
        empty_dir = os.path.join(self.test_dir, 'empty')
        os.mkdir(empty_dir)

        ls(set(), [empty_dir])
        captured = capsys.readouterr()

        assert not captured.out

    def test_ls_with_many_paths(self, capsys):
        subdir2 = os.path.join(self.test_dir, 'sub_dir2')
        os.mkdir(subdir2)
        Path(subdir2, 'file3.txt').touch()

        ls(set(), [os.path.abspath('subdir'), subdir2])
        captured = capsys.readouterr()

        assert 'subdir' in captured.out
        assert 'sub_dir2' in captured.out
        assert 'nested.txt' in captured.out
        assert 'file3.txt' in captured.out

    def test_ls_with_many_files(self, capsys):
        files_dir = os.path.join(self.test_dir, 'files')
        os.mkdir(files_dir)

        for i in range(100):
            Path(files_dir, f'file_{i}.txt').touch()

        ls(set(), [files_dir])
        captured = capsys.readouterr()

        assert all(f'file_{i}.txt' in captured.out for i in range(100))
