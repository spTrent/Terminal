import os
import shutil
import tempfile
from pathlib import Path

import pytest

import src.config.exceptions
from src.utilities.cp import cp


class TestCpCommand:
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

        Path(self.test_dir, 'file1.txt').write_text('Content 1')
        Path(self.test_dir, 'file2.txt').write_text('Content 2')
        Path(self.test_dir, 'empty.txt').touch()

        Path(self.test_dir, 'dir1').mkdir()
        Path(self.test_dir, 'dir1', 'nested.txt').write_text('Nested')
        Path(self.test_dir, 'dest_dir').mkdir()

        yield

        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)


    def test_cp_file_to_dir(self):
        cp(set(), ['file1.txt', 'dest_dir/'])
        cp(set(), ['file2.txt', 'dest_dir'])

        assert Path(self.test_dir, 'dest_dir', 'file1.txt').exists()
        assert Path(self.test_dir, 'dest_dir', 'file2.txt').exists()
        assert Path(self.test_dir, 'dest_dir', 'file1.txt').read_text() == 'Content 1'
        assert Path(self.test_dir, 'dest_dir', 'file2.txt').read_text() == 'Content 2'


    def test_cp_file_rename(self):
        cp(set(), ['file1.txt', 'file_copy.txt'])

        assert Path(self.test_dir, 'file_copy.txt').exists()
        assert Path(self.test_dir, 'file_copy.txt').read_text() == 'Content 1'

    def test_cp_file_to_dir_rename(self):
        cp(set(), ['file1.txt', 'dest_dir/file_copy.txt'])

        assert Path(self.test_dir, 'dest_dir', 'file_copy.txt').exists()
        assert Path(self.test_dir, 'dest_dir', 'file_copy.txt').read_text() == 'Content 1'


    def test_cp_empty_file(self):
        cp(set(), ['empty.txt', 'empty_copy.txt'])

        assert Path(self.test_dir, 'empty_copy.txt').exists()
        assert not Path(self.test_dir, 'empty_copy.txt').read_text()


    def test_cp_abs_path(self):
        src = os.path.join(self.test_dir, 'file1.txt')
        dest = os.path.join(self.test_dir, 'abs_copy.txt')
        cp(set(), [src, dest])

        assert Path(dest).exists()


    def test_cp_relative_path(self):
        cp(set(), ['./file1.txt', './rel_copy.txt'])

        assert Path(self.test_dir, 'rel_copy.txt').exists()


    def test_cp_dir_with_flag_r(self):
        cp({'r'}, ['dir1', 'dir_copy'])

        assert Path(self.test_dir, 'dir_copy').exists()
        assert Path(self.test_dir, 'dir_copy', 'nested.txt').exists()
        assert Path(self.test_dir, 'dir_copy', 'nested.txt').read_text() == 'Nested'


    def test_cp_dir_with_flag_recursive(self):
        cp({'recursive'}, ['dir1', 'dir_copy'])

        assert Path(self.test_dir, 'dir_copy').exists()
        assert Path(self.test_dir, 'dir_copy', 'nested.txt').exists()
        assert Path(self.test_dir, 'dir_copy', 'nested.txt').read_text() == 'Nested'


    def test_cp_dir_to_dir(self):
        cp({'recursive'}, ['dir1', 'dest_dir'])

        assert Path(self.test_dir, 'dest_dir', 'dir1').exists()
        assert Path(self.test_dir, 'dest_dir', 'dir1', 'nested.txt').exists()
        assert Path(self.test_dir, 'dest_dir', 'dir1', 'nested.txt').read_text() == 'Nested'

    def test_cp_dir_to_dir_rename(self):
        cp({'recursive'}, ['dir1', 'dest_dir/newdir'])

        assert Path(self.test_dir, 'dest_dir', 'newdir').exists()
        assert Path(self.test_dir, 'dest_dir', 'newdir', 'nested.txt').exists()
        assert Path(self.test_dir, 'dest_dir', 'newdir', 'nested.txt').read_text() == 'Nested'


    def test_cp_nonexist_file(self):
        with pytest.raises(src.config.exceptions.PathError):
            cp(set(), ['haha.txt', 'copy.txt'])


    def test_cp_dir_without_flag(self):
        with pytest.raises(src.config.exceptions.IsNotFile):
            cp(set(), ['dir1', 'dir_copy'])


    def test_cp_file_with_flag(self):
        with pytest.raises(src.config.exceptions.IsNotDirectory):
            cp({'r'}, ['file1.txt', 'file_copy.txt'])


    def test_cp_without_paths(self):
        with pytest.raises(src.config.exceptions.IncorrectInput):
            cp(set(), [])


    def test_cp_with_one_path(self):
        with pytest.raises(src.config.exceptions.IncorrectInput):
            cp(set(), ['file1.txt'])


    def test_cp_with_incorrect_path_count(self):
        with pytest.raises(src.config.exceptions.IncorrectInput):
            cp(set(), ['file1.txt', 'file2.txt', 'file3.txt'])


    def test_cp_incorrect_flag(self):
        with pytest.raises(src.config.exceptions.IncorrectFlag):
            cp({'a'}, ['file1.txt', 'copy.txt'])


    def test_cp_incorrect_flags(self):
        with pytest.raises(src.config.exceptions.IncorrectFlag):
            cp({'r', 'a'}, ['file1.txt', 'copy.txt'])

    def test_cp_permission_error_file1(self, capsys):
        cp(set(), ['file1.txt', '~/..'])
        captured = capsys.readouterr()

        assert 'Ошибка: Недостаточно прав' in captured.out

    def test_cp_permission_error_new_file(self, capsys):
        file1 = Path(self.test_dir, 'file1.txt')
        file1.chmod(0o000)

        try:
            cp(set(), ['file1.txt', 'copy.txt'])
            captured = capsys.readouterr()

            assert 'Ошибка: Недостаточно прав' in captured.out
        finally:
            file1.chmod(0o644)
