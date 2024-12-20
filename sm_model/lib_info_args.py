"""
Library Features:

Name:          lib_info_args
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20241018'
Version:       '1.5.0'
"""

# -------------------------------------------------------------------------------------
# Library
import pandas as pd
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# time information
time_type = 'GMT'  # 'GMT', 'local'
time_units = 'days since 1970-01-01 00:00:00'
time_calendar = 'gregorian'
time_format_datasets = "%Y%m%d%H%M"
time_format_algorithm = '%Y-%m-%d %H:%M'
time_machine = pd.Timestamp.now

# log information
logger_name = 'sm_model_logger'
logger_file = 'sm_model_log.txt'
logger_handle = 'file'  # 'file' or 'stream'
logger_format = '%(asctime)s %(name)-12s %(levelname)-8s ' \
                '%(message)-80s %(filename)s:[%(lineno)-6s - %(funcName)-20s()] '

# definition of wkt for projections
proj_wkt = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,' \
           'AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],' \
           'UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]]'
proj_epsg = 'EPSG:4326'

# definition of time and geographical variables, coords and dims
time_var_name = 'time'
time_coord_name = 'time'
time_dim_name = 'time'
geo_var_name_x, geo_var_name_y = 'longitude', 'latitude'
geo_coord_name_x, geo_coord_name_y = 'longitude', 'latitude'
geo_dim_name_x, geo_dim_name_y = 'longitude', 'latitude'

# definition of crs
crs_epsg_code = 4326
crs_grid_mapping_name = "latitude_longitude"
crs_longitude_of_prime_meridian = 0.0
crs_semi_major_axis = 6378137.0
crs_inverse_flattening = 298.257223563

# definition of zip extension
zip_extension = '.gz'

# definition of file information
file_conventions = "CF-1.7"
file_title = "SM Model Product"
file_institution = "CIMA Research Foundation - www.cimafoundation.org"
file_web_site = ""
file_source = "Python library developed by CIMA Research Foundation"
file_history = "1.0.0 [20241018]"
file_references = "http://cf-pcmdi.llnl.gov/ ; http://cf-pcmdi.llnl.gov/documents/cf-standard-names/"
file_comment = "Author(s): Fabio Delogu"
file_email = "fabio.delogu@cimafoundation.org"
file_project_info = ""
file_algorithm = "Processing tool developed by CNR-IRPI for the SM model"
# -------------------------------------------------------------------------------------
