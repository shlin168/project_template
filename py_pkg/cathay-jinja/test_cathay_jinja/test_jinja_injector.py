# -*- coding: utf-8 -*-

from datetime import datetime
from cathay_jinja.jinja_injector import JinjaInjector


def test_string_render_args():

    result = JinjaInjector.string_render_args(content="A=> {{A}}", A='10')

    assert result == 'A=> 10'


def test_string_render_args_with_custom_dt_fmt_filter_ym():

    render_value = datetime(2018, 11, 21, 16, 30)
    result = JinjaInjector.string_render_args(
        content="yyyymm=> {{yyyymm|dt.format('%Y%m')}}", yyyymm=render_value)

    assert result == 'yyyymm=> 201811'


def test_string_render_args_with_custom_dt_fmt_filter_ymd():

    render_value = datetime(2018, 11, 21, 16, 30)
    result = JinjaInjector.string_render_args(
        content="yyyymm=> {{yyyymm|dt.format('%Y%m%d')}}", yyyymm=render_value)

    assert result == 'yyyymm=> 20181121'


def test_string_render_args_with_custom_dt_add_day_filter_trace_1():

    render_value = datetime(2018, 11, 21, 16, 30)
    result = JinjaInjector.string_render_args(
        content="yyyymm=> {{yyyymm|dt.add_day(format='%Y%m%d',trace_num=1)}}", yyyymm=render_value)

    assert result == 'yyyymm=> 20181122'


def test_string_render_args_with_custom_dt_add_day_filter_trace_pre_1():

    render_value = datetime(2018, 11, 21, 16, 30)
    result = JinjaInjector.string_render_args(
        content="yyyymm=> {{yyyymm|dt.add_day(format='%Y%m%d',trace_num=-1)}}", yyyymm=render_value)

    assert result == 'yyyymm=> 20181120'


def test_string_render_args_with_custom_dt_add_month_filter_trace_1():

    render_value = datetime(2018, 11, 21, 16, 30)
    result = JinjaInjector.string_render_args(
        content="yyyymm=> {{yyyymm|dt.add_month(format='%Y%m',trace_num=1)}}", yyyymm=render_value)

    assert result == 'yyyymm=> 201812'


def test_string_render_args_with_custom_dt_add_month_filter_trace_pre_1():

    render_value = datetime(2018, 11, 21, 16, 30)
    result = JinjaInjector.string_render_args(
        content="yyyymm=> {{yyyymm|dt.add_month(format='%Y%m',trace_num=-1)}}", yyyymm=render_value)

    assert result == 'yyyymm=> 201810'
