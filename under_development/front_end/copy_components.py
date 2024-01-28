import os
import shutil
from time import sleep


SOURCE_DIR = "./chemical-ur/src/components"
DESTINATION_DIR = "./chemical-create/src/components"
PERIOD = 3


source_dict = dict()

while True:
    old_source_set = set(source_dict)
    source_list = os.listdir(SOURCE_DIR)
    actual_source_set = set(source_list)
    new_files = actual_source_set - old_source_set
    deleted_files = old_source_set - actual_source_set
    
    for file_name in new_files:
        full_path_to_source = os.path.join(SOURCE_DIR, file_name)
        full_path_to_destination = os.path.join(DESTINATION_DIR, file_name)
        shutil.copyfile(full_path_to_source, full_path_to_destination)
        source_dict[file_name] = os.path.getmtime(full_path_to_source)

    for file_name in deleted_files:
        full_path_to_destination = os.path.join(DESTINATION_DIR, file_name)
        if os.path.exists(full_path_to_destination):
            os.remove(full_path_to_destination)
        del sounce_dict[file_name]

    for file_name in source_dict:
        modification_time = source_dict[file_name]
        source_path = os.path.join(SOURCE_DIR, file_name)
        new_modification_time = os.path.getmtime(source_path)
        if new_modification_time != modification_time:
            destination_path = os.path.join(DESTINATION_DIR, file_name)
            shutil.copyfile(source_path, destination_path)
            source_dict[file_name] = new_modification_time
    sleep(PERIOD)
