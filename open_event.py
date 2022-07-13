import requests
from flatten_dict import flatten, unflatten
from format_mail import format_mail


def open_event(
    json_data: dict, mail_details: dict, session_token: str, url: str
) -> dict:
    """
    It takes a json_data dict, a mail_details dict and a session_token string as arguments, open a ArcherEvent with mail_details returns
    a json response

    :param json_data: dict = The json data that is returned from the get_json_data function
    :type json_data: dict
    :param mail_details: a dictionary containing the subject and body of the email
    :type mail_details: dict
    :param session_token: The session token that you get from the login function
    :type session_token: str
    :param url: The url of the Archer Endpoint
    :type url: str
    :return: A dict json format response
    """

    event_desc_formatted = format_mail(mail_details)
    url = f"{url}/platformapi/core/content"
    # Flatten function necessary to update the dict request with correct parameters from json_file
    flatten_json_data = flatten(json_data)
    # Set session token in the request header
    flatten_json_data[
        ("OpenEventHeaders", "Authorization")
    ] = f"Archer session-id={session_token}"
    # Development, homologation and production ids are different, so we need to get the correct ids in the json file
    title_id = list(json_data["OpenEventParameters"]["Content"]["FieldContents"])[0]
    incident_desc_id = list(
        json_data["OpenEventParameters"]["Content"]["FieldContents"]
    )[1]
    # Event title
    mail_subject = mail_details["Assunto"]
    flatten_json_data[
        ("OpenEventParameters", "Content", "FieldContents", title_id, "Value")
    ] = f"ABUSE - {mail_subject}"
    # Event description
    flatten_json_data[
        ("OpenEventParameters", "Content", "FieldContents", incident_desc_id, "Value")
    ] = event_desc_formatted
    json_data = unflatten(flatten_json_data)
    body = json_data["OpenEventParameters"]
    headers = json_data["OpenEventHeaders"]
    try:
        request = requests.post(url, json=body, headers=headers)
        response = request.json()
        try:
            event_id = response["RequestedObject"]["Id"]
            print(f"Aberto evento {event_id}")
            return response
        except KeyError:
            return response
    except requests.exceptions.ConnectionError as e:
        raise ValueError(f"Erro na Requisicao: {e}")
