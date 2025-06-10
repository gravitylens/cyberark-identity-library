import requests
import json
import base64
import secrets
import string

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

def new_identity_user(username, pw, orgpath=None):
    uri = f"{url}/CDirectoryService/CreateUser"

    body = {
        "Name": username,
        "Mail": username,
        "DisplayName": username,
        "Password": pw,
        "ConfirmPassword": pw,
        "MFA": False,
        "PasswordNeverExpire": True,
        "ForcePasswordChangeNext": False,
        "OrgPath": orgpath
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
        result = "Password Reset"
    else:
        result = f"Unable to Reset Password for {uid}"

    return result

def create_organization(org_name, org_desc=None):
    uri = f"{url}/Org/Create"

    body = {
        "Name": org_name,
        "Description": org_desc
    }

    response = requests.post(uri, headers=headers, json=body)
    
    if response.json()["success"]:
        result = response.json()["Result"]
    else:
        result = f"Unable to create organization {org_name}"

    return result['ID']

def delete_organization(org_id):
    uri = f"{url}/Org/Delete"

    body = {
        "OrgId": org_id
    }

    response = requests.post(uri, headers=headers, json=body)
    
    if response.json()["success"]:
        result = f"Organization {org_id} deleted successfully"
    else:
        result = f"Unable to delete organization {org_id}"

    return result

def get_organization(org_id):
    uri = f"{url}/Org/Get"

    body = {
        "OrgId": org_id
    }

    response = requests.get(uri, headers=headers, json=body)
    
    if response.json()["success"]:
        result = response.json()["Result"]
    else:
        result = f"Unable to retrieve organization {org_id}"

    return result

def get_organizations():
    uri = f"{url}/Org/ListAll"
    response = requests.get(uri, headers=headers)
    if response.json()["success"]:
        result = response.json()["Result"]
    else:
        result = "Unable to retrieve organizations"
    return result

def get_organization_roles(org_id):
    uri = f"{url}/Org/GetRoles"
    body = {
        "OrgId": org_id
    }
    response = requests.post(uri, headers=headers, json=body)
    if response.json()["success"]:
        result = response.json()["Result"]
    else:
        result = "Unable to retrieve roles"
    return result

def update_org_admins(org_id, uid):
    uri = f"{url}/Org/UpdateAdministrators"
    body = {
        "Grant": [
            {
            "Id": uid,
            "Type": "User"
            }
        ],
        "OrgId": org_id
    }
    response = requests.post(uri, headers=headers, json=body)
    if response.json()["success"]:
        result = response.json()["Result"]
    else:
        result = "Unable to update org admins"
    return result

def create_role(role_name, orgpath):
    uri = f"{url}/Roles/StoreRole"

    body = {
        "Name": role_name,
        "Description": "{role_name} Description",
        "RoleType": "PrincipalList",
        "OrgPath": orgpath,
    }

    response = requests.post(uri, headers=headers, json=body)
    
    if response.json()["success"]:
        result = response.json()["Result"]
    else:
        result = f"Unable to create role {role_name}"

    return result["_RowKey"]

def assign_role_adminrights(role_id, path):
    uri = f"{url}/Roles/AssignSuperRights"
    body = [{
        "Role": role_id,
        "Path": path
    }]
    response = requests.post(uri, headers=headers, json=body)
    if response.json()["success"]:
        print(f"Role {role_id} assigned admin rights to {path}")
    else:
        print(f"Unable to assign admin rights to {role_id} for {path}")
    return response.json()

def get_role(role_id):
    uri = f"{url}/Roles/GetRole?Name={role_id}"

    response = requests.post(uri, headers=headers)
    
    if response.json()["success"]:
        result = response.json()["Result"]
    else:
        result = "Unable to retrieve roles"

    return result

def identity_query(script):
    uri= f"{url}/Redrock/query"

    body = {
        "Script": script
    }

    response = requests.post(uri, headers=headers, json=body)
    
    if response.json()["success"]:
        result = response.json()["Result"]
    else:
        result = "Unable to retrieve query results"

    return result

def generate_unique_password(
    length=12,
    min_lowercase=2,
    max_lowercase=None,
    min_uppercase=2,
    max_uppercase=None,
    min_digits=2,
    max_digits=None,
    min_special=0,
    max_special=None,
    disallowed_chars=""
):
    """
    Generates a unique password with a mix of letters, digits, and special characters.

    :param length: Length of the password (default is 12)
    :param min_lowercase: Minimum number of lowercase letters (default is 2)
    :param max_lowercase: Maximum number of lowercase letters (default is None, no limit)
    :param min_uppercase: Minimum number of uppercase letters (default is 2)
    :param max_uppercase: Maximum number of uppercase letters (default is None, no limit)
    :param min_digits: Minimum number of digits (default is 2)
    :param max_digits: Maximum number of digits (default is None, no limit)
    :param min_special: Minimum number of special characters (default is 0)
    :param max_special: Maximum number of special characters (default is None, no limit)
    :param disallowed_chars: A string of characters that should not be included in the password
    :return: A unique password string
    """
    if length < (min_lowercase + min_uppercase + min_digits + min_special):
        raise ValueError("Password length must be at least the sum of minimum character requirements")

    # Define allowed character sets
    allowed_lowercase = ''.join(c for c in string.ascii_lowercase if c not in disallowed_chars)
    allowed_uppercase = ''.join(c for c in string.ascii_uppercase if c not in disallowed_chars)
    allowed_special = ''.join(c for c in string.punctuation if c not in disallowed_chars)
    allowed_digits = ''.join(c for c in string.digits if c not in disallowed_chars)
    allowed_remaining = ''.join(c for c in (string.ascii_letters + string.digits) if c not in disallowed_chars)

    if not (allowed_lowercase and allowed_uppercase and allowed_digits and allowed_remaining):
        raise ValueError("Disallowed characters exclude all possible characters for password generation")

    # Generate required characters
    lowercase = ''.join(secrets.choice(allowed_lowercase) for _ in range(min_lowercase)) if max_lowercase != 0 else ''
    uppercase = ''.join(secrets.choice(allowed_uppercase) for _ in range(min_uppercase)) if max_uppercase != 0 else ''
    digits = ''.join(secrets.choice(allowed_digits) for _ in range(min_digits)) if max_digits != 0 else ''
    special = ''.join(secrets.choice(allowed_special) for _ in range(min_special)) if max_special != 0 else ''

    # Apply maximum limits if specified
    if max_lowercase is not None:
        lowercase = lowercase[:max_lowercase]
    if max_uppercase is not None:
        uppercase = uppercase[:max_uppercase]
    if max_digits is not None:
        digits = digits[:max_digits]
    if max_special is not None:
        special = special[:max_special]

    # Adjust remaining characters
    remaining_length = length - len(lowercase) - len(uppercase) - len(digits) - len(special)
    remaining = ''.join(secrets.choice(allowed_remaining) for _ in range(remaining_length))

    # Combine and shuffle
    password = list(lowercase + uppercase + digits + special + remaining)
    secrets.SystemRandom().shuffle(password)
    return ''.join(password)

__all__ = [
    "new_identity_session",
    "new_identity_user",
    "add_user_to_role",
    "set_additional_attribute",
    "remove_identity_user",
    "reset_identity_password",
    "create_organization",
    "delete_organization",
    "get_organization",
    "get_organizations",
    "get_organization_roles",
    "update_org_admins",
    "create_role",
    "assign_role_adminrights",
    "get_role",
    "identity_query",
    "generate_unique_password",
]