import logging

import pandas as pd

from interfaces.file import File
# ------------------------------------------------------------------------------------------------------
from models import storage_path
from models.os_functions import program_ends

# setting logging variable -----------------------------------------------
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class CsvFile(File):

    def data_to_file(self, report):
        log.info('data_to_file: csv file')
        queries = report.queries
        folder_path = storage_path + report.folder_name + '/'
        for query in queries:
            try:
                data, column_names = query.connection_type.run_query(query.query_content)
                file_name = query.queries_details.query_name
                path = folder_path + file_name
                # check if the data list is empty
                if not data:
                    log.error(f'the query id : {query.queries_details.id} does not return any data')
                    continue
                result_df = pd.DataFrame(data)
                result_df.to_csv(path + '.csv', index=False, header=column_names)
            except Exception as e:
                report.update_report_state(status='failed', execution_message=e)
                log.error(f'there was an error with report : {report.report_details.id} : {e}')
                program_ends(report)
