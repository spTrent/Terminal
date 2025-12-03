import os
import shutil
import tempfile
from pathlib import Path

import pytest

import src.config.exceptions
from src.utilities.archivers import is_archive, make_archive, unpack

class TestIsArchive:
    def test_is_archive_zip(self):
        assert is_archive('file.zip') is True

    def test_is_archive_tar(self):
        assert is_archive('file.tar') is True

    def test_is_archive_tar_gz(self):
        assert is_archive('file.tar.gz') is True

    def test_is_archive_tar_bz(self):
        assert is_archive('file.tar.bz') is True

    def test_is_archive_tar_xz(self):
        assert is_archive('file.tar.xz') is True

    def test_is_archive_with_path(self):
        assert is_archive('/path/to/archive.zip') is True

    def test_is_not_archive_txt(self):
        with pytest.raises(src.config.exceptions.IsNotArchive):
            is_archive('file.txt')

    def test_is_not_archive_no_extension(self):
        with pytest.raises(src.config.exceptions.IsNotArchive):
            is_archive('file')

    def test_is_not_archive_wrong_extension(self):
        with pytest.raises(src.config.exceptions.IsNotArchive):
            is_archive('file.rar')

    def test_is_not_archive_partial_match(self):
        with pytest.raises(src.config.exceptions.IsNotArchive):
            is_archive('file.tarz')


class TestMakeArchive:
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

        self.source_dir = Path(self.test_dir, 'source_dir')
        self.source_dir.mkdir()
        Path(self.source_dir, 'file1.txt').write_text('Content 1')
        Path(self.source_dir, 'file2.txt').write_text('Content 2')

        yield

        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)

    def test_make_zip_archive(self):
        make_archive('zip', set(), ['source_dir', 'output'])
        assert Path(self.test_dir, 'output.zip').exists()

    def test_make_tar_archive(self):
        make_archive('tar', set(), ['source_dir', 'output'])
        assert Path(self.test_dir, 'output.tar.gz').exists()

    def test_make_archive_with_relative_path(self):
        make_archive('zip', set(), ['./source_dir', 'output'])
        assert Path(self.test_dir, 'output.zip').exists()

    def test_make_archive_with_abs_path(self):
        abs_path = str(self.source_dir)
        make_archive('zip', set(), [abs_path, 'output'])
        assert Path(self.test_dir, 'output.zip').exists()

    def test_make_archive_path(self):
        make_archive('zip', set(), ['source_dir'])
        assert Path(self.test_dir, 'source_dir.zip').exists()

    def test_make_archive_with_flag(self):
        with pytest.raises(src.config.exceptions.IncorrectFlag):
            make_archive('zip', {'r'}, ['source_dir', 'output'])

    def test_make_archive_too_many_paths(self):
        with pytest.raises(src.config.exceptions.IncorrectInput):
            make_archive('zip', set(), ['dir1', 'dir2', 'dir3'])

    def test_make_archive_not_directory(self):
        Path(self.test_dir, 'file.txt').touch()
        with pytest.raises(src.config.exceptions.IsNotDirectory):
            make_archive('zip', set(), ['file.txt', 'output'])

    def test_make_archive_nonexistpath(self):
        with pytest.raises(src.config.exceptions.PathError):
            make_archive('zip', set(), ['haha', 'output'])

    def test_make_zip__tar(self):
        make_archive('zip', set(), ['source_dir', 'output'])
        make_archive('tar', set(), ['source_dir', 'output'])

        assert Path(self.test_dir, 'output.zip').exists()
        assert Path(self.test_dir, 'output.tar.gz').exists()

    def test_make_archive_overwrite_existing(self):
        Path(self.test_dir, 'test').mkdir()
        make_archive('zip', set(), ['source_dir', 'output'])
        size = Path(self.test_dir, 'output.zip').stat().st_size

        assert Path(self.test_dir, 'output.zip').exists()

        make_archive('zip', set(), ['test', 'output'])
        new_size = Path(self.test_dir, 'output.zip').stat().st_size

        assert Path(self.test_dir, 'output.zip').exists()
        assert new_size < size

class TestUnpack:
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

        self.source_dir = Path(self.test_dir, 'archive_content')
        self.source_dir.mkdir()
        Path(self.source_dir, 'file1.txt').write_text('Content 1')
        Path(self.source_dir, 'file2.txt').write_text('Content 2')

        shutil.make_archive('test_archive', 'zip', self.source_dir)
        shutil.make_archive('test_tar', 'gztar', self.source_dir)

        shutil.rmtree(self.source_dir)

        yield

        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)

    def test_unpack_zip(self):
        unpack('unzip', set(), ['test_archive.zip'])

        assert Path(self.test_dir, 'test_archive').exists()
        assert Path(self.test_dir, 'test_archive', 'file1.txt').exists()
        assert Path(self.test_dir, 'test_archive', 'file2.txt').exists()

    def test_unpack_tar_gz(self):
        unpack('untar', set(), ['test_tar.tar.gz'])

        assert Path(self.test_dir, 'test_tar').exists()
        assert Path(self.test_dir, 'test_tar', 'file1.txt').exists()

    def test_unpack_with_relative_path(self):
        unpack('unzip', set(), ['./test_archive.zip'])

        assert Path(self.test_dir, 'test_archive').exists()

    def test_unpack_with_abs_path(self):
        abs_path = os.path.join(self.test_dir, 'test_archive.zip')
        unpack('unzip', set(), [abs_path])

        assert Path(self.test_dir, 'test_archive').exists()

    def test_unpack_with_flag(self):
        with pytest.raises(src.config.exceptions.IncorrectFlag):
            unpack('unzip', {'x'}, ['test_archive.zip'])

    def test_unpack_too_many_paths(self):
        with pytest.raises(src.config.exceptions.IncorrectInput):
            unpack('unzip', set(), ['archive1.zip', 'archive2.zip'])

    def test_unpack_no_paths(self):
        with pytest.raises(src.config.exceptions.IncorrectInput):
            unpack('unzip', set(), [])

    def test_unpack_not_archive(self):
        Path(self.test_dir, 'file.txt').touch()
        with pytest.raises(src.config.exceptions.IsNotArchive):
            unpack('unzip', set(), ['file.txt'])

    def test_unpack_nonexist_file(self):
        with pytest.raises(src.config.exceptions.PathError):
            unpack('unzip', set(), ['haha.zip'])

    def test_unpack_existing_dest(self):
        with pytest.raises(src.config.exceptions.AlreadyExists):
            unpack('unzip', set(), ['test_archive.zip'])
            unpack('unzip', set(), ['test_archive.zip'])

    def test_unpack_preserves_content(self):
        unpack('unzip', set(), ['test_archive.zip'])

        content1 = Path(self.test_dir, 'test_archive', 'file1.txt').read_text()
        content2 = Path(self.test_dir, 'test_archive', 'file2.txt').read_text()

        assert content1 == 'Content 1'
        assert content2 == 'Content 2'

    def test_unpack_creates_directory_with_archive_name(self):
        unpack('unzip', set(), ['test_archive.zip'])

        assert Path(self.test_dir, 'test_archive').is_dir()

    def test_unpack_nested_archive_structure(self):
        nested_dir = Path(self.test_dir, 'nested_content')
        nested_dir.mkdir()
        subdir = Path(nested_dir, 'subdir')
        subdir.mkdir()
        Path(subdir, 'nested.txt').write_text('Nested content')
        shutil.make_archive('nested_archive', 'zip', nested_dir)
        shutil.rmtree(nested_dir)
        unpack('unzip', set(), ['nested_archive.zip'])

        assert Path(self.test_dir, 'nested_archive', 'subdir', 'nested.txt').exists()

    def test_unpack_archive_with_dots_in_name(self):
        dots_dir = Path(self.test_dir, 'dots_content')
        dots_dir.mkdir()
        Path(dots_dir, 'file.txt').touch()

        shutil.make_archive('archive.with.dots', 'zip', dots_dir)
        shutil.rmtree(dots_dir)

        unpack('unzip', set(), ['archive.with.dots.zip'])
        assert Path(self.test_dir, 'archive.with.dots').exists()
