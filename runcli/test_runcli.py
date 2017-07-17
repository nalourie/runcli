"""
runcli.test_runcli
==================
Tests for ``runcli.runcli``.
"""

import logging
import os
import shutil
import stat
import tempfile
import unittest

from . import runcli


logger = logging.getLogger(__name__)


# eventually this context manager should be replaced with
# tempfile.TemporaryDirectory when only newer versions of python are
# targeted by this project.
class TemporaryDirectory(object):
    """A context manager that creates a temporary directory.

    This context manager returns the path to a temporary directory which
    is destroyed upon exiting the context.

    Use this context manager for python 2.7 compatibility. A version of
    this context manager exists in the tempfile module in newer versions
    of python.
    """

    def __enter__(self):
        """Create an return a temporary directory."""
        self.tmp_dir_path = tempfile.mkdtemp()
        return self.tmp_dir_path

    def __exit__(self, *args):
        """Remove the temporary directory created by __enter__."""
        shutil.rmtree(self.tmp_dir_path)


class TestGetRunfilePath(unittest.TestCase):
    """Test ``runcli.get_runfile_path``."""

    def test_gets_runfile_path_from_directory(self):
        """Test ``get_runfile_path`` gets the right path from the dir.

        Test that ``get_runfile_path` gets the correct path to the
        Runfile when in the same directory as the Runfile.
        """
        with TemporaryDirectory() as tmp_dir_path:
            # on MacOS '/var' is a symlink to '/private/var' so we need
            # to get the real path returned by TemporaryDirectory
            tmp_dir_path = os.path.realpath(tmp_dir_path)
            runfile_path = os.path.join(tmp_dir_path, 'Runfile')
            with open(runfile_path, 'w') as runfile:
                runfile.write('')

            os.chdir(tmp_dir_path)
            self.assertEqual(
                runcli.get_runfile_path(),
                runfile_path)

    def test_gets_runfile_path_from_subdirectory(self):
        """Test ``get_runfile_path`` gets the right path from a subdir.

        Test that ``get_runfile_path`` gets the correct path to the
        Runfile when in a subdirectory of the directory contianing the
        Runfile.
        """
        with TemporaryDirectory() as tmp_dir_path:
            # on MacOS '/var' is a symlink to '/private/var' so we need
            # to get the real path returned by TemporaryDirectory
            tmp_dir_path = os.path.realpath(tmp_dir_path)
            runfile_path = os.path.join(tmp_dir_path, 'Runfile')
            with open(runfile_path, 'w') as runfile:
                runfile.write('')
            subdir_path = os.path.join(tmp_dir_path, 'subdir')
            os.mkdir(subdir_path)

            os.chdir(subdir_path)
            self.assertEqual(
                runcli.get_runfile_path(),
                runfile_path)

    def test_raises_error_when_runfile_missing(self):
        """Test ``get_runfile_path`` raises error if Runfile is missing."""
        with TemporaryDirectory() as tmp_dir_path:
            # on MacOS '/var' is a symlink to '/private/var' so we need
            # to get the real path returned by TemporaryDirectory
            tmp_dir_path = os.path.realpath(tmp_dir_path)

            os.chdir(tmp_dir_path)
            with self.assertRaises(RuntimeError):
                runcli.get_runfile_path()


class TestMain(unittest.TestCase):
    "Test ``runcli.main``."""

    def test_main(self):
        """Test ``runcli.main`` end to end."""
        with TemporaryDirectory() as tmp_dir_path:
            # on MacOS '/var' is a symlink to '/private/var' so we need
            # to get the real path returned by TemporaryDirectory
            tmp_dir_path = os.path.realpath(tmp_dir_path)
            runfile_path = os.path.join(tmp_dir_path, 'Runfile')
            tmp_output_path = os.path.join(tmp_dir_path, 'tmp.txt')
            with open(runfile_path, 'w') as runfile:
                runfile.write(
                    '#! /bin/bash\n'
                    'echo $@ > {tmp_output_path}\n'.format(
                        tmp_output_path=tmp_output_path))
            # make the runfile executable
            os.chmod(
                runfile_path,
                os.stat(runfile_path).st_mode | stat.S_IEXEC)

            # test main functionality in same directory as Runfile
            os.chdir(tmp_dir_path)
            runcli.main('foo bar --baz')
            with open(tmp_output_path, 'r') as tmp_output_file:
                self.assertEqual(
                    tmp_output_file.read(),
                    'foo bar --baz\n')
            # test main functionality in a subdirectory of the directory
            # containing the Runfile
            subdir_path = os.path.join(tmp_dir_path, 'subdir')
            os.mkdir(subdir_path)
            os.chdir(subdir_path)
            runcli.main('--foo --bar baz')
            with open(tmp_output_path, 'r') as tmp_output_file:
                self.assertEqual(
                    tmp_output_file.read(),
                    '--foo --bar baz\n')
