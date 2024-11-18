"""
Library Features:

Name:          lib_utils_model
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20231010'
Version:       '1.0.0'
"""


# ----------------------------------------------------------------------------------------------------------------------
# libraries
import logging
import numpy as np
import pandas as pd

from lib_utils_generic import invert_dict
from lib_info_args import logger_name

import matplotlib.dates as mdates
import matplotlib.pylab as plt

# logging
log_stream = logging.getLogger(logger_name)
logging.getLogger('matplotlib').setLevel(logging.WARNING)
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to filter model data
def filter_model_data(dframe_data, dframe_fields=None,
                      var_tag_rain='rain', var_tag_airt='air_temperature', var_tag_sm='soil_moisture',
                      var_no_data=-9999.0,
                      interp_limit_airt=2, interp_limit_sm=2,
                      interp_direction_airt='both', interp_direction_sm='both'):

    # sort data by index
    dframe_data = dframe_data.sort_index()

    # filter data null of rain
    dframe_data[dframe_data[var_tag_rain] == var_no_data] = np.nan
    # remove data null (based on rain values)
    dframe_data = dframe_data.dropna(how='all')

    # filter data null of air temperature
    mask_airt = (dframe_data[var_tag_airt] == var_no_data)
    dframe_data[var_tag_airt][mask_airt] = np.nan
    # filter data null of soil moisture
    mask_sm = (dframe_data[var_tag_sm] == var_no_data)
    dframe_data[var_tag_sm][mask_sm] = np.nan

    # fill nans with interpolation (
    dframe_data[var_tag_airt] = dframe_data[var_tag_airt].interpolate(
        limit=interp_limit_airt, limit_direction=interp_direction_airt)
    dframe_data[var_tag_sm] = dframe_data[var_tag_sm].interpolate(
        limit=interp_limit_sm, limit_direction=interp_direction_sm)

    # dframe fields default
    if dframe_fields is None:
        dframe_fields = {}
    # organize file fields
    tmp_fields = invert_dict(dframe_fields)
    dframe_data = dframe_data.rename(columns=tmp_fields)

    return dframe_data
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to organize model results
def organize_model_results(dframe_common,
                           values_results, values_time, dframe_fields=None,
                           var_tag_time='time'):

    dict_results = {'values_model': values_results}
    dframe_results = pd.DataFrame(dict_results, index=values_time)
    dframe_results.index.name = var_tag_time

    dframe_common = dframe_common.join(dframe_results)

    # dframe fields default
    if dframe_fields is None:
        dframe_fields = {}
    # organize file fields
    dframe_common = dframe_common.rename(columns=dframe_fields)

    return dframe_common
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to organize model metrics
def organize_model_metrics(data_metrics, data_registry, data_time=None, data_fields=None):

    if data_time is None:
        data_time = {}

    # organize model metrics and registry
    data_common = {**data_metrics, **data_registry, **data_time}

    # define data fields
    if data_fields is None:
        data_list = list(data_common.keys())
    else:
        data_list = list(data_fields.keys())

    # iterate over data fields
    data_filter = {}
    for data_key, data_value in data_common.items():
        if data_key in data_list:
            data_filter[data_key] = data_value

    dframe_filter = pd.DataFrame(data=data_filter, index=['info'])

    return dframe_filter
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to organize model data
def organize_model_data(dframe_data, var_tag_rain='values_k1', var_tag_airt='values_k2', var_tag_sm='values_k3'):

    # get rain and time data
    if var_tag_rain in list(dframe_data.columns):
        dframe_data_rain = dframe_data[var_tag_rain]
        values_rain = dframe_data_rain.values
        values_time = dframe_data_rain.index
    else:
        log_stream.error(' ===> Variable "' + var_tag_rain + '" not included in the dataframe obj')
        raise IOError('Check your dataframe obj')
    # get airt data
    if var_tag_airt in list(dframe_data.columns):
        dframe_data_airt = dframe_data[var_tag_airt]
        values_airt = dframe_data_airt.values
    else:
        log_stream.error(' ===> Variable "' + var_tag_airt + '" not included in the dataframe obj')
        raise IOError('Check your dataframe obj')
    # get sm data
    if var_tag_sm in list(dframe_data.columns):
        dframe_data_sm = dframe_data[var_tag_sm]
        values_sm = dframe_data_sm.values
    else:
        log_stream.error(' ===> Variable "' + var_tag_sm + '" not included in the dataframe obj')
        raise IOError('Check your dataframe obj')

    if len(values_rain) != len(values_airt) != len(values_sm):
        log_stream.error(' ===> Variables have different length')
        raise IOError('Check your dataframe obj')

    values_data = np.dstack((values_rain, values_airt,values_sm))[0, :, :]

    return values_data, values_time
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to organize model parameters
def organize_model_parameters(params_dict, parameters_list=None, parameters_mandatory=True):

    if parameters_list is None:
        parameters_list = ['w_p', 'w_max', 'alpha', 'm2', 'ks', 'kc', 'theta_min', 'theta_max']

    parameters_values = []
    for parameters_name in parameters_list:

        if parameters_name in list(params_dict.keys()):
            parameters_values.append(params_dict[parameters_name])
        else:
            if parameters_mandatory:
                log_stream.error(' ===> Variable "' + parameters_name + '" not included in the parameters dictionary')
                raise IOError('Check your parameters dictionary')
            else:
                log_stream.warning(' ===> Variable "' + parameters_name + '" not included in the parameters dictionary')

    # convert parameters values in array
    values_params = np.array(parameters_values)

    return values_params
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# Method to configure time-series axes
def configure_time_axes(time_data, time_format='%Y-%m-%d'):

    tick_time_period = list(time_data)
    tick_time_idx = time_data
    tick_time_labels = [tick_label.strftime(time_format) for tick_label in time_data]

    return tick_time_period, tick_time_idx, tick_time_labels
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to plot model results
def plot_model_results(file_name, dframe_results, dframe_metrics,
                       fig_spacing_x=None, fig_dpi=150, fig_show=True,
                       no_data_rain=-9999.0, no_data_air_t=-9999.0,
                       no_data_theta_obs=-9999.0, no_data_theta_sim=-9999.0,
                       **kwargs):

    # sort data by index (time)
    dframe_results = dframe_results.sort_index()

    # compute expected time period and data frame
    time_index_start, time_index_end = dframe_results.index[0], dframe_results.index[-1]
    time_index_resolution = dframe_results.index.resolution

    if time_index_resolution == 'hour':
        time_index_frequency = 'H'
    else:
        log_stream.error(' ===> Time resolution not expected in the dataframe obj')
        raise NotImplemented('Case not implemented yet')
    time_index_range = pd.date_range(start=time_index_start, end=time_index_end, freq=time_index_frequency)

    dframe_expected = pd.DataFrame(index=time_index_range)
    dframe_expected = dframe_expected.join(dframe_results)

    # get ts values
    values_time = dframe_expected.index
    values_rain = dframe_expected['rain'].values
    values_air_t = dframe_expected['air_temperature'].values
    values_theta_obs = dframe_expected['theta_observed'].values
    values_theta_sim = dframe_expected['theta_simulated'].values

    # nullify no data values
    values_rain[values_rain == no_data_rain] = np.nan
    values_air_t[values_air_t == no_data_air_t] = np.nan
    values_theta_obs[values_theta_obs == no_data_theta_obs] = np.nan
    values_theta_sim[values_theta_sim == no_data_theta_sim] = np.nan

    # get metrics values
    metrics_ns = dframe_metrics['ns'].values[0]
    metrics_ns_ln_q = dframe_metrics['ns_ln_q'].values[0]
    metrics_ns_rad_q = dframe_metrics['ns_rad_q'].values[0]
    metrics_kge = dframe_metrics['kge'].values[0]
    metrics_rmse = dframe_metrics['rmse'].values[0]
    metrics_rq = dframe_metrics['rq'].values[0]
    # get registry values
    registry_name = dframe_metrics['name'].values[0].strip()
    registry_catchment = dframe_metrics['catchment'].values[0].strip()
    registry_time = dframe_metrics['time'].values[0]

    # filter ts values (remove no data values)
    values_rain[values_rain == -9999] = np.nan
    values_theta_obs[values_theta_obs == -9999] = np.nan
    values_theta_sim[values_theta_sim == -9999] = np.nan

    y_min_sm = -0.05
    y_max_sm = 1.05
    y_min_rain = 0
    y_max_rain = np.nanmax([np.nanmax(values_rain[np.isfinite(values_rain)]), 25])
    y_min_air_t = np.nanmin([np.nanmin(values_air_t[np.isfinite(values_air_t)]), -25])
    y_max_air_t = np.nanmax([np.nanmax(values_air_t[np.isfinite(values_air_t)]), 50])

    # select time start and time end
    time_start_string, time_start_stamp = values_time[0].strftime('%Y-%m-%d %H:%M'), values_time[0]
    time_end_string, time_end_stamp = values_time[-1].strftime('%Y-%m-%d %H:%M'), values_time[-1]

    time_period_tick, time_idx_tick, time_labels_tick = configure_time_axes(values_time)

    if fig_spacing_x is not None:

        spacing_type = 'automatic'
        if 'type' in list(fig_spacing_x.keys()):
            spacing_type = fig_spacing_x['type']
        spacing_offset = 0
        if 'offset' in list(fig_spacing_x.keys()):
            spacing_offset = fig_spacing_x['offset']

        if spacing_type == 'days':
            time_period_tick_start = time_period_tick[0]
            time_period_tick_end = time_period_tick[-1] + pd.DateOffset(days=spacing_offset)
        elif spacing_type == 'months':
            time_period_tick_start = time_period_tick[0]
            time_period_tick_end = time_period_tick[-1] + pd.DateOffset(months=spacing_offset)
        else:
            time_period_tick_start = time_period_tick[0]
            time_period_tick_end = time_period_tick[-1]
    else:
        time_period_tick_start = time_period_tick[0]
        time_period_tick_end = time_period_tick[-1]

    # plot figure
    fig = plt.figure(figsize=(10, 7))
    fig.autofmt_xdate()

    # title
    s = ('Point -- Name: "' + registry_name + '" Catchment: "' + registry_catchment + '"\n'
         ' Time Ref: "' + registry_time + ' Time Period Start: "' +
         time_start_string + '" Time Period End: "' + time_end_string +
         '" UTC \n'
         f'NS: "{metrics_ns:.3f}" NS(lnSD): "{metrics_ns_ln_q:.3f}" NS(radSD): "{metrics_ns_rad_q:.3f}" '
         f'RQ: "{metrics_rq:.3f}" RMSE: "{metrics_rmse:.3f}" KGE: "{metrics_kge:.3f}"')

    # upper panel (soil moisture)
    ax1 = plt.axes([0.1, 0.5, 0.8, 0.40])
    ax1.set_title(s, fontsize=10, fontweight='bold')
    ax1.plot(values_time, values_theta_obs, 'g', linewidth=2, label=r'$\theta_{obs}$')
    ax1.plot(values_time, values_theta_sim, 'r', linewidth=1, label=r'$\theta_{sim}$')
    ax1.legend()
    ax1.set_ylabel('Relative Soil Moisture [-]')
    ax1.set_xlim([time_period_tick_start, time_period_tick_end])
    ax1.set_ylim([y_min_sm, y_max_sm])
    ax1.tick_params(labelbottom=False)
    ax1.grid(b=True)

    # lower panel (rain)
    ax2 = plt.axes([0.1, 0.1, 0.8, 0.40])
    ax2.plot(values_time, values_rain, color=[.5, .5, .5], linewidth=1, label='rain')
    ax2.set_ylabel('Rain (mm/h)')
    ax2.set_ylim([y_min_rain, y_max_rain])
    ax2.set_xlim(time_period_tick_start, time_period_tick_end)
    ax2.tick_params(axis='x', labelrotation=45, labelsize=6)
    ax2.grid(b=True)

    ax3 = ax2.twinx()
    ax3.plot(values_time, values_air_t, color='r', linewidth=0.2, label='air temperature')
    ax3.set_ylabel('Air Temperature (C)')
    ax3.set_ylim(y_min_air_t, y_max_air_t)
    ax3.set_xlim(time_period_tick_start, time_period_tick_end)

    # save figure
    plt.savefig(file_name, format='png', dpi=fig_dpi)

    if fig_show:
        plt.show()
# ----------------------------------------------------------------------------------------------------------------------
