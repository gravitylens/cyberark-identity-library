# CyberArk Identity Library

This library provides functions to interact with the CyberArk Identity API.

## Installation
Install the library
```bash
pip install https://github.com/gravitylens/skytap-python/releases/download/v0.1.1-alpha/skytap-0.1.1-py3-none-any.whl
```

Import the library in your code and sign in
```python
Import cyberark_identity_library as id

base_url = "https://subdomain.id.cyberark.cloud"
app_id = "apiautomation"
username = "apiuser@subdomain"
password = "Passw0rd!"
id.new_identity_session(base_url, username, password, app_id)
```

## Functions

### `new_identity_session(base_url, username, password, app_id)`
Establishes a new identity session and retrieves an access token.

- `base_url`: The base URL of the CyberArk Identity instance.
- `username`: The username for authentication.
- `password`: The password for authentication.
- `app_id`: The application ID.

---

### `new_identity_user(username, pw, orgpath=None)`
Creates a new identity user.

- `username`: The username of the new user.
- `pw`: The password for the new user.
- `orgpath`: (Optional) The organizational path for the new user.

**Returns:**
- `uid`: The guid for the user.

---

### `add_user_to_role(uid, role_id)`
Adds a user to a specified role.

- `uid`: The user ID.
- `role_id`: The role ID.

---

### `set_additional_attribute(uid, attribute, value)`
Sets an additional attribute for a user.

- `uid`: The user ID.
- `attribute`: The attribute name.
- `value`: The value to set.

---

### `remove_identity_user(uid)`
Removes a user from the directory.

- `uid`: The user ID.

---

### `reset_identity_password(uid, new_password)`
Resets the password for a user.

- `uid`: The user ID.
- `new_password`: The new password.

---

### `create_organization(org_name, org_desc=None)`
Creates a new organization.

- `org_name`: The name of the organization.
- `org_desc`: (Optional) The description of the organization.

**Returns:**
- `org_id`: The guid for the user.
---

### `delete_organization(org_id)`
Deletes an organization.

- `org_id`: The organization ID.

---

### `get_organization(org_id)`
Retrieves details of an organization.

- `org_id`: The organization ID.

---

### `get_organizations()`
Retrieves a list of all organizations.

---

### `get_organization_roles(org_id)`
Retrieves roles for a given organization.

- `org_id`: The organization ID.

---

### `update_org_admins(org_id, uid)`
Updates the administrators for an organization.

- `org_id`: The organization ID.
- `uid`: The user ID to grant admin rights.

---

### `create_role(role_name, orgpath)`
Creates a new role.

- `role_name`: The name of the role.
- `orgpath`: The organizational path for the role.

**Returns:**
- `role_id`: The guid for the user.
---

### `assign_role_adminrights(role_id, path)`
Assigns admin rights to a role for a given path.

- `role_id`: The role ID.
- `path`: The path to assign admin rights to.

---

### `get_role(role_id)`
Retrieves details of a role.

- `role_id`: The role ID.

---

### `identity_query(script)`
Runs a custom identity query.

- `script`: The query script.

---

### `generate_unique_password(length=12, min_lowercase=2, max_lowercase=None, min_uppercase=2, max_uppercase=None, min_digits=2, max_digits=None, min_special=0, max_special=None, disallowed_chars="")`
Generates a unique password with a mix of uppercase, lowercase, digits, and special characters. You can specify minimum and maximum counts for each character type, and exclude any characters you don't want in the password.

- `length`: (Optional) Total length of the password. Must be at least the sum of all minimum character requirements. Default is 12.
- `min_lowercase`: (Optional) Minimum number of lowercase letters. Default is 2.
- `max_lowercase`: (Optional) Maximum number of lowercase letters. Default is None (no limit). If set to 0, no lowercase letters will be included.
- `min_uppercase`: (Optional) Minimum number of uppercase letters. Default is 2.
- `max_uppercase`: (Optional) Maximum number of uppercase letters. Default is None (no limit). If set to 0, no uppercase letters will be included.
- `min_digits`: (Optional) Minimum number of digits. Default is 2.
- `max_digits`: (Optional) Maximum number of digits. Default is None (no limit). If set to 0, no digits will be included.
- `min_special`: (Optional) Minimum number of special characters. Default is 0.
- `max_special`: (Optional) Maximum number of special characters. Default is None (no limit). If set to 0, no special characters will be included.
- `disallowed_chars`: (Optional) String of characters that should not be included in the password. Default is an empty string.

**Returns:**  
A unique password string that meets all specified requirements.

**Raises:**  
- `ValueError` if the password length is less than the sum of minimum character requirements, or if disallowed characters exclude all possible characters for password generation.

