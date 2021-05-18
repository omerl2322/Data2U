import logging

import pandas as pd
from xlsxwriter.exceptions import XlsxWriterException

from interfaces.file import File
# ------------------------------------------------------------------------------------------------------
from models import storage_path
from models.os_functions import program_ends

# setting logging variable -----------------------------------------------
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class ExcelMultiTab(File):

    def data_to_file(self, report):
        log.info('data_to_file: ExcelMultiTab file')
        folder_path = storage_path + report.folder_name + '/'
        report_name = report.report_details.report_name
        path = folder_path + report_name
        writer = None
        try:
            # Create a Pandas Excel writer using XlsxWriter as the engine.
            writer = pd.ExcelWriter(path + '.xlsx', engine='xlsxwriter')
            queries = report.queries
            for query in queries:
                data, column_names = query.connection_type.run_query(query.query_content)
                # check if the data list is empty
                if not data:
                    log.error(f'the query id : {query.queries_details.id} does not return any data')
                    continue
                result_df = pd.DataFrame(data)
                sheet_name = query.queries_details.query_name
                # Write each dataframe to a different worksheet.
                result_df.to_excel(writer, sheet_name=sheet_name, header=column_names, index=False)
        except (XlsxWriterException, RuntimeError, Exception) as e:
            log.error(f'there was an error with report : {report.report_details.id} : {e}')
            report.update_report_state(status='failed', execution_message=e)
            program_ends(report)
        # Close the Pandas Excel writer and output the Excel file.
        writer.save()


# ------------------------------------------------------------------------------------------------------

class ExcelSeparateFiles(File):

    def data_to_file(self, report):
        log.info('data_to_file: ExcelSeparateFiles file')
        queries = report.queries
        folder_path = storage_path + report.folder_name + '/'
        for query in queries:
            try:
                data, column_names = query.connection_type.run_query(query.query_content)
                # check if the data list is empty
                if not data:
                    log.error(f'the query id : {query.queries_details.id} does not return any data')
                    continue
                file_name = query.queries_details.query_name
                path = folder_path + file_name
                result_df = pd.DataFrame(data)
                result_df.to_excel(path + '.xlsx', index=False, header=column_names, sheet_name=file_name)
            except Exception as e:
                log.error(f'there was an error with report : {report.report_details.id} : {e}')
                report.update_report_state(status='failed', execution_message=e)
                program_ends(report)
