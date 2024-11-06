"""
Library Features:

Name:          lib_utils_time
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20231121'
Version:       '1.1.0'
"""

# ----------------------------------------------------------------------------------------------------------------------
# libraries
import logging
import re
import pandas as pd

from datetime import datetime, timedelta
from datetime import date

from lib_info_args import logger_name

# logging
log_stream = logging.getLogger(logger_name)
logging.getLogger('rasterio').setLevel(logging.WARNING)
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to split time part
def split_time_part(time_frequency):

    if time_frequency[0].isalpha():
        time_frequency = time_frequency.lower()
        time_period = 1
    else:
        time_period = time_frequency[0]
        time_frequency = time_frequency[1:].lower()

    return time_period, time_frequency
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to replace time part
def replace_time_part(time_obj_src, time_rounding='H', time_value=0):

    time_list = []
    for time_step in time_obj_src:
        if time_rounding == 'H':
            time_tmp = time_step.replace(hour=time_value)
        else:
            log_stream.error(' ===> Time rounding "' + time_rounding + '" is not expected')
            raise NotImplementedError('Case not implemented yet')
        time_list.append(time_tmp)

    time_obj_dst = pd.DatetimeIndex(time_list)

    return time_obj_dst
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# Method to set time info
def set_time_info(time_run_args=None, time_run_file=None,
                  time_format='%Y-%m-%d %H:$M', time_frequency='H', time_rounding='H'):

    log_stream.info(' ----> Set time info ... ')

    if time_run_args is not None:
        time_run = time_run_args
        log_stream.info(' ------> Time ' + time_run + ' set by argument')
    elif (time_run_args is None) and (time_run_file is not None):
        time_run = time_run_file
        log_stream.info(' ------> Time ' + time_run + ' set by user')
    elif (time_run_args is None) and (time_run_file is None):
        time_now = date.today()
        time_run = time_now.strftime(time_format)
        log_stream.info(' ------> Time ' + time_run + ' set by system')
    else:
        log_stream.info(' ----> Set time info ... FAILED')
        log_stream.error(' ===> Argument "time_run" is not correctly set')
        raise IOError('Time type or format is wrong')

    time_run = pd.Timestamp(time_run)
    if time_rounding.isupper():
        time_rounding = time_rounding.lower()
    time_reference = time_run.floor(time_rounding)

    log_stream.info(' ----> Set time info ... DONE')

    return time_run, time_reference

# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to define time frequency
def define_time_frequency(time_index, time_freq_default='D'):

    if isinstance(time_index, pd.DatetimeIndex):
        if time_index.shape[0] >= 3:
            time_freq_raw = pd.infer_freq(time_index)

            if time_freq_raw is None:
                log_stream.warning(' ===> Time freq is not defined by inferred frequency. Define using the '
                                   'time delta methods')
                time_delta = time_index[1] - time_index[0]
                time_freq_raw = time_delta.resolution_string

            time_freq_str = re.findall("[a-zA-Z]+", time_freq_raw)[0]

        elif time_index.shape[0] == 2:
            time_delta = time_index[1] - time_index[0]
            time_freq_str = time_delta.resolution_string
        elif time_index.shape[0] == 1:
            time_freq_str = time_freq_default
        else:
            log_stream.error(' ===> Time index is not correctly defined. Check your settings file.')
            raise RuntimeError('Time index is not correctly defined')
    else:
        log_stream.warning(' ===> Time index is not defined by pd.DatetimeIndex. '
                           'The time frequency is set to "' + time_freq_default + '"')
        time_freq_str = time_freq_default

    return time_freq_str
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# Method to define time period
def define_time_range(time_dict, time_reverse=False):

    time_period = time_dict['time_period']
    time_reference = time_dict['time_reference']
    time_frequency = time_dict['time_frequency']
    time_rounding = time_dict['time_rounding']
    time_start = time_dict['time_start']
    time_end = time_dict['time_end']

    if time_start and time_end:

        time_start, time_end = pd.Timestamp(time_start), pd.Timestamp(time_end)
        time_start, time_end = time_start.round(time_rounding), time_end.round(time_rounding)

        time_range = pd.date_range(start=time_start, end=time_end, freq=time_frequency)

    elif time_period and time_reference:

        time_end = pd.Timestamp(time_reference)
        time_end = time_end.round(time_rounding)
        time_range = pd.date_range(end=time_end, periods=time_period, freq=time_frequency)

        time_start = time_range[0]

    else:
        log_stream.error(' ===> "time_start" and "time_end" or "time_period" and "time_reference" must be defined')
        raise RuntimeError('Time information are not enough to define the "time_range')

    if time_reverse:
        time_range = time_range[::-1]

    return time_range, time_start, time_end
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to convert datetime to datenum (matlab)
def datetime_to_datenum(dt):

   #ord = dt.toordinal()

   mdn = dt + timedelta(days=366)
   frac = (dt - datetime(dt.year, dt.month, dt.day,0, 0, 0)).seconds / (24.0 * 60.0 * 60.0)

   datenum = mdn.toordinal() + frac

   return datenum
# ----------------------------------------------------------------------------------------------------------------------
