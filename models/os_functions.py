import logging
import os
import shutil

# setting logging variable t -------------------------------------------------------------------------------------------
from models import storage_path

# ----------------------------------------------------------------------------------------------------------------------


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


# ----------------------------------------------------------------------------------------------------------------------
def change_dir(statement):
    print(os.getcwd())
    os.chdir(statement)
    print(os.getcwd())


# ----------------------------------------------------------------------------------------------------------------------
# get the number of files in dir
def get_number_of_files_in_dir(dir_name):
    count = 0
    for path in os.listdir(dir_name):
        if os.path.isfile(os.path.join(dir_name, path)):
            count += 1
    return count


# ----------------------------------------------------------------------------------------------------------------------
def get_files_names(dir_name):
    return os.listdir(storage_path + dir_name)


# ----------------------------------------------------------------------------------------------------------------------
def create_folder(report):
    log.info(f'create_folder for: {report.folder_name}')
    path = 'storage/' + report.folder_name
    print(os.getcwd())
    try:
        os.mkdir(path)
    except OSError as e:
        log.error("creation of the directory %s failed" % path)
        error_message = 'there was an error with create_folder method :' + str(e)
        report.update_report_state(status='failed', execution_message=error_message)
        program_ends(report.folder_name)


# ----------------------------------------------------------------------------------------------------------------------
def delete_folder(report):
    log.info(f'delete_folder: {report.folder_name}')
    path = 'storage/' + report.folder_name
    try:
        shutil.rmtree(path)
    except OSError as e:
        log.error("deletion of the directory %s failed" % path)
        error_message = 'there was an error with delete_folder method :' + str(e)
        report.update_report_state(status='failed', execution_message=error_message)


# ----------------------------------------------------------------------------------------------------------------------
def program_ends(report=None):
    if report is not None:
        delete_folder(report)
    log.info('program ends')
    exit()
