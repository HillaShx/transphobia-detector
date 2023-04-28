import hashlib
import json
from http import HTTPStatus

import requests
from authlib.integrations.starlette_client import OAuth
from fastapi import HTTPException
from starlette.config import Config
from starlette.requests import Request

# Configure the OAuth client for Google authentication
config = Config('.env')
oauth = OAuth(config)

GOOGLE_MIN_OAUTH = {
    'name': 'google',
    'server_metadata_url': 'https://accounts.google.com/.well-known/openid-configuration',
    'client_id': '<Add client ID>',
    'client_secret': '<Add client secret',
    'client_kwargs': {
        'scope': 'openid email profile https://www.googleapis.com/auth/drive.file',
    },
    'authorize_params': {'access_type': 'offline',
                         'include_granted_scopes': 'true'}
}

drive_create_file_url = 'https://www.googleapis.com/upload/drive/v3/files?uploadType=media'


def is_google_authoritative(person_info) -> bool:
    """Security measure recommended by google.
        Args:
            The data from google authorization.
        Returns:
            True/False - is the data verified.
        """
    if (person_info.get('hd') and person_info.get('email_verified')) \
            or (person_info.get('email') and '@gmail.com' in person_info.get('email')):
        return True
    return False


def is_person_authorized(email: str) -> bool:
    """Checks whether the email is listed in the whitelist (hashed)."""
    hasher = hashlib.sha256()
    hasher.update(email.encode("utf-8"))
    hex_dig = hasher.hexdigest()
    with open('resources/whitelist.json', 'r') as file:
        whitelist = json.load(file).get('whitelist')
        return hex_dig in whitelist


def get_current_user(request: Request):
    """Define a function to get the current user from the session"""
    user = request.session.get('user')
    if user is None:
        raise HTTPException(status_code=401, detail='Not authenticated')
    return user


def add_a_new_user_to_whitelist(email: str) -> bool:
    hasher = hashlib.sha256()
    hasher.update(email.encode("utf-8"))
    hex_dig = hasher.hexdigest()
    try:
        # Open the JSON file for reading and writing and acquire a lock
        with open('resources/whitelist.json', 'r+') as file:
            data = json.load(file)

            # Append the new item to the "whitelist" array
            data['whitelist'].append(hex_dig)

            file.seek(0)  # Move the file pointer to the beginning of the file
            file.truncate()  # Clear the file contents

            # Write the updated data to the JSON file
            json.dump(data, file)
        return True

    except Exception as e:
        # Handle any exceptions that might occur during reading or writing
        print(f"Error accessing file: {e}")
        return False


def add_new_file_to_drive(request: Request, file) -> bool:
    user = request.session['user']
    token = user.token
    headers = {"Authorization": "Bearer ",
               'Content-Type': 'MIME',
               'Content-Length': file.size()}
    file_metadata = {
        "title": f"{file.name}.csv",
        'name': f"{file.name}.csv",
        "parents": [{"id": "1geJkc84wcKDl95rvSrCXc0zg66DJxJ2S"}]
    }
    files = {
        "data": ("metadata", json.dumps(file_metadata), "application/json; charset=UTF-8"),
        "file": requests.get("image_url").content
    }
    response = requests.post(drive_create_file_url, headers=headers, files=files)

    if not response.status == HTTPStatus.OK:
        # some retry machinism
        pass
    return True
