"""
Library Features:

Name:          lib_data_io_generic
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20220320'
Version:       '1.0.0'
"""

# ----------------------------------------------------------------------------------------------------------------------
# libraries
import logging
import numpy as np
import pandas as pd

from copy import deepcopy

from lib_info_args import logger_name
from lib_utils_time import define_time_frequency

# logging
log_stream = logging.getLogger(logger_name)
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to combine data over the expected time range
def combine_data_point_by_time(dframe_k1, dframe_k2, dframe_k3,
                               time_tag='time', time_frequency='H', time_reverse=True,
                               no_data_k1=-9999, no_data_k2=-9999, no_data_k3=-9999,
                               scale_factor_k1=1, scale_factor_k2=1, scale_factor_k3=0.01):

    # check dataframes
    if (dframe_k1 is None) or (dframe_k2 is None) or (dframe_k3 is None):
        log_stream.warning(' ===> Dataframes are not defined; One or more dataframes are defined by None')
        return None

    # define time common limits
    time_start_k1, time_end_k1 = dframe_k1.index.min(), dframe_k1.index.max()
    time_start_k2, time_end_k2 = dframe_k2.index.min(), dframe_k2.index.max()
    time_start_k3, time_end_k3 = dframe_k3.index.min(), dframe_k3.index.max()

    time_start_common = pd.DatetimeIndex([time_start_k1, time_start_k2, time_start_k3]).min()
    time_end_common = pd.DatetimeIndex([time_end_k1, time_end_k2, time_end_k3]).max()

    time_range_common = pd.date_range(time_start_common, time_end_common, freq=time_frequency)

    # get attributes
    attrs_common = dframe_k1.attrs

    # remove time information from each dataframe and apply scale factor
    dframe_k1 = dframe_k1.drop(columns=[time_tag])

    if 'values_k1' not in dframe_k1.columns:
        log_stream.error(' ===> Dataframe 1 does not have the column "values_k1"')
        raise RuntimeError('Column "values_k1" must be included in the dataframe. '
                           'Check if the variable mapping is correctly defined')

    dframe_k1['values_k1'][dframe_k1['values_k1'] == no_data_k1] = np.nan
    dframe_k1['values_k1'] = dframe_k1['values_k1'].values * scale_factor_k1
    dframe_k1['values_k1'][np.isnan(dframe_k1['values_k1'])] = no_data_k1

    dframe_k2 = dframe_k2.drop(columns=[time_tag])

    if 'values_k2' not in dframe_k2.columns:
        log_stream.error(' ===> Dataframe 2 does not have the column "values_k2"')
        raise RuntimeError('Column "values_k2" must be included in the dataframe. '
                           'Check if the variable mapping is correctly defined')

    dframe_k2['values_k2'][dframe_k2['values_k2'] == no_data_k2] = np.nan
    dframe_k2['values_k2'] = dframe_k2['values_k2'].values * scale_factor_k2
    dframe_k2['values_k2'][np.isnan(dframe_k2['values_k2'])] = no_data_k2

    dframe_k3 = dframe_k3.drop(columns=[time_tag])

    if 'values_k3' not in dframe_k3.columns:
        log_stream.error(' ===> Dataframe 3 does not have the column "values_k3"')
        raise RuntimeError('Column "values_k3" must be included in the dataframe. '
                           'Check if the variable mapping is correctly defined')

    dframe_k3['values_k3'][dframe_k3['values_k3'] == no_data_k3] = np.nan
    dframe_k3['values_k3'] = dframe_k3['values_k3'].values * scale_factor_k3
    dframe_k3['values_k3'][np.isnan(dframe_k3['values_k3'])] = no_data_k3

    # define common dataframe
    dframe_common = pd.DataFrame(index=time_range_common)
    dframe_common.index.name = time_tag
    dframe_common = dframe_common.join(dframe_k1)
    dframe_common = dframe_common.join(dframe_k2)
    dframe_common = dframe_common.join(dframe_k3)
    # add column time to the dataframe
    if time_tag not in dframe_common.columns:
        dframe_common[time_tag] = dframe_common.index

    # time reverse flag
    if time_reverse:
        dframe_common = dframe_common.sort_index(ascending=False)

    dframe_common.attrs = attrs_common

    return dframe_common

# ----------------------------------------------------------------------------------------------------------------------
