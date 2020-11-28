
from pathlib import Path

import pytest

from cli_toolkit.exceptions import FileParserError
from cli_toolkit.textfile import LineTextFile, SortedLineTextFile

from . import DATA_DIRECTORY

TEST_FILE = DATA_DIRECTORY.joinpath('linefile')
TEST_FILE_CUSTOM_COMMENTS = DATA_DIRECTORY.joinpath('linefile_custom_comments')
TEST_FILE_SORTED = DATA_DIRECTORY.joinpath('linefile_sorted')

SKIPPED_LINE = 'skipme'


class UnsortedLinesFile(LineTextFile):
    """
    Base class to test text files
    """

    def parse_line(self, line):
        """
        Dummy method to parse test list
        """
        if line == SKIPPED_LINE:
            return None
        return super().parse_line(line)


class SortedTestLinesFile(SortedLineTextFile):
    """
    Base class to test sorted text files
    """

    def parse_line(self, line):
        """
        Dummy method to parse test list
        """
        if line == SKIPPED_LINE:
            return None
        return super().parse_line(line)


def validate_test_file(datafile, path, line_count):
    """
    Validate test file common properties
    """
    assert datafile.path == path
    assert len(datafile) == line_count


def test_file_lines_parsing():
    """
    Test parsing trivial line based files
    """
    datafile = UnsortedLinesFile(TEST_FILE)
    validate_test_file(datafile, TEST_FILE, line_count=3)


def test_file_custom_comments_parsing():
    """
    Test parsing trivial line based files
    """
    comment_prefixes = '#!'
    datafile = UnsortedLinesFile(TEST_FILE, comment_prefixes=comment_prefixes)
    validate_test_file(datafile, TEST_FILE, line_count=3)


def test_file_lines_sorted_parsing():
    """
    Test parsing trivial line based files with sorting
    """
    datafile = SortedTestLinesFile(TEST_FILE_SORTED)
    validate_test_file(datafile, TEST_FILE_SORTED, line_count=4)


def test_file_lines_loading_path_is_directory():
    """
    Test loading of directory as file
    """
    path = Path(__file__).parent
    with pytest.raises(FileParserError):
        UnsortedLinesFile(path)
    with pytest.raises(FileParserError):
        SortedTestLinesFile(path)


def test_file_invalid_file_path():
    """
    Test loading non-existing path
    """
    with pytest.raises(FileParserError):
        UnsortedLinesFile('3F403784-1316-4F12-B1BD-F05F72B915D2')
    with pytest.raises(FileParserError):
        SortedTestLinesFile('3F403784-1316-4F12-B1BD-F05F72B915D2')
