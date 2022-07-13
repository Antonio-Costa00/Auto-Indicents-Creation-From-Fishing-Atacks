import os

from O365 import Account, FileSystemTokenBackend


def get_account_access(
    app_id: str,
    app_secret: str,
    token_path: str,
    token_filename: str,
    tenant_id: str,
):
    """
    Get an access token for the user's account.
    """

    credentials = (app_id, app_secret)

    token_backend = FileSystemTokenBackend(token_path, token_filename)
    account = Account(
        credentials,
        auth_flow_type="authorization",
        token_backend=token_backend,
        tenant_id=tenant_id,
    )

    try:
        is_token_exists = os.path.isfile(f"{token_path}/{token_filename}")
        if is_token_exists:
            return account
        account.authenticate(scopes=["basic", "message_all"])
        return account
    except Exception:
        os.remove(f"{token_path}/{token_filename}")
