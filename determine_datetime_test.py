import unittest

from determine_datetime import UnixTimestampSplitter


class TestUnixTimestampSplitter(unittest.TestCase):
    def test_split_unix_timestamp(self):
        timestamp = 1694871429
        splitter = UnixTimestampSplitter()
        year, month, day, hour, minute, seconds = splitter.split_unix_timestamp(timestamp)

        assert year == 2023
        assert month == 9
        assert day == 16
        assert hour == 15
        assert minute == 37
        assert seconds == 9


if __name__ == "__main__":
    test = TestUnixTimestampSplitter()
    test.test_split_unix_timestamp()