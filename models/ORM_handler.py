import datetime
import logging
from datetime import datetime
from operator import and_

from sqlalchemy import create_engine, MetaData
from sqlalchemy import exc
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

from models import db_url_value, db_tables
from models.os_functions import program_ends
# ------------------------------------------------------------------------------------------------------
from models.traffic_row import insert_traffic_row

# setting logging variable -----------------------------------------------
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


# ------------------------------------------------------------------------------------------------------
def get_session():
    log.info('get session ORM')
    try:
        engine = create_engine(db_url_value, echo=False, pool_recycle=1800)
        metadata = MetaData()
        metadata.reflect(engine, only=db_tables)
        Base = automap_base(metadata=metadata)
        Base.prepare()
        session = Session(engine)
        return Base, session
    except exc.SQLAlchemyError as e:
        log.error(f'there was an error with get_session method: {e}')
        program_ends()


# ------------------------------------------------------------------------------------------------------
def get_traffic_row_number(report_id, timestamp):
    log.info(f'get_traffic_row_number for report: {report_id} and timestamp: {timestamp}')
    try:
        Base, session = get_session()
        report_traffic_table = Base.classes.push_report_traffic
        result = session.query(report_traffic_table).filter(
            and_(report_traffic_table.report_id == report_id,
                 report_traffic_table.stats_date == timestamp)).all()
        if result[0].id is None or result[0].id == '':
            # return_status_code('can not find traffic row for report, please check db', 404)
            raise exc.SQLAlchemyError('can not get traffic row, check your traffic row')
        return result[0].id
    except exc.SQLAlchemyError as e:
        log.error(f'there was an error with get_traffic_row_number method: {e}')
        program_ends()


# ------------------------------------------------------------------------------------------------------
def get_report_details(report_id):
    log.info(f'get_report_details for report: {report_id}')
    try:
        Base, session = get_session()
        reports_details_table = Base.classes.push_report_details
        result = session.query(reports_details_table).filter(and_(reports_details_table.id == report_id,
                                                                  reports_details_table.report_status == 'Active')).all()
        if result[0] is None or result[0] == '':
            raise exc.SQLAlchemyError('can not get_report_details, check report id')
        return result[0]
    except exc.SQLAlchemyError as e:
        log.error(f'there was an error with get_report_details method: {e}')
        program_ends()


# ------------------------------------------------------------------------------------------------------
def get_queries_details(report):
    report_id = report.report_details.id
    log.info(f'get_queries_details for report: {report_id}')
    try:
        Base, session = get_session()
        queries_details_table = Base.classes.push_report_queries
        result = session.query(queries_details_table).filter(and_(queries_details_table.report_id == report_id,
                                                                  queries_details_table.query_status == 'Active')).all()
        if result is None or result == '':
            raise exc.SQLAlchemyError('can not get_queries_details, check your queries')
        return result
    except exc.SQLAlchemyError as e:
        log.error(f'there was an error with get_queries_details method: {e}')
        report.update_report_state(status='failed', execution_message=e)
        program_ends()


# ------------------------------------------------------------------------------------------------------
def update_while_running_traffic_row(report):
    log.info(f'update_while_running_traffic_row for traffic row: {report.traffic_row}')
    try:
        Base, session = get_session()
        report_traffic_table = Base.classes.push_report_traffic
        result = session.query(report_traffic_table).filter(report_traffic_table.id == report.traffic_row).all()
        result[0].delivery_status = report.delivery_status
        result[0].execution_message = report.execution_message
        result[0].report_duration_sec = report.timer.duration
        session.commit()
    except exc.SQLAlchemyError as e:
        log.error(f'there was an error with update_while_running_traffic_row method: {e}')
        program_ends(report.folder_name)


# ------------------------------------------------------------------------------------------------------
def get_reports_for_time_frame(time_frame):
    log.info(f'get_reports_for_time_frame for time frame: {time_frame}')
    try:
        Base, session = get_session()
        reports_details_table = Base.classes.push_report_details
        result = session.query(reports_details_table).filter(and_(reports_details_table.scheduler_type == time_frame,
                                                                  reports_details_table.report_status == 'Active')).all()
        if result is None or result == '':
            raise exc.SQLAlchemyError('can not get_reports_for_time_frame, check your time_frame')
        return result
    except exc.SQLAlchemyError as e:
        log.error(f'there was an error with get_reports_for_time_frame method: {e}')
        program_ends()


# ------------------------------------------------------------------------------------------------------
def create_traffic_rows(time_frame_reports):
    log.info('create_traffic_rows for reports in time frame')
    reports = []
    for report in time_frame_reports:
        report_id = report.id
        row_timestamp = datetime.now().replace(microsecond=0)
        traffic_data = (report_id, row_timestamp)
        insert_traffic_row(report, row_timestamp)
        reports.append(traffic_data)
    return reports
