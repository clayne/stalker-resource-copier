import os
import shutil
import time

from . import const


LOG_FILE_NAME = 'stalker_resource_copier.log'
ALL_COPIED = 'All files are copied.'
MISSIGNG_FILES = 'These files are not copied because they are missing:\n\n'


def read_file(path):
    with open(path, 'rb') as file:
        data = file.read()
    return data


def copy_file(src, output, missing_files):
    if os.path.exists(src):
        out_dir_name = os.path.dirname(output.lower())
        if not os.path.exists(out_dir_name):
            os.makedirs(out_dir_name)
        shutil.copyfile(src, output.lower())

    else:
        missing_files.add(src)


def write_log(missing_files):
    missing_files = list(missing_files)
    missing_files.sort()

    log_lines = []
    if len(missing_files):
        log_lines.append(MISSIGNG_FILES)
        for file in missing_files:
            log_lines.append('{}\n'.format(file))

    else:
        log_lines.append(ALL_COPIED)

    with open(LOG_FILE_NAME, 'w', encoding='utf-8') as log_file:
        for log_line in log_lines:
            log_file.write(log_line)


def report_total_time(status_label, start_time):
    end_time = time.time()
    total_time = end_time - start_time
    total_time_str = 'total time:    {} sec'.format(round(total_time, 2))
    status_label.configure(text=total_time_str, bg=const.LABEL_COLOR)
