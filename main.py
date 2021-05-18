

# # from factories.data_to_file_factory import DataToFileFactory
# from factories.factory import DataToFileFactory
# from factories.db_connection_factory import DbConnectionFactory
#
# # query_content_vertica = """SELECT dima_name from dima_marketer"""
# query_content_mysql = """select * from carf_card_availalbe_in"""
# # query_2 = query_content_vertica + """ limit 20"""
# query_3 = query_content_mysql + """ limit 20"""
# mysql_conn = DbConnectionFactory.get_db_connection('mysql')
# excel_example = DataToFileFactory.get_data_to_file_handler('excel')
# temp_result, column_list = mysql_conn.run_query(query_3)
# excel_example.data_to_file(temp_result, column_list)
#
# # t = VerticaConnection()
# # temp_result, column_list = t.run_query(query_2)
# # t2 = ExcelFile()
# # t2.data_to_file(temp_result, column_list)
