"""
Class Features

Name:          driver_data_dynamic
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20231120'
Version:       '1.5.0'
"""

# -------------------------------------------------------------------------------------
# libraries
import logging
import os

from lib_data_io_generic import combine_data_point_by_time
from lib_data_io_csv import read_datasets_csv, write_datasets_csv

from lib_utils_io import fill_string_with_time, fill_string_with_info
from lib_utils_generic import make_folder

from lib_info_args import logger_name, time_format_algorithm, time_format_datasets

# logging
log_stream = logging.getLogger(logger_name)
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# class driver data
class DriverData:

    # -------------------------------------------------------------------------------------
    # initialize class
    def __init__(self, time_reference, time_run, alg_data_static,
                 alg_data_dynamic, alg_info, alg_template, alg_flags):

        # set time reference
        self.time_reference = time_reference
        self.time_run = time_run

        # set data static object(s)
        self.data_registry = alg_data_static['registry']
        self.data_params = alg_data_static['parameters']

        # set algorithm information
        self.alg_flags = alg_flags
        self.alg_info = alg_info
        self.alg_datasets_src_rain = alg_data_dynamic['source']['rain']
        self.alg_datasets_src_airt = alg_data_dynamic['source']['air_temperature']
        self.alg_datasets_src_sm = alg_data_dynamic['source']['soil_moisture']
        self.alg_datasets_dst = alg_data_dynamic['destination']
        self.alg_template_time = alg_template['time']
        self.alg_template_datasets = alg_template['datasets']

        # reset flags
        self.reset_data_static = self.alg_flags['reset_data_static']
        self.reset_data_dynamic = self.alg_flags['reset_data_dynamic']

        # datasets tag(s)
        self.file_name_tag, self.folder_name_tag = 'file_name', 'folder_name'
        self.time_tag, self.filters_tag = 'time', 'filters'
        self.fields_tag, self.format_tag, self.delimiter_tag = 'fields', 'format', 'delimiter'
        # time tag(s)
        self.time_start_tag = "time_start"
        self.time_end_tag = "time_end"
        self.time_frequency_tag = "time_frequency"
        self.time_rounding_tag = "time_rounding"
        self.time_format_tag = 'time_format'

        # source rain object(s)
        self.folder_name_src_rain = self.alg_datasets_src_rain['folder_name']
        self.file_name_src_rain = self.alg_datasets_src_rain['file_name']
        self.format_rain = self.alg_datasets_src_rain[self.format_tag]
        self.delimiter_rain = self.alg_datasets_src_rain[self.delimiter_tag]
        self.fields_rain = self.alg_datasets_src_rain[self.fields_tag]
        self.time_rain = self.alg_datasets_src_rain[self.time_tag]
        self.filters_rain = self.alg_datasets_src_rain[self.filters_tag]
        self.file_path_src_rain = os.path.join(self.folder_name_src_rain, self.file_name_src_rain)
        # source air temperature object(s)
        self.folder_name_src_airt = self.alg_datasets_src_airt['folder_name']
        self.file_name_src_airt = self.alg_datasets_src_airt['file_name']
        self.format_airt = self.alg_datasets_src_airt[self.format_tag]
        self.delimiter_airt = self.alg_datasets_src_airt[self.delimiter_tag]
        self.fields_airt = self.alg_datasets_src_airt[self.fields_tag]
        self.time_airt = self.alg_datasets_src_airt[self.time_tag]
        self.filters_airt = self.alg_datasets_src_airt[self.filters_tag]
        self.file_path_src_airt = os.path.join(self.folder_name_src_airt, self.file_name_src_airt)
        # source soil moisture object(s)
        self.folder_name_src_sm = self.alg_datasets_src_sm['folder_name']
        self.file_name_src_sm = self.alg_datasets_src_sm['file_name']
        self.format_sm = self.alg_datasets_src_sm[self.format_tag]
        self.delimiter_sm = self.alg_datasets_src_sm[self.delimiter_tag]
        self.fields_sm = self.alg_datasets_src_sm[self.fields_tag]
        self.time_sm = self.alg_datasets_src_sm[self.time_tag]
        self.filters_sm = self.alg_datasets_src_sm[self.filters_tag]
        self.file_path_src_sm = os.path.join(self.folder_name_src_sm, self.file_name_src_sm)

        # destination object(s)
        self.folder_name_dst = self.alg_datasets_dst['folder_name']
        self.file_name_dst = self.alg_datasets_dst['file_name']
        self.format_dst = self.alg_datasets_dst[self.format_tag]
        self.fields_dst = self.alg_datasets_dst[self.fields_tag]
        self.time_dst = self.alg_datasets_dst[self.time_tag]
        self.filters_dst = self.alg_datasets_dst[self.filters_tag]
        self.file_path_dst = os.path.join(self.folder_name_dst, self.file_name_dst)

    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # method to get datasets object
    def get_obj_datasets(self, file_name, file_format='csv', file_delimiter=';',
                         file_mandatory=True,
                         file_fields=None, time_fields=None, registry_fields=None):

        # info start method
        log_stream.info(' -----> Read file datasets "' + file_name + '" ... ')

        # check file existence
        if not os.path.exists(file_name):
            if file_mandatory:
                log_stream.error(' ===> File "' + file_name + '" does not exist')
                raise IOError('File parameters must be available')
            else:
                log_stream.warning(' ===> File "' + file_name + '" does not exist')
                return None

        # check file format
        if file_format == 'csv':

            # time fields
            if time_fields is None:
                time_fields = {}

            # get datasets in ascii format
            fields_obj = read_datasets_csv(
                file_name,
                time_reference=self.time_reference, file_sep=file_delimiter,
                file_fields=file_fields, registry_fields=registry_fields,
                file_decimal='.', **time_fields)

        else:
            # exit with error if file format is not supported
            log_stream.error(' ===> File format "' + file_format + '" is not supported')
            raise NotImplemented('Case not implemented yet')

        # info end method
        log_stream.info(' -----> Read file datasets "' + file_name + '" ... DONE')

        return fields_obj
    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # method to dump datasets object
    def dump_obj_datasets(self, file_name, file_dframe, file_format='csv',
                          file_fields=None, time_fields=None, registry_fields=None):

        # info start method
        log_stream.info(' -----> Dump file datasets "' + file_name + '" ... ')

        # check file format
        if file_format == 'csv':

            # dump combined dframe
            folder_name, _ = os.path.split(file_name)
            make_folder(folder_name)

            # write datasets in csv format
            write_datasets_csv(
                file_name, file_dframe, file_fields=file_fields, time_fields=time_fields,
                dframe_index_label='time', dframe_index_format='%Y-%m-%d %H:%M',
                dframe_sep=';', dframe_decimal='.', dframe_float_format='%.3f',
                dframe_index=True, dframe_header=True)

        else:
            # exit with error if file format is not supported
            log_stream.error(' ===> File format "' + file_format + '" is not supported')
            raise NotImplemented('Case not implemented yet')

        # info end method
        log_stream.info(' -----> Dump file datasets "' + file_name + '" ... DONE')

    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # method to define file string
    def __define_file_string(self, file_string_tmpl, extended_info=None):

        if extended_info is not None:
            alg_info = {**self.alg_info, **extended_info}
        else:
            alg_info = self.alg_info

        file_string_def = fill_string_with_time(file_string_tmpl, self.time_reference, self.alg_template_time)
        file_string_def = fill_string_with_info(file_string_def, alg_info, self.alg_template_datasets)
        return file_string_def
    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # method to organize data
    def organize_data(self):

        # method start info
        log_stream.info(' ----> Organize data dynamic object(s) ... ')

        # get time reference
        time_reference = self.time_reference
        # get data registry
        data_registry = self.data_registry

        # get path(s
        file_path_src_rain_tmpl = self.file_path_src_rain
        file_path_src_airt_tmpl = self.file_path_src_airt
        file_path_src_sm_tmpl = self.file_path_src_sm
        file_path_dst_tmpl = self.file_path_dst

        # get flag(s)
        reset_data_dynamic = self.reset_data_dynamic

        # iterate over geo point(s)
        obj_collections = {}
        for fields_data in data_registry.to_dict(orient="records"):

            # get point information
            point_name, point_tag = fields_data['name'], fields_data['tag']

            # info point start
            log_stream.info(' -----> Point -- (1) Name: "' + point_tag + '" :: (2) Tag: "' + point_tag + '" ... ')

            # method to fill the filename(s)
            file_path_src_rain_point = self.__define_file_string(
                file_path_src_rain_tmpl, extended_info={'point_name': point_tag})
            file_path_src_airt_point = self.__define_file_string(
                file_path_src_airt_tmpl, extended_info={'point_name': point_tag})
            file_path_src_sm_point = self.__define_file_string(
                file_path_src_sm_tmpl, extended_info={'point_name': point_tag})

            file_path_dst_point = self.__define_file_string(
                file_path_dst_tmpl, extended_info={'point_name': point_tag})

            # reset ancillary file if required
            if reset_data_dynamic:
                if os.path.exists(file_path_dst_point):
                    os.remove(file_path_dst_point)

            # check ancillary file availability
            if not os.path.exists(file_path_dst_point):

                # get rain dataframe
                dframe_rain = self.get_obj_datasets(
                    file_path_src_rain_point,
                    file_format=self.format_rain, file_delimiter=self.delimiter_rain, file_mandatory=True,
                    time_fields=self.time_rain, file_fields=self.fields_rain, registry_fields=data_registry)

                # get air temperature dataframe
                dframe_airt = self.get_obj_datasets(
                    file_path_src_airt_point,
                    file_format=self.format_airt, file_delimiter=self.delimiter_airt, file_mandatory=True,
                    time_fields=self.time_airt, file_fields=self.fields_airt, registry_fields=data_registry)

                # get soil moisture dataframe
                dframe_sm = self.get_obj_datasets(
                    file_path_src_sm_point,
                    file_format=self.format_sm, file_delimiter=self.delimiter_sm, file_mandatory=False,
                    time_fields=self.time_sm, file_fields=self.fields_sm, registry_fields=data_registry)

                # create combined dataframe
                dframe_combined = combine_data_point_by_time(
                    dframe_k1=dframe_rain, dframe_k2=dframe_airt, dframe_k3=dframe_sm)

                # check combined dataframe
                if dframe_combined is not None:

                    # dump combined dataframe
                    self.dump_obj_datasets(
                        file_path_dst_point, dframe_combined, file_format=self.format_dst,
                        file_fields=self.fields_dst, time_fields=self.time_dst, registry_fields=data_registry)

                    # store file path
                    obj_collections[point_tag] = file_path_dst_point

                    # info point end
                    log_stream.info(' -----> Point -- (1) Name: "' + point_tag + '" :: (2) Tag: "' + point_tag +
                                    '" ... DONE')
                else:
                    log_stream.info(' -----> Point -- (1) Name: "' + point_tag + '" :: (2) Tag: "' + point_tag +
                                    '" ... SKIPPED. Datasets not available')

            else:

                # store file path
                obj_collections[point_tag] = file_path_dst_point

                # info point end
                log_stream.info(' -----> Point -- (1) Name: "' + point_tag + '" :: (2) Tag: "' + point_tag +
                                '" ... SKIPPED. Datasets previously saved')

        # check if datasets are available
        if not obj_collections:
            log_stream.warning(' ===> All datasets are not available. Check your data source(s)')
            obj_collections = None

        # method end info
        log_stream.info(' ----> Organize data dynamic object(s) ... DONE')

        return obj_collections
    # -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
