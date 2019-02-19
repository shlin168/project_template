from datetime import datetime
from jinja2.exceptions import FilterArgumentError

from cathay_time_utils.time_utils import TimeUtils


def dt_format(value, format='%Y-%m-%d'):
    """
    Convert datetime value to string.

    :type value: datetime
    :rtype : str
    """
    if isinstance(value, datetime):
        return TimeUtils.cvt_datetime2str(value, format)
    else:
        raise FilterArgumentError("value must be datetime instance Now is {}".format(type(value)))


def dt_add_month(value, trace_num=0, format='%Y-%m'):
    """
    :type value: datetime
    :rtype : str
    """
    if isinstance(value, datetime):
        result_dt = TimeUtils.add_month(value, months=trace_num)
        return TimeUtils.cvt_datetime2str(result_dt, format)
    else:
        raise FilterArgumentError("value must be datetime instance Now is {}".format(type(value)))


def dt_add_day(value, trace_num=0, format='%Y-%m-%d'):
    """
    :type value: datetime
    :rtype : str
    """
    if isinstance(value, datetime):
        result_dt = TimeUtils.add_day(value, days=trace_num)
        return TimeUtils.cvt_datetime2str(result_dt, format)
    else:
        raise FilterArgumentError("value must be datetime instance Now is {}".format(type(value)))


CUSTOM_FILTERS = {
    'dt.format': dt_format,
    'dt.add_month': dt_add_month,
    'dt.add_day': dt_add_day
}
