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

def add_user_to_role(username, role_name):
    """
    Add a user to a role by username and role name (with automatic ID lookup)
    
    Args:
        username (str): Username, email, or display name of the user
        role_name (str): Name of the role
    
    Returns:
        dict: Result with success status and details, or error information
        
    Examples:
        # Add user to role by name
        result = add_user_to_role("user@domain.com", "System Administrator")
        
        # Check result
        if result.get("success"):
            print("User added successfully!")
        else:
            print(f"Failed: {result.get('error_message')}")
    """
    
    # Step 1: Look up user ID
    user_id = None
    user_display_name = None
    
    # Try different user lookup methods
    user_queries = [
        f"SELECT * FROM User WHERE DisplayName = '{username}'",
        f"SELECT * FROM User WHERE Username = '{username}'", 
        f"SELECT * FROM User WHERE Email = '{username}'"
    ]
    
    for query in user_queries:
        try:
            user_result = identity_query(query)
            if user_result and not user_result.get('error'):
                results = user_result.get('Results', [])
                if results:
                    user_data = results[0]['Row']
                    user_id = user_data.get('ID')
                    user_display_name = user_data.get('DisplayName') or user_data.get('Username')
                    break
        except Exception as e:
            continue  # Try next query format
    
    if not user_id:
        return {
            "success": False,
            "error_type": "user_not_found", 
            "error_message": f"User '{username}' not found",
            "details": "User lookup failed with DisplayName, Username, and Email queries"
        }
    
    # Step 2: Look up role ID
    role_id = None
    role_display_name = None
    
    try:
        role_query = f"SELECT * FROM Role WHERE Name = '{role_name}'"
        role_result = identity_query(role_query)
        
        if role_result and not role_result.get('error'):
            results = role_result.get('Results', [])
            if results:
                role_data = results[0]['Row']
                role_id = role_data.get('ID')
                role_display_name = role_data.get('Name')
        
        if not role_id:
            return {
                "success": False,
                "error_type": "role_not_found",
                "error_message": f"Role '{role_name}' not found", 
                "details": f"Role query returned no results for name '{role_name}'"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error_type": "role_query_failed",
            "error_message": f"Failed to query role '{role_name}': {str(e)}",
            "details": "Exception occurred during role lookup"
        }
    
    # Step 3: Perform the assignment
    try:
        uri = f"{url}/SaasManage/AddUsersAndGroupsToRole"
        
        body = {
            "Name": role_id,
            "Users": [user_id]
        }
        
        response = requests.post(uri, headers=headers, json=body)
        assignment_result = response.json()
        
        # Enhance the result with our lookup information
        if assignment_result.get("success"):
            return {
                "success": True,
                "message": f"Successfully added user '{user_display_name}' to role '{role_display_name}'",
                "user_id": user_id,
                "user_name": user_display_name,
                "role_id": role_id, 
                "role_name": role_display_name,
                "api_response": assignment_result
            }
        else:
            return {
                "success": False,
                "error_type": "assignment_failed",
                "error_message": assignment_result.get("Message", "Assignment API call failed"),
                "user_id": user_id,
                "user_name": user_display_name,
                "role_id": role_id,
                "role_name": role_display_name,
                "api_response": assignment_result
            }
            
    except Exception as e:
        return {
            "success": False,
            "error_type": "api_exception", 
            "error_message": f"Assignment API call failed: {str(e)}",
            "user_id": user_id,
            "user_name": user_display_name,
            "role_id": role_id,
            "role_name": role_display_name
        }

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

def identity_query(script, page_number=1, page_size=100, limit=100000, sort_by="", caching=-1):
    """
    Execute a RedRock query against the CyberArk Identity database
    
    Args:
        script (str): SQL query to execute
        page_number (int): Page number for pagination (default: 1)
        page_size (int): Number of records per page (default: 100) 
        limit (int): Maximum total records (default: 100000)
        sort_by (str): Sort field (default: "")
        caching (int): Caching setting (default: -1)
    
    Returns:
        dict: Query result with Results, Count, Columns, etc. or error message
    
    Examples:
        # Query users
        result = identity_query("SELECT * FROM User WHERE DisplayName LIKE '%john%'")
        
        # Query roles
        result = identity_query("SELECT * FROM Role WHERE Name = 'EPM_80003'")
    """
    uri = f"{url}/RedRock/query"

    body = {
        "Script": script,
        "Args": {
            "PageNumber": page_number,
            "PageSize": page_size,
            "Limit": limit,
            "SortBy": sort_by,
            "Caching": caching
        }
    }

    response = requests.post(uri, headers=headers, json=body)
    
    if response.status_code == 200:
        json_response = response.json()
        if json_response.get("success"):
            return json_response.get("Result")
        else:
            return {"error": True, "message": json_response.get("Message", "Unknown error")}
    else:
        return {"error": True, "message": f"HTTP {response.status_code}: {response.text}"}

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