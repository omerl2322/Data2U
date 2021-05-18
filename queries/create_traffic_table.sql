
CREATE TABLE faprt_push_report_traffic_test (
    faprt_id INT NOT NULL auto_increment primary key,
    faprt_stats_date datetime not null,
    faprt_report_id int not null,
    faprt_report_name varchar(100),
    faprt_scheduler_type varchar(15),
    faprt_delivery_status varchar(10),
    faprt_delivery_method varchar(15),
    faprt_report_duration time,
    faprt_execution_message varchar(2000)
);

select * from faprt_push_report_traffic_test
limit 20