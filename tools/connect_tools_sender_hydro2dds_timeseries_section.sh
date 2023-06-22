#!/bin/bash

#-----------------------------------------------------------------------------------------
# Script information
script_name='HYDE - HYDRO 2 DDS - TIMESERIES - REALTIME'
script_version="2.0.0"
script_date='2021/04/28'

# Server information
dds_host='10.198.26.22'
dds_usr='user'
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# Datasets
dset_template_list=(
	"HMC TIMESERIES SECTIONS"
)

file_template_list=(
	"hydrograph*.txt"
)

hour_template_list=(
	""
)
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# Get arguments
DATE=$(echo $1)
source_path_base=$2
dds_path_base=$3
source_path_data=$4

# Parse time parts
YEAR=$(echo $1 | cut -c1-4)
MONTH=$(echo $1 | cut -c6-7)
DAY=$(echo $1 | cut -c9-10)
HH=$(echo $1 | cut -c12-13)
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------
# Info script start
echo " ==================================================================================="
echo " ==> "$script_name" (Version: "$script_version" Release_Date: "$script_date")"
echo " ==> START ..."
echo " ===> EXECUTION ..."
echo " "
echo " ==== TIMEREF: $1 "
echo " ==== Source base path: $2 "
echo " ==== DDS base path: $3 "
echo " ==== Source base data: $4 "
echo " "
echo " ==== DATE: $DATE -- YEAR: $YEAR -- MONTH: $MONTH -- DAY: $DAY -- HOUR: $HH"
echo " "

# Iterate over tags
for datasets_id in "${!dset_template_list[@]}"; do
     
	dset_template_step=${dset_template_list[datasets_id]}
	file_template_step=${file_template_list[datasets_id]}
	hour_template_step=${hour_template_list[datasets_id]}
	
	echo " ====> DSET: $dset_template_step ... "
	
	file_name_list=$(find $source_path_base/$YEAR/$MONTH/$DAY/$HH$source_path_data/ -type f -name $file_template_step)	
	for file_name_step in ${file_name_list}; do

		echo " =====> FILENAME: $file_name_step ... "     
		
		file_name_datepart=${file_name_step##*_}
		file_name_nopath=${file_name_step##*/}
		file_name_year=$(echo $file_name_datepart | cut -c1-4)
    	file_name_month=$(echo $file_name_datepart | cut -c5-6)
    	file_name_day=$(echo $file_name_datepart | cut -c7-8)
    	
		if ! (ssh $dds_usr@$dds_host  [ -d $dds_path_base/$YEAR/$MONTH/$DAY/ ]); then
			ssh $dds_usr@$dds_host "mkdir -p $dds_path_base/$YEAR/$MONTH/$DAY/"
		fi
		
		echo " ======> SYNC, UNZIP AND CHANGE OWNER ... "  
	   	rsync -ue ssh $source_path_base/$file_name_year/$file_name_month/$file_name_day/$HH$source_path_data/$file_name_nopath $dds_usr@$dds_host:$dds_path_base/$YEAR/$MONTH/$DAY/$file_name_nopath
		ssh $dds_usr@$dds_host "chown -R user:user $dds_path_base/$file_name_year/$MONTH/$DAY"
		echo " ======> SYNC, UNZIP AND CHANGE OWNER ... DONE" 
		
		echo " =====> FILENAME: $file_name_step ... DONE" 
		
	done
	
	echo " ====> DSET: $dset_template_step ... DONE"
	
done

# Info script end
echo " ===> EXECUTION ... DONE"
echo " ==> "$script_name" (Version: "$script_version" Release_Date: "$script_date")"
echo " ==> Bye, Bye"
echo " ==================================================================================="
# ----------------------------------------------------------------------------------------


