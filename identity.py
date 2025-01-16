import requests
import json
import base64

headers = {
    "Accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded"
}

def new_identity_session(base_url, username, password, app_id):
    global url
    url = base_url
    uri = f"{url}/oauth2/token/{app_id}"

    # Encode username:password as Base64 and add to header
    auth_str = f"{username}:{password}"
    authorization = base64.b64encode(auth_str.encode()).decode()
    headers["Authorization"] = f"Basic {authorization}"

    body = "grant_type=client_credentials&scope=all"

    response = requests.post(uri, headers=headers, data=body)
    access_token = response.json()["access_token"]
    headers["Authorization"] = f"Bearer {access_token}"

def new_identity_user(username, pw):
    uri = f"{url}/CDirectoryService/CreateUser"

    body = {
        "Name": username,
        "Mail": username,
        "DisplayName": username,
        "Password": pw,
        "ConfirmPassword": pw,
        "MFA": False,
        "PasswordNeverExpire": True,
        "ForcePasswordChangeNext": False
    }

    response = requests.post(uri, headers=headers, json=body)
    
    if response.json()["success"]:
        result = response.json()["Result"]
    else:
        result = f"Unable to create {username}"

    return result

def add_user_to_role(uid, role_id):
    uri = f"{url}/SaasManage/AddUsersAndGroupsToRole"

    body = {
        "Name": role_id,
        "Users": [uid]
    }

    try:
        response = requests.post(uri, headers=headers, json=body)
    except Exception as e:
        print(f"Unable to add {uid} to {role_id}")
        return

    return response.json()

def set_additional_attribute(uid, attribute, value):
    uri = f"{url}/ExtData/SetColumns"

    body = {
        "Table": "users",
        "ID": uid,
        "Columns": {
            attribute: value
        }
    }

    response = requests.post(uri, headers=headers, json=body)
    return response.json()

def remove_identity_user(uid):
    global url
    uri = f"{url}/UserMgmt/RemoveUser?ID={uid}"
    response = requests.post(uri, headers=headers)
    #return response.json()

def reset_identity_password(uid, new_password):
    uri = f"{url}/UserMgmt/ResetUserPassword"

    body = {
        "ID": uid,
        "newPassword": new_password
    }

    response = requests.post(uri, headers=headers, json=body)

    if response.json()["success"]:
s        result = "Password Reset"
    else:
        result = f"Unable to Reset Password for {uid}"

    return result
