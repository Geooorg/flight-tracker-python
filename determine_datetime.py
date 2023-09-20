import datetime
from zoneinfo import ZoneInfo

class UnixTimestampSplitter:

    @staticmethod
    def split_unix_timestamp(timestamp):

        result_tuple = datetime.datetime.fromtimestamp(timestamp, tz=ZoneInfo("Europe/Berlin"))

        year = result_tuple.year
        month = result_tuple.month
        day = result_tuple.day
        hour = result_tuple.hour
        minute = result_tuple.minute
        second = result_tuple.second

        return year, month, day, hour, minute, second
