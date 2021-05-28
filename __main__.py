import os
import shutil
import time
import threading

directory_filter = [".git", ".hg"]
file_extension_filter_list = [".gdoc", ".gsheet"]

class Stats:
    files_copied = 0
    files_skipped = 0
    file_errors = 0
    filtered = 0
    end = False


def thread_function(stats):

    print("Starting")
    while not stats.end:
        time.sleep(3)
        print(f"Copied: {stats.files_copied:,}, Skipped: {stats.files_skipped:,}, Filtered: {stats.filtered}, Errors: {stats.file_errors}")


def sync_directory(source_path, destination_path, stats):
    try:
        source_path_entries = os.listdir(source_path)
    except Exception as e:
        print(f"Unable to get directory listing for {source_path}.", e)
        stats.file_errors += 1
        return
    try:
        destination_path_entries = os.listdir(destination_path)
    except Exception as e:
        print(f"Unable to get directory listing for {source_path}.", e)
        stats.file_errors += 1
        return

    for directory_entry in source_path_entries:
        source_full_path = os.path.join(source_path, directory_entry)
        destination_full_path = os.path.join(destination_path, directory_entry)

        # --- Files
        if os.path.isfile(source_full_path):

            filtered = False
            for file_extension_filter in file_extension_filter_list:
                if source_full_path.endswith(file_extension_filter):
                    filtered = True
                    break

            if filtered:
                stats.filtered += 1
                continue

            source_size = os.path.getsize(source_full_path)
            source_time = os.path.getmtime(source_full_path)

            copy = False
            if directory_entry in destination_path_entries:
                # print(f"Exists: {directory_entry}")

                try:
                    destination_size = os.path.getsize(destination_full_path)
                    destination_time = os.path.getmtime(destination_full_path)

                    if source_size != destination_size:
                        print(f"Different size {source_size:,} != {destination_size:,}, copying {source_full_path}")
                        copy = True
                    if abs(source_time - destination_time) > 5.0:
                        print(f"Different time {source_time} != {destination_time}, copying {source_full_path}")
                        copy = True
                except FileNotFoundError:
                    print(f"Error - Can't fine {destination_full_path}")
                    copy = True
            else:
                print(f"Missing: {source_full_path}")
                copy = True

            if copy:
                try:
                    shutil.copy2(source_full_path, destination_full_path)
                    stats.files_copied += 1
                except Exception as e:
                    print(f"Error copying {e}")
                    stats.file_errors += 1
            else:
                stats.files_skipped += 1

        # --- Directories
        else:
            if directory_entry not in directory_filter:
                source_time = os.path.getmtime(source_full_path)

                if directory_entry not in destination_path_entries:
                    print(f"Directory does not exist {destination_full_path}")
                    os.mkdir(destination_full_path)
                    os.utime(destination_full_path, (source_time, source_time))

                sync_directory(source_full_path, destination_full_path, stats)
            else:
                # print(f"Filtered {destination_full_path}")
                stats.filtered += 1


def main():
    # source_path = "G:/My Drive"
    # destination_path = "G:/backup/My Drive"
    source_path = "G:/My Drive/"
    destination_path = "D:/backup/My Drive/"
    # destination_path = "C:/Users/paul.craven/OneDrive"

    # source_path = "test_source"
    # destination_path = "test_backup"

    stats = Stats()
    x = threading.Thread(target=thread_function, args=(stats,))
    x.start()
    sync_directory(source_path, destination_path, stats)
    print("Done")
    stats.end = True


main()