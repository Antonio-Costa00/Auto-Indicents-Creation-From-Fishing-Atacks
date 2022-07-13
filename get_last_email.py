import time
from datetime import datetime


def get_last_email(account) -> dict:
    """
    It checks for new emails, comparing the total_mails_bfr and total_mails_new_check and returns the last email's details as a dictionary

    :param account: The authtenticate account
    :return: A dictionary with the last email details
    """

    try:
        mail_box = account.mailbox()
        mails_list = list(mail_box.get_messages())
        total_mails_bfr = len(mails_list)
    except Exception as e:
        raise Exception(f"Failed to get mail box: {e}")
    while True:
        mail_box = account.mailbox()
        mails_list = list(mail_box.get_messages())
        mails_new_check = mails_list
        total_mails_new_check = len(mails_new_check)
        last_mail = mails_new_check[0]
        if total_mails_new_check == total_mails_bfr:
            time.sleep(0.1)
            continue
        last_mail = mails_new_check[0]
        separator = ", "
        mail_ccs = separator.join((str(cc) for cc in last_mail.cc))
        mail_tos = separator.join((str(to) for to in last_mail.to))
        formatted_date_last_email = str(
            datetime.strftime(last_mail.sent, "%d/%m/%Y %H:%M:%S")
        )
        last_mail_details = {
            "De": last_mail.sender,
            "Enviada em": formatted_date_last_email,
            "Para": mail_tos,
            "CC": mail_ccs,
            "Assunto": last_mail.subject,
            "Conteudo": last_mail.body_preview,
        }
        return last_mail_details
