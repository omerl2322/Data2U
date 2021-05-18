import logging
from datetime import date

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from sendgrid.helpers.mail import Mail, To, Content, Email, Attachment, FileContent, FileName, Disposition, ContentId

from interfaces.delivery_method import DeliveryMethod
from interfaces.file import File
from models import from_email_value, sendgrid_api_key, email_template_name, resources_path, storage_path, \
    email_template_name_outside_ob
# ------------------------------------------------------------------------------------------------------
from models.os_functions import get_files_names, program_ends

# setting logging variable -----------------------------------------------
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def check_template(recipient_list):
    for recipient_address in recipient_list:
        if '@outbrain.com' not in recipient_address:
            return email_template_name_outside_ob
    return email_template_name


class ViaEmail(DeliveryMethod):

    def send_report(self, report):
        log.info('send_report via email')
        try:
            recipient_list = str(report.report_details.mailing_list).split(',')
            template_name = check_template(recipient_list)
            if len(recipient_list) == 0:
                raise Exception('recipient_list is empty')
            for recipient_address in recipient_list:
                email_obj = build_email(report, recipient_address, template_name)
                add_attachments(email_obj, report.folder_name)
                sendgrid_client = SendGridAPIClient(sendgrid_api_key)
                response = sendgrid_client.send(email_obj)
        except Exception as e:
            log.error(f'There was an issue with send_report via email method: {e}')
            report.update_report_state(status='failed', execution_message=e)
            program_ends(report)

    # ------------------------------------------------------------------------------------------------------


def build_email(report, to_email, template_name):
    email_template = get_email_template(template_name)
    if report.report_details.mail_subject != '':
        subject_value = report.report_details.mail_subject
    else:
        # subject_value = report.folder_name + " - Push report"
        subject_value = report.report_details.report_name + " - Data2U - " + str(date.today())
    return Mail(
        from_email=Email(from_email_value),
        to_emails=To(to_email),
        subject=subject_value,
        html_content=Content("text/html", email_template)
    )


def add_attachments(email_obj, folder_name):
    attachment_list = get_files_names(folder_name)
    if len(attachment_list) == 0:
        raise Exception('there are no files in ' + str(folder_name))
    attachment_id = 1
    for attachment_name in attachment_list:
        attachment_path = storage_path + folder_name + '/' + attachment_name
        attachment = Attachment()
        encoded_data = File.file_encode(attachment_path)
        attachment.file_content = FileContent(encoded_data)
        attachment.file_name = FileName(attachment_name)
        attachment.disposition = Disposition('attachment')
        attachment.content_id = ContentId(f'Attachment {str(attachment_id)}')
        email_obj.attachment = attachment
        attachment_id += 1


def get_email_template(template_name):
    with open(resources_path + str(template_name), "r") as f:
        my_template = ''
        my_template += f.read()
        my_template += ''
    return my_template
