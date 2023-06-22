#!/bin/bash

#-----------------------------------------------------------------------------------------
# Script information
script_name="HYDE UTILS - MANAGER DATASETS - HMC - STORAGE - REALTIME"
script_version="1.0.0"
script_date="2021/02/22"
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Get script information
script_file="hyde_tools_manager_datasets_hmc_storage.sh"

# Get time information (-u to get gmt time)
time_script_now=$(date -u +"%Y-%m-%d 00:00")
#time_script_now="2021-02-20 00:00"

time_script_period=3
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Folder of remote and local machine(s)
group_datasets_name=(
    "DYNAMIC DATA - EXPERT FORECAST 2017 - RAIN"
    "DYNAMIC DATA - EXPERT FORECAST 2009 - RAIN"
)

group_folder_datasets_source_raw=(
    "/hydro/data/data_dynamic/source/subjective-forecast_aa2017/" 
    "/hydro/data/data_dynamic/source/subjective-forecast_aa2009/" 
)

group_folder_datasets_destination_raw=(
    "/hydro/storage/subjective-forecast_aa2017/%YYYY/%mm/"
    "/hydro/storage/subjective-forecast_aa2009/%YYYY/%mm/" 
)

group_file_datasets_pattern_raw=(
	"%YYYY-%mm-%dd_dati_prev.csv"
	"%YYYY-%mm-%dd_dati_prev.csv"
)

group_file_datasets_sync=(
    true
    false
)

group_file_datasets_latency=(
    15
    15
)

group_file_datasets_period=(
    15
    0
)
#-----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# Info script start
echo " ==================================================================================="
echo " ==> "$script_name" (Version: "$script_version" Release_Date: "$script_date")"
echo " ==> START ..."
echo " ===> EXECUTION ..."

time_script_now=$(date -d "$time_script_now" +'%Y-%m-%d 00:00')
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# Iterate over tags
for datasets_id in "${!group_datasets_name[@]}"; do

	# ----------------------------------------------------------------------------------------
	# Get values of tag(s) and folder(s)        
	datasets_name=${group_datasets_name[datasets_id]}
	
	folder_datasets_source_raw=${group_folder_datasets_source_raw[datasets_id]}
	folder_datasets_destination_raw=${group_folder_datasets_destination_raw[datasets_id]}
	
	file_datasets_pattern_raw=${group_file_datasets_pattern_raw[datasets_id]} 

	file_datasets_sync=${group_file_datasets_sync[datasets_id]}
	file_datasets_frequency=${group_file_datasets_frequency[datasets_id]}
	
	file_datasets_latency=${group_file_datasets_latency[datasets_id]}
	file_datasets_period=${group_file_datasets_period[datasets_id]}
	
	# Info datasets type start
	echo " ====> DATASETS TYPE ${datasets_name} ... "
	# ----------------------------------------------------------------------------------------
	
	# ----------------------------------------------------------------------------------------
	# Check sync activation
	if ${file_datasets_sync} ; then
		
		# ----------------------------------------------------------------------------------------
		# Get time latency information
		time_script_latency=$(date -d "$time_script_now ${file_datasets_latency} days ago" +'%Y-%m-%d 00:00')
		# ----------------------------------------------------------------------------------------
		
		# ----------------------------------------------------------------------------------------
		# Iterate over datasets period
		for file_datasets_step in $(seq 0 $file_datasets_period); do
			
			# ----------------------------------------------------------------------------------------
			time_step=$(date -d "$time_script_latency ${file_datasets_step} days ago" +'%Y-%m-%d 00:00')
			year_step=$(date -u -d "$time_step" +"%Y")
			month_step=$(date -u -d "$time_step" +"%m")
			day_step=$(date -u -d "$time_step" +"%d")
			hour_step=$(date -u -d "$time_step" +"%H")
			minute_step=$(date -u -d "$time_step" +"%M")
			
			# Info time step start
			echo " =====> TIME STEP ${time_step} ... "
			# ----------------------------------------------------------------------------------------
			
		    # ----------------------------------------------------------------------------------------
		    # Define remote and local folder(s)
		    folder_datasets_source_step=${folder_datasets_source_raw/'%YYYY'/$year_step}
		    folder_datasets_source_step=${folder_datasets_source_step/'%mm'/$month_step}
		    folder_datasets_source_step=${folder_datasets_source_step/'%dd'/$day_step}
		    folder_datasets_source_step=${folder_datasets_source_step/'%HH'/$hour_step}
		    folder_datasets_source_step=${folder_datasets_source_step/'%MM'/$minute_step}
		    
		    folder_datasets_destination_step=${folder_datasets_destination_raw/'%YYYY'/$year_step}
		    folder_datasets_destination_step=${folder_datasets_destination_step/'%mm'/$month_step}
		    folder_datasets_destination_step=${folder_datasets_destination_step/'%dd'/$day_step}
		    folder_datasets_destination_step=${folder_datasets_destination_step/'%HH'/$hour_step}
		    folder_datasets_destination_step=${folder_datasets_destination_step/'%MM'/$minute_step}
		    
		    # Define filename
		    file_datasets_pattern_step=${file_datasets_pattern_raw/'%YYYY'/$year_step}
		    file_datasets_pattern_step=${file_datasets_pattern_step/'%mm'/$month_step}
		    file_datasets_pattern_step=${file_datasets_pattern_step/'%dd'/$day_step}
		    file_datasets_pattern_step=${file_datasets_pattern_step/'%HH'/$hour_step}
		    file_datasets_pattern_step=${file_datasets_pattern_step/'%MM'/$minute_step}
			# ----------------------------------------------------------------------------------------

			# ----------------------------------------------------------------------------------------
			# Sync file from source to destination folders
			echo " ======> SYNC FILE ${file_datasets_pattern_step} ... "
			
			path_datasets_source_step=${folder_datasets_source_step}${file_datasets_pattern_step} 
			path_datasets_destination_step=${folder_datasets_destination_step}${file_datasets_pattern_step}

			cmd_sync="rsync -rtv --progress ${path_datasets_source_step} ${path_datasets_destination_step}"
				
			if [ -d "$folder_datasets_source_step" ]; then
				
				if [ -f $path_datasets_source_step ]; then
				
					# Create local folder
					if [ ! -d "$folder_datasets_destination_step" ]; then
						mkdir -p $folder_datasets_destination_step
					fi
					
					# Execute command-line
					if ! ${cmd_sync} ; then
						# Info tag end (failed)
						echo " ======> SYNC FILE ${file_datasets_pattern_step} ... FAILED. ERRORS IN EXECUTING $cmd_sync COMMAND-LINE"
					else
						# Info tag end (completed)
						echo " ======> SYNC FILE ${file_datasets_pattern_step} ... DONE"
					fi
					
					echo " ======> REMOVE FILE FROM SOURCE ${file_datasets_pattern_step} ... "
					if  [[ -f $path_datasets_source_step && -f $path_datasets_destination_step ]]; then
	   					rm $path_datasets_source_step
	   					echo " ======> REMOVE FILE FROM SOURCE ${file_datasets_pattern_step} ... DONE"
					else
	   					echo " ======> REMOVE FILE FROM SOURCE ${file_datasets_pattern_step} ... SKIPPED. Source and/or destination file is/are unavailable"
					fi
					
					echo " ======> CHECK DESTINATION FOLDER $folder_datasets_destination_step ... "
					if [ "$(ls -A $folder_datasets_destination_step)" ]; then
						echo " ======> CHECK DESTINATION FOLDER $folder_datasets_destination_step ... NOT EMPTY"
					else
						echo " ======> CHECK DESTINATION FOLDER $folder_datasets_destination_step ... EMPTY. REMOVE FOLDER"
						rm -rf $folder_datasets_destination_step
					fi
				
				else
					# Source file does not exist
					echo " ======> SYNC FILE ${file_datasets_pattern_step} ... FAILED. SOURCE FILE $file_datasets_pattern_step DOES NOT EXIST"
				fi
				
			else
				# Source folder does not exist
				echo " ======> SYNC FILE ${file_datasets_pattern_step} ... FAILED. SOURCE FOLDER $folder_datasets_source_step DOES NOT EXIST"
			fi

			# ----------------------------------------------------------------------------------------
				
			# ----------------------------------------------------------------------------------------
			# Info time step end
			echo " =====> TIME STEP ${time_step} ... DONE"
			# ----------------------------------------------------------------------------------------
			
		done
	
		# Info datasets type end
		echo " ====> DATASETS TYPE ${datasets_name} ... DONE"
		# ----------------------------------------------------------------------------------------
		
	else
	
		# ----------------------------------------------------------------------------------------
		# Info tag end (not activated)
		echo " ====> DATASETS TYPE ${datasets_name} ... SKIPPED. SYNC NOT ACTIVATED"
		# ----------------------------------------------------------------------------------------
		
	fi
	# ----------------------------------------------------------------------------------------
	
done
# ----------------------------------------------------------------------------------------

# Info script end
echo " ==> ... END"
echo " ==> Bye, Bye"
echo " ==================================================================================="
# ----------------------------------------------------------------------------------------





