import time
from six import string_types
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from pytz import timezone


class TimeUtils(object):

    @classmethod
    def cvt_datetime2timestamp(cls, dtime):
        '''
            input: dtime:type(datetime)
            output: timestamp:type(int)
        '''
        return int(time.mktime(dtime.timetuple()))

    @classmethod
    def cvt_timestamp2datetime(cls, tstamp):
        '''
            input: tstamp:type(int)
            output: datetime:type(datetime)
        '''
        return datetime.fromtimestamp(tstamp)

    @classmethod
    def cvt_datetime2str(cls, base, fmt='%Y-%m-%d %H:%M:%S'):
        '''
            input: base(int | datetime), fmt:type(str)
            output: type(str)
        '''
        if isinstance(base, int):
            base = cls.cvt_timestamp2datetime(base)

        return base.strftime(fmt)

    @classmethod
    def cvt_date2datetime(cls, dtdate):
        '''
            input:  dtdate:type(date)
            output: datetime:type(datetime)
        '''
        return datetime.combine(dtdate, datetime.min.time())

    @classmethod
    def cvt_datetime(cls, base, fmt="%Y-%m-%d %H:%M:%S"):
        '''
            input:  base:type(int | datetime | date | string)
            output: datetime:type(datetime)
        '''
        if isinstance(base, string_types):
            base = datetime.strptime(base, fmt)

        elif isinstance(base, int):
            base = cls.cvt_timestamp2datetime(base)

        elif isinstance(base, date):
            base = cls.cvt_date2datetime(base)

        elif isinstance(base, datetime):
            pass
        else:
            print(type(base))
            raise TypeError

        return base

    @classmethod
    def cvt_second2timeformat(cls, seconds):
        '''
            input: seconds:type(int)
            output: time: type(timedelta)
        '''
        return timedelta(seconds=seconds)

    @classmethod
    def add_second(cls, base, seconds):
        '''
            input: base:type(int | datetime), seconds:type(int)
            output: timestamp:type(int)
        '''
        if isinstance(base, int):
            result = cls.cvt_timestamp2datetime(
                base) + timedelta(seconds=seconds)
        elif isinstance(base, datetime):
            result = base + timedelta(seconds=seconds)
        else:
            raise TypeError
        return cls.cvt_datetime2timestamp(result)

    @classmethod
    def add_day(cls, base, days):
        '''
            input: base:type(int | datetime), days:type(int)
            output: timestamp:type(int)
        '''
        return cls.add_second(base, days * 24 * 60 * 60)

    @classmethod
    def add_month(cls, base, months, fmt="%Y-%m-%d"):
        '''
            input:  base:type(int | datetime | string)
            output: timestamp:type(int)
        '''

        return cls.cvt_datetime(base, fmt) + relativedelta(months=months)

    @classmethod
    def get_now(cls, fmt='dt'):
        '''
            input: fmt(dt->datetime | ts->timestamp)
            output: datetime:type(datetime) | timestamp:type(int)
        '''
        today = time.time()
        if fmt == 'dt':
            return cls.cvt_timestamp2datetime(today)
        elif fmt == 'ts':
            return int(today)

    @classmethod
    def get_specified_day_of_month(cls, base, fmt="%Y-%m-%d", day=1):
        '''
            input:  base:type(int | datetime | date | string)
            output: datetime:type(datetime.date)
        '''
        base_dt = cls.cvt_datetime(base, fmt)
        return date(base_dt.year, base_dt.month, day)

    @classmethod
    def get_last_day_of_month(cls, base, fmt="%Y-%m-%d"):
        '''
            input:  base:type(int | datetime | date | string)
            output: datetime:type(datetime)
        '''
        base_dt = cls.cvt_datetime(base, fmt)
        base_dt_add = cls.add_month(base_dt, 1)
        return date(base_dt_add.year, base_dt_add.month,
                    1) - relativedelta(days=1)

    @classmethod
    def cvt_timezone(cls, base_tz, target_tz, base, fmt="%Y-%m-%d %H:%M:%S"):
        '''
            input:
                    base_tz: timzone type(string)
                    target_tz: timzone type(string)
                    base:type(int | datetime | date | string)
            output: datetime:type(datetime)
        '''
        base_dt = cls.cvt_datetime(base, fmt)
        base_pytz = timezone(base_tz)
        base_tz_dt = base_pytz.localize(base_dt, is_dst=None)

        target_pytz = timezone(target_tz)
        target_tz_dt = base_tz_dt.astimezone(target_pytz)
        return target_tz_dt

    @classmethod
    def validate_dtfmt(cls, date_text, fmt='%Y-%m-%d'):
        """
            input:
                    date_text: type(string)
                    fmt: type(string)
        """
        try:
            datetime.strptime(date_text, fmt)
        except ValueError:
            raise ValueError("Incorrect data format, should be {}".format(fmt))
