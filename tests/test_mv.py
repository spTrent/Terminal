import os
import shutil
import tempfile
from pathlib import Path

import pytest

import src.config.exceptions
from src.utilities.mv import mv


class TestMvCommand:

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

        Path(self.test_dir, 'file1.txt').write_text('Content 1')
        Path(self.test_dir, 'file2.txt').write_text('Content 2')
        Path(self.test_dir, 'subdir1').mkdir()
        Path(self.test_dir, 'subdir2').mkdir()
        Path(self.test_dir, 'subdir1', 'nested.txt').write_text('Nested')

        yield

        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)


    def test_mv_file_rename(self):
        mv(set(), ['file1.txt', 'renamed.txt'])

        assert not Path(self.test_dir, 'file1.txt').exists()
        assert Path(self.test_dir, 'renamed.txt').exists()
        assert Path(self.test_dir, 'renamed.txt').read_text() == 'Content 1'

    def test_mv_file_to_dir(self):
        mv(set(), ['file1.txt', 'subdir1/'])

        assert not Path(self.test_dir, 'file1.txt').exists()
        assert Path(self.test_dir, 'subdir1', 'file1.txt').exists()
        assert Path(self.test_dir, 'subdir1', 'file1.txt').read_text() == 'Content 1'

    def test_mv_file_to_dir2(self):
        mv(set(), ['file2.txt', 'subdir1'])

        assert not Path(self.test_dir, 'file2.txt').exists()
        assert Path(self.test_dir, 'subdir1', 'file2.txt').exists()
        assert Path(self.test_dir, 'subdir1', 'file2.txt').read_text() == 'Content 2'

    def test_mv_file_to_dir_rename(self):
        mv(set(), ['file2.txt', 'subdir1/renamed.txt'])

        assert not Path(self.test_dir, 'file2.txt').exists()
        assert Path(self.test_dir, 'subdir1', 'renamed.txt').exists()
        assert Path(self.test_dir, 'subdir1', 'renamed.txt').read_text() == 'Content 2'

    def test_mv_files_to_dir(self):
        mv(set(), ['file1.txt', 'file2.txt', 'subdir1'])

        assert not Path(self.test_dir, 'file1.txt').exists()
        assert not Path(self.test_dir, 'file2.txt').exists()
        assert Path(self.test_dir, 'subdir1', 'file1.txt').read_text() == 'Content 1'
        assert Path(self.test_dir, 'subdir1', 'file2.txt').read_text() == 'Content 2'

    def test_mv_dir_rename(self):
        mv(set(), ['subdir1', 'renamed_dir'])

        assert not Path(self.test_dir, 'subdir1').exists()
        assert Path(self.test_dir, 'renamed_dir').exists()
        assert Path(self.test_dir, 'renamed_dir', 'nested.txt').read_text() == 'Nested'

    def test_mv_dir_to_dir(self):
        Path(self.test_dir, 'target').mkdir()
        mv(set(), ['subdir1', 'target'])

        assert not Path(self.test_dir, 'subdir1').exists()
        assert Path(self.test_dir, 'target', 'subdir1').exists()
        assert Path(self.test_dir, 'target', 'subdir1', 'nested.txt').read_text() == 'Nested'


    def test_mv_with_abs_path(self):
        source = os.path.abspath('file1.txt')
        mv(set(), [source, 'renamed.txt'])

        assert not Path(self.test_dir, 'file1.txt').exists()
        assert Path(self.test_dir, 'renamed.txt').read_text() == 'Content 1'

    def test_mv_with_abs_path_dest(self):
        nest = Path(self.test_dir, 'subdir1', 'nested_dir')
        os.mkdir(nest)
        dest = os.path.abspath(nest)
        mv(set(), ['file1.txt', dest])

        assert not Path(self.test_dir, 'file1.txt').exists()
        assert Path(self.test_dir, 'subdir1', 'nested_dir', 'file1.txt').read_text() == 'Content 1'

    def test_mv_with_relative_path(self):
        mv(set(), ['./file1.txt', './subdir1'])

        assert not Path(self.test_dir, 'file1.txt').exists()
        assert Path(self.test_dir, 'subdir1', 'file1.txt').read_text() == 'Content 1'

    def test_mv_nested_file(self):
        mv(set(), ['subdir1/nested.txt', 'moved.txt'])

        assert not Path(self.test_dir, 'subdir1', 'nested.txt').exists()
        assert Path(self.test_dir, 'moved.txt').exists()
        assert Path(self.test_dir, 'moved.txt').read_text() == 'Nested'

    def test_mv_with_parent_directory(self):
        os.chdir(Path(self.test_dir, 'subdir1'))
        mv(set(), ['nested.txt', '../moved.txt'])

        assert not Path(self.test_dir, 'subdir1', 'nested.txt').exists()
        assert Path(self.test_dir, 'moved.txt').read_text() == 'Nested'

    def test_mv_nonexist_file(self):
        with pytest.raises(src.config.exceptions.PathError):
            mv(set(), ['haha.txt', 'dest.txt'])

    def test_mv_with_flag(self):
        with pytest.raises(src.config.exceptions.IncorrectFlag):
            mv({'f'}, ['file1.txt', 'renamed.txt'])

    def test_mv_without_arguments(self):
        with pytest.raises(src.config.exceptions.IncorrectInput):
            mv(set(), [])

    def test_mv_with_one_argument(self):
        with pytest.raises(src.config.exceptions.IncorrectInput):
            mv(set(), ['file1.txt'])

    def test_mv_file_already_exists(self, capsys):
        Path(self.test_dir, 'target.txt').write_text('Target')
        mv(set(), ['file1.txt', 'target.txt'])
        captured = capsys.readouterr()

        assert 'target.txt уже существует' in captured.out
        assert Path(self.test_dir, 'file1.txt').exists()
        assert Path(self.test_dir, 'target.txt').read_text() == 'Target'

    def test_mv_permission_error(self, capsys):
        Path(self.test_dir, 'file_perm.txt').touch()
        original_mode = Path(self.test_dir).stat().st_mode
        Path(self.test_dir).chmod(0o555)
        try:
            mv(set(), ['file_perm.txt', '~'])
            captured = capsys.readouterr()

            assert 'Недостаточно прав' in captured.out
        finally:
            Path(self.test_dir).chmod(original_mode)

    def test_mv_file_with_spaces_in_name(self):
        Path(self.test_dir, 'file with spaces.txt').write_text('Content')
        mv(set(), ['file with spaces.txt', 'renamed.txt'])

        assert not Path(self.test_dir, 'file with spaces.txt').exists()
        assert Path(self.test_dir, 'renamed.txt').exists()


    def test_mv_multiple_files_mixed_types(self):
        mv(set(), ['file1.txt', 'subdir1', 'subdir2'])

        assert not Path(self.test_dir, 'file1.txt').exists()
        assert not Path(self.test_dir, 'subdir1').exists()
        assert Path(self.test_dir, 'subdir2', 'file1.txt').exists()
        assert Path(self.test_dir, 'subdir2', 'subdir1').exists()
        assert Path(self.test_dir, 'subdir2', 'subdir1', 'nested.txt').read_text() == 'Nested'

    def test_mv_to_nested_directory(self):
        Path(self.test_dir, 'subdir1', 'subdir3').mkdir()
        mv(set(), ['file1.txt', 'subdir1/subdir3'])

        assert not Path(self.test_dir, 'file1.txt').exists()
        assert Path(self.test_dir, 'subdir1', 'subdir3', 'file1.txt').read_text() == 'Content 1'

    def test_mv_to_nested_directory_rename(self):
        Path(self.test_dir, 'subdir1', 'subdir3').mkdir()
        mv(set(), ['file1.txt', 'subdir1/subdir3/renamed.txt'])

        assert not Path(self.test_dir, 'file1.txt').exists()
        assert Path(self.test_dir, 'subdir1', 'subdir3', 'renamed.txt').read_text() == 'Content 1'


    def test_mv_partial_success(self, capsys):
        Path(self.test_dir, 'nested.txt').touch()
        Path(self.test_dir, 'existing.txt').write_text('Exists')
        mv(set(), ['file2.txt', 'nested.txt', 'existing.txt', 'subdir1'])
        captured = capsys.readouterr()

        assert not Path(self.test_dir, 'file2.txt').exists()
        assert Path(self.test_dir, 'subdir1', 'file2.txt').exists()
        assert Path(self.test_dir, 'subdir1', 'file2.txt').read_text() == 'Content 2'
        assert 'nested.txt уже существует' in captured.out
        assert Path(self.test_dir, 'nested.txt').exists()
        assert Path(self.test_dir, 'subdir1', 'nested.txt').exists()
        assert Path(self.test_dir, 'subdir1','existing.txt').exists()
        assert Path(self.test_dir, 'subdir1','existing.txt').read_text() == 'Exists'


    def test_mv_directory_with_many_files(self):
        many_files_dir = Path(self.test_dir, 'many_files')
        many_files_dir.mkdir()

        for i in range(50):
            Path(self.test_dir, 'many_files', f'file_{i}').touch()

        mv(set(), ['many_files', 'moved_many_files'])

        assert not Path(self.test_dir, 'many_files').exists()
        assert Path(self.test_dir, 'moved_many_files').exists()
        assert all(Path(self.test_dir, 'moved_many_files', f'file_{i}').exists() for i in range(50))
