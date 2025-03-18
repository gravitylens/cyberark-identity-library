# CyberArk Identity Library

This library provides functions to interact with the CyberArk Identity API.

## Installation



## Functions

### `new_identity_session(base_url, username, password, app_id)`

Establishes a new identity session and retrieves an access token.

- `base_url`: The base URL of the CyberArk Identity instance.
- `username`: The username for authentication.
- `password`: The password for authentication.
- `app_id`: The application ID.

### `new_identity_user(username, pw, orgpath=None)`

Creates a new identity user.

- `username`: The username of the new user.
- `pw`: The password for the new user.
- `orgpath`: (Optional) The organizational path for the new user.

### `add_user_to_role(uid, role_id)`

Adds a user to a specified role.

- `uid`: The user ID.
- `role_id`: The role ID.

### `set_additional_attribute(uid, attribute, value)`

Sets an additional attribute for a user.

- `uid`: The user ID.
- `attribute`: The attribute name.
- `value`: The attribute value.

### `remove_identity_user(uid)`

Removes an identity user.

- `uid`: The user ID.

### `reset_identity_password(uid, new_password)`

Resets the password for an identity user.

- `uid`: The user ID.
- `new_password`: The new password.

### `create_organization(org_name, org_desc=None)`

Creates a new organization.

- `org_name`: The name of the organization.
- `org_desc`: (Optional) The description of the organization.

### `delete_organization(org_id)`

Deletes an organization.

- `org_id`: The organization ID.

### `get_organization(org_id)`

Retrieves details of an organization.

- `org_id`: The organization ID.

### `get_organizations()`

Retrieves a list of all organizations.

- Returns: A list of organizations.

### `get_organization_roles(org_id)`

Retrieves roles associated with a specific organization.

- `org_id`: The organization ID.

### `update_org_admins(org_id, uid)`

Updates the administrators of an organization.

- `org_id`: The organization ID.
- `uid`: The user ID to be granted admin rights.

### `create_role(role_name, orgpath)`

Creates a new role within an organization.

- `role_name`: The name of the role.
- `orgpath`: The organizational path where the role will be created.

### `assign_role_adminrights(role_id, path)`

Assigns administrative rights to a role for a specific path.

- `role_id`: The role ID.
- `path`: The path to assign admin rights.

### `get_role(role_id)`

Retrieves details of a specific role.

- `role_id`: The role ID.

### `identity_query(script)`

Executes a custom query against the CyberArk Identity API.

- `script`: The query script to execute.

## Running Tests

To run the test cases, execute the `test.py` script:
```sh
python test.py
```