import os
import shutil
import tempfile
from pathlib import Path

import pytest

import src.config.exceptions
from src.utilities.cd import cd


class TestCdCommand:
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

        Path(self.test_dir, 'subdir1').mkdir()
        Path(self.test_dir, 'subdir2').mkdir()
        Path(self.test_dir, 'subdir1', 'nested').mkdir()
        Path(self.test_dir, 'file.txt').touch()

        yield

        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)

    def test_cd_subdir(self):
        cd(set(), ['subdir1'])

        assert os.getcwd() == os.path.join(self.test_dir, 'subdir1')

    def test_cd_abs_path(self):
        target_dir = os.path.join(self.test_dir, 'subdir2')
        cd(set(), [target_dir])

        assert os.getcwd() == target_dir

    def test_cd_nested_dir(self):
        cd(set(), ['subdir1/nested'])

        assert os.getcwd() == os.path.join(self.test_dir, 'subdir1', 'nested')

    def test_cd_parent_dir(self):
        subdir = os.path.join(self.test_dir, 'subdir1')
        os.chdir(subdir)
        cd(set(), ['..'])

        assert os.getcwd() == self.test_dir

    def test_cd_curr_directory(self):
        initial_dir = os.getcwd()
        cd(set(), ['.'])

        assert os.getcwd() == initial_dir

    def test_cd_home_dir(self):
        cd(set(), ['~'])

        assert os.getcwd() == os.path.expanduser('~')

    def test_cd_back_from_home(self):
        cd(set(), ['~'])
        cd(set(), [self.test_dir])

        assert os.getcwd() == self.test_dir

    def test_cd_empty_path(self):
        cd(set(), [])

        assert os.getcwd() == os.path.expanduser('~')

    def test_cd_nonexist_dir(self):
        with pytest.raises(src.config.exceptions.PathError):
            cd(set(), ['haha'])

    def test_cd_to_file(self):
        with pytest.raises(src.config.exceptions.IsNotDirectory):
            cd(set(), ['file.txt'])

    def test_cd_with_flag(self):
        with pytest.raises(src.config.exceptions.IncorrectFlag):
            cd({'l'}, ['subdir1'])

    def test_cd_many_args(self):
        with pytest.raises(src.config.exceptions.IncorrectInput):
            cd(set(), ['subdir1', 'subdir2'])

    def test_cd_from_nested_dir(self):
        nested_dir = os.path.join(self.test_dir, 'subdir1', 'nested')
        os.chdir(nested_dir)
        cd(set(), ['../..'])

        assert os.getcwd() == self.test_dir

    def test_cd_curr_relative(self):
        cd(set(), ['./subdir1'])

        assert os.getcwd() == os.path.join(self.test_dir, 'subdir1')

    def test_cd_parent_relative(self):
        subdir1 = os.path.join(self.test_dir, 'subdir1')
        os.chdir(os.path.join(subdir1))
        cd(set(), ['../subdir2'])

        assert os.getcwd() == os.path.join(self.test_dir, 'subdir2')

    def test_cd_many_slashes(self):
        cd(set(), ['subdir1///nested'])

        assert os.getcwd() == os.path.join(self.test_dir, 'subdir1', 'nested')

    def test_cd_dir_with_spaces(self):
        dir_with_spaces = Path(self.test_dir, 'dir with spaces')
        dir_with_spaces.mkdir()
        cd(set(), ['dir with spaces'])

        assert os.getcwd() == str(dir_with_spaces)

    def test_cd_to_root(self):
        cd(set(), ['/'])

        assert os.getcwd() == os.path.abspath(os.sep)
