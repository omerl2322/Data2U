import logging

from sqlalchemy import create_engine, Column, String
from sqlalchemy import exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import Integer

from models import db_url_value, traffic_table_name
from models.os_functions import program_ends

# setting logging variable -----------------------------------------------
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

Base = declarative_base()


# ------------------------------------------------------------------------------------------------------

class TrafficRow(Base):
    __tablename__ = traffic_table_name
    id = Column(Integer, primary_key=True, autoincrement=True)
    stats_date = Column(String)
    report_id = Column(Integer)
    report_name = Column(String(100))
    scheduler_type = Column(String(15))
    delivery_status = Column(String(20))
    delivery_method = Column(String(15))
    report_duration_sec = Column(Integer)
    execution_message = Column(String)


# ------------------------------------------------------------------------------------------------------
def insert_traffic_row(report, row_timestamp):
    log.info(f'insert_traffic_row for report: {report.id}, row_timestamp: {row_timestamp}')
    try:
        engine = create_engine(db_url_value, echo=True, pool_recycle=1800)
        Session = sessionmaker(bind=engine)
        session = Session()
        traffic_row = TrafficRow(stats_date=row_timestamp,
                                 report_id=report.id, report_name=report.report_name,
                                 scheduler_type=report.scheduler_type, delivery_method='', delivery_status='',
                                 report_duration_sec=0, execution_message='')
        session.add(traffic_row)
        session.commit()
    except exc.SQLAlchemyError as e:
        log.error(f'there was an error with insert_traffic_row method: {e}')
        program_ends()
