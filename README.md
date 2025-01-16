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

## Running Tests

To run the test cases, execute the `test.py` script:
```sh
python test.py
```