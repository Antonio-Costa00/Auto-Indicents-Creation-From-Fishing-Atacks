import json
import os

from dotenv import load_dotenv

if __name__ == "__main__":

    from Account.get_account_access import get_account_access
    from Account.get_last_email import get_last_email
    from Archer.ArcherPlatform.auth_request import auth_request
    from Archer.ArcherPlatform.open_event import open_event
    from Archer.read_json import read_json

    load_dotenv()

    APP_ID = str(os.getenv("APP_ID"))
    APP_SECRET = str(os.getenv("APP_SECRET"))
    TENANT_ID = str(os.getenv("TENANT_ID"))
    ARCHER_URL = str(os.getenv("ARCHER_URL"))
    ARCHER_USER = str(os.getenv("ARCHER_USER"))
    INSTANCE_NAME = str(os.getenv("INSTANCE_NAME"))
    ARCHER_PASSWORD = str(os.getenv("ARCHER_PASSWORD"))
    TOKEN_PATH = "token_dir"
    TOKEN_FILENAME = "o365_token.txt"
    JSON_DATA = read_json("Archer/ArcherAPI/archer_example.json")

    # Get account access
    account = get_account_access(
        APP_ID, APP_SECRET, TOKEN_PATH, TOKEN_FILENAME, TENANT_ID
    )
    while True:
        # Get last email from box messages
        last_email = get_last_email(account)
        print(last_email)

        #  Get session token
        # session_token = auth_request(
        #     json_data, ARCHER_URL, ARCHER_USER, ARCHER_PASSWORD
        # )
        session_token = ""

        # Open event
        request = open_event(JSON_DATA, last_email, session_token, ARCHER_URL)
        print(json.dumps(request, indent=2))
