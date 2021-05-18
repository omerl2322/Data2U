-- tests for push report new sys----------------------------------------------------------------------------------------
-- test 1---------------------------------------------------------------------------------------------------------------
-- report id = 7 - test on Vertica for two queries - different workbooks = excel - separate files
INSERT INTO faprt_push_report_traffic_test (faprt_id, faprt_stats_date, faprt_report_id, faprt_report_name, faprt_scheduler_type,
                                            faprt_delivery_status, faprt_report_duration, faprt_execution_message)
                                            VALUES (7,'2021-02-28 15:43:01',7,'SYSTEM TEST 1','single_time','started','','');

select * from faprt_push_report_traffic_test
where faprt_report_id = 7;

INSERT INTO push_report_details (id, report_name, report_type, file_type, report_status, scheduler_type, delivery_method, bi_ticket_number, mailing_list,
                                 domain_type, report_owner, ftp_name, first_send_date, mail_content, mail_subject,
                                 creator, creation_date, modified_by, modification_date)
VALUES (7,'SYSTEM TEST 1','Excel','excel - separate files','Active','Daily','Email','BI0564015','bisupport@outbrain.com,omlevi@outbrain.com',
        'Supply','Omer levy',null,'2021-02-08','','sys test','bi-platform','2021-02-04','','2021-02-11');


select * from push_report_details
where id = 7;

INSERT INTO push_report_queries (id, connection_type, report_query, query_name, query_status, creation_date, report_id)
VALUES (14,'Vertica','SELECT facm_est_stats_date, sum(facm_gross_revenue)
FROM facm_campaign_traffic_d
WHERE facm_marketer_id = 1066
AND facm_est_stats_date >= date_trunc(''month'',current_date)
AND facm_est_stats_date < current_date
GROUP BY facm_est_stats_date','test-1-1','Active','2021-02-07',7);


INSERT INTO push_report_queries (id, connection_type, report_query, query_name, query_status, creation_date, report_id)
VALUES (16,'Vertica','SELECT facm_marketer_id, sum(facm_gross_revenue)
FROM facm_campaign_traffic_d
WHERE facm_marketer_id = 2137482582
AND facm_est_stats_date >= date_trunc(''month'',current_date)
AND facm_est_stats_date < current_date
GROUP BY facm_marketer_id','test-1-2','Active','2021-02-07',7);

select * from push_report_queries
where report_id = 7;


UPDATE faprt_push_report_traffic_test
SET faprt_report_name = 'SYSTEM TEST 1'
WHERE faprt_report_id = 7


-- test 1----END--------------------------------------------------------------------------------------------------------
-- test 2---------------------------------------------------------------------------------------------------------------
# report id = 8 - test on Vertica for two queries - different workbooks = excel - multi tab
INSERT INTO faprt_push_report_traffic_test (faprt_id, faprt_stats_date, faprt_report_id, faprt_report_name,
                                            faprt_scheduler_type, faprt_delivery_status,
                                            faprt_report_duration, faprt_execution_message)
                                            VALUES (13,'2021-02-16 17:51:16',13,'SYSTEM TEST 2','single_time','started',null,null);


select * from faprt_push_report_traffic_test
where faprt_id = 8;


INSERT INTO push_report_details (id, report_name, report_type, file_type, report_status, scheduler_type, delivery_method,
                                 bi_ticket_number, mailing_list, domain_type, report_owner, ftp_name,
                                 first_send_date, mail_content, mail_subject, creator, creation_date, modified_by, modification_date)
                                 VALUES (13,'SYSTEM TEST 2','excel','excel - multi tab','Active','single_time','Email','','bisupport@outbrain.com,omlevi@outbrain.com',
                                         'Demand','Omer Levy','','2021-02-04','','','bi-platform','2021-02-04',null,'2021-02-04');


select * from push_report_details
where id = 8;

INSERT INTO push_report_queries (id, connection_type, report_query, query_name, query_status, creation_date, report_id)
VALUES (4,'Vertica','select *
from dima_marketer
limit 10','test-2-1','Active','2021-02-04',8)

INSERT INTO push_report_queries (id, connection_type, report_query, query_name, query_status, creation_date, report_id)
VALUES (6,'Vertica','select facm_marketer_id,sum(facm_budget_id) as budget,
    sum(facm_num_paid_clicks) as clicks,
    sum(facm_gross_revenue)
    as rev from facm_campaign_traffic_d
group by 1
limit 200','test-2-2','Active','2021-02-04',8);

select * from push_report_queries
where report_id = 8;

-- test 2--END----------------------------------------------------------------------------------------------------------
-- test 3---------------------------------------------------------------------------------------------------------------
# report id = 9 - test on MySql for two queries - different workbooks = excel - separate files
INSERT INTO faprt_push_report_traffic_test (faprt_id, faprt_stats_date, faprt_report_id, faprt_report_name, faprt_scheduler_type,
                                            faprt_delivery_status, faprt_report_duration, faprt_execution_message)
                                            VALUES (9,'2021-03-21 22:36:17',9,'SYSTEM TEST 3','single_time','started',null,null);



select * from faprt_push_report_traffic_test
where faprt_id = 9;


INSERT INTO push_report_details (id, report_name, report_type, file_type, report_status, scheduler_type, delivery_method,
                                 bi_ticket_number, mailing_list, domain_type, report_owner,
                                 ftp_name, first_send_date, mail_content, mail_subject, creator, creation_date, modified_by, modification_date)
                                 VALUES (9,'SYSTEM TEST 3','excel','excel - separate files','Active','single_time','Email','','bisupport@outbrain.com,omlevi@outbrain.com',
                                         'Demand','Omer Levy','','2021-02-04','','sys test','bi-platform','2021-02-04','','2021-02-04');


select * from push_report_details
where id = 9;


INSERT INTO push_report_queries (id, connection_type, report_query, query_name, query_status,
                                 creation_date, report_id)
                                 VALUES (9,'Mysql','select * from rfua_user_agent
limit 20','test-3-1','Active','2021-02-07',9);

INSERT INTO push_report_queries (id, connection_type, report_query, query_name, query_status,
                                 creation_date, report_id)
                                 VALUES (9,'Mysql','select * from pccm_campaign
limit 20','test-3-2','Active','2021-02-07',9);


select * from push_report_queries
where report_id=9;

-- test 3-----END-------------------------------------------------------------------------------------------------------
-- test 4---------------------------------------------------------------------------------------------------------------
# report id = 10 - test on MySql for two queries - different workbooks = excel - multi tab

INSERT INTO faprt_push_report_traffic_test (faprt_id, faprt_stats_date, faprt_report_id, faprt_report_name, faprt_scheduler_type,
                                            faprt_delivery_status, faprt_report_duration, faprt_execution_message)
                                            VALUES (10,'2021-03-21 22:37:03',10,'SYSTEM TEST 4','single_time','started',null,null);


select * from faprt_push_report_traffic_test
where faprt_id = 10;


INSERT INTO push_report_details (id, report_name, report_type, file_type, report_status, scheduler_type, delivery_method,
                                 bi_ticket_number, mailing_list, domain_type, report_owner,
                                 ftp_name, first_send_date, mail_content, mail_subject, creator, creation_date, modified_by, modification_date)
                                 VALUES (10,'SYSTEM TEST 4','excel','excel - multi tab','Active','single_time','Email','','bisupport@outbrain.com,omlevi@outbrain.com',
                                         'Demand','Omer Levy','','2021-02-04','','sys test','bi-platform','2021-02-04','','2021-02-04');

select * from push_report_details
where id = 10;


INSERT INTO push_report_queries (id, connection_type, report_query, query_name, query_status,
                                 creation_date, report_id)
                                 VALUES (2,'Mysql','select * from rfal_access_level_group','test-4-1','Active','2021-02-02',10);

INSERT INTO push_report_queries (id, connection_type, report_query, query_name, query_status,
                                 creation_date, report_id)
                                 VALUES (8,'Mysql','select * from pccc_currency_cpc
limit 500','test-4-2','Active','2021-02-02',10);


select * from push_report_queries
where report_id=10


-- test 4---END---------------------------------------------------------------------------------------------------------
-- test 5---------------------------------------------------------------------------------------------------------------
# report id = 11 - test on MySql for query - different workbooks = csv

INSERT INTO faprt_push_report_traffic_test (faprt_id, faprt_stats_date, faprt_report_id, faprt_report_name, faprt_scheduler_type,
                                            faprt_delivery_status, faprt_report_duration, faprt_execution_message)
                                            VALUES (11,'2021-03-21 22:40:03',11,'SYSTEM TEST 5','single_time','started',null,null);


select * from faprt_push_report_traffic_test
where faprt_id=11;

INSERT INTO push_report_details (id, report_name, report_type, file_type, report_status, scheduler_type, delivery_method,
                                 bi_ticket_number, mailing_list, domain_type, report_owner,
                                 ftp_name, first_send_date, mail_content, mail_subject, creator, creation_date, modified_by, modification_date)
                                 VALUES (11,'SYSTEM TEST 5','Csv','Csv','Active','single_time','Email','','bisupport@outbrain.com,omlevi@outbrain.com',
                                         'Demand','Omer Levy','','2021-02-04','','sys test 5','bi-platform','2021-02-04','','2021-02-04');


select * from push_report_details
where id=11;


INSERT INTO push_report_queries (id, connection_type, report_query, query_name, query_status,
                                 creation_date, report_id)
                                 VALUES (17,'Vertica','SELECT facm_est_stats_date, sum(facm_gross_revenue)
FROM facm_campaign_traffic_d
WHERE facm_marketer_id = 1066
AND facm_est_stats_date >= date_trunc(''month'',current_date)
AND facm_est_stats_date < current_date
GROUP BY facm_est_stats_date
ORDER BY 1 DESC','test-5-1','Active','2021-02-07',11);


select * from push_report_queries
where report_id=11;
-- test 5------END------------------------------------------------------------------------------------------------------

