import os
import shutil

def sync_directory(source_path, destination_path):
    source_path_entries = os.listdir(source_path)
    destination_path_entries = os.listdir(destination_path)

    for directory_entry in source_path_entries:
        source_full_path = os.path.join(source_path, directory_entry)
        destination_full_path = os.path.join(destination_path, directory_entry)

        # --- Files
        if os.path.isfile(source_full_path):
            source_size = os.path.getsize(source_full_path)
            source_time = os.path.getmtime(source_full_path)

            copy = False
            if directory_entry in destination_path_entries:
                print(f"Exists: {directory_entry}")

                destination_size = os.path.getsize(destination_full_path)
                destination_time = os.path.getmtime(destination_full_path)

                if source_size == destination_size and source_time == destination_time:
                    print("Same, skipping.")
                else:
                    print("Different, copying")
                    copy = True
            else:
                print(f"Missing: {directory_entry}")
                copy = True
            if copy:
                shutil.copy2(source_full_path, destination_full_path)

        # --- Directories
        else:
            source_time = os.path.getmtime(source_full_path)

            if directory_entry in destination_path_entries:
                print("Directory exists")
            else:
                print("Directory does not exist")
                os.mkdir(destination_full_path)
                os.utime(destination_full_path, (source_time, source_time))


def main():
    # source_path = "G:/My Drive"
    # destination_path = "H:/backup/My Drive"
    source_path = "G:/My Drive/U of Idaho/2006 CS501"
    destination_path = "H:/backup/My Drive/U of Idaho/2006 CS501"

    # source_path = "test_source"
    # destination_path = "test_backup"

    sync_directory(source_path, destination_path)

main()