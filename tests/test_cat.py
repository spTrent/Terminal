import os
import shutil
import tempfile
from pathlib import Path

import pytest

import src.config.exceptions
from src.utilities.cat import cat


class TestCatCommand:
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

        Path(self.test_dir, 'file1.txt').write_text('Hello World!')
        Path(self.test_dir, 'file2.txt').write_text('Line 1\nLine 2\nLine 3')
        Path(self.test_dir, 'empty.txt').touch()
        Path(self.test_dir, 'subdir').mkdir()
        Path(self.test_dir, 'subdir', 'nested.txt').write_text('Content')

        yield

        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)

    def test_cat_file(self, capsys):
        cat(set(), ['file1.txt'])
        captured = capsys.readouterr()

        assert 'Hello World!' in captured.out

    def test_cat_files(self, capsys):
        cat(set(), ['file1.txt', 'file2.txt'])
        captured = capsys.readouterr()

        assert 'Hello World!' in captured.out
        assert 'Line 1' in captured.out
        assert 'Line 2' in captured.out
        assert 'Line 3' in captured.out

    def test_cat_empty_file(self, capsys):
        cat(set(), ['empty.txt'])
        captured = capsys.readouterr()

        assert not captured.out

    def test_cat_multiline_file(self, capsys):
        cat(set(), ['file2.txt'])
        captured = capsys.readouterr()

        assert 'Line 1\nLine 2\nLine 3' in captured.out

    def test_cat_abs_path(self, capsys):
        abs_path = os.path.join(self.test_dir, 'file1.txt')
        cat(set(), [abs_path])
        captured = capsys.readouterr()

        assert 'Hello World!' in captured.out

    def test_cat_relative_path(self, capsys):
        cat(set(), ['./file1.txt'])
        captured = capsys.readouterr()

        assert 'Hello World!' in captured.out

    def test_cat_nested_file(self, capsys):
        cat(set(), ['subdir/nested.txt'])
        captured = capsys.readouterr()
        assert 'Content' in captured.out

    def test_cat_nonexist_file(self):
        with pytest.raises(src.config.exceptions.PathError):
            cat(set(), ['haha.txt'])

    def test_cat_dir(self):
        with pytest.raises(src.config.exceptions.IsNotFile):
            cat(set(), ['subdir'])

    def test_cat_empty_paths(self):
        with pytest.raises(src.config.exceptions.IncorrectInput):
            cat(set(), [])

    def test_cat_with_flag(self):
        with pytest.raises(src.config.exceptions.IncorrectFlag):
            cat({'a'}, ['file1.txt'])

    def test_cat_mixed(self, capsys):
        captured = capsys.readouterr()
        with pytest.raises(src.config.exceptions.PathError):
            cat(set(), ['file1.txt', 'haha.txt'])

            assert 'Hello World!' in captured.out

    def test_cat_file_and_dir(self, capsys):
        captured = capsys.readouterr()
        with pytest.raises(src.config.exceptions.IsNotFile):
            cat(set(), ['file1.txt', 'subdir'])

            assert 'Hello World!' in captured.out
