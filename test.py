import os
from identity import (
    new_identity_session,
    new_identity_user,
    add_user_to_role,
    set_additional_attribute,
    remove_identity_user,
    reset_identity_password,
    create_organization,
    delete_organization,
    get_organization
)

def load_env():
    from dotenv import load_dotenv
    load_dotenv()

def test_new_identity_session():
    base_url = os.getenv("identityURL")
    username = os.getenv("identityuid")
    password = os.getenv("identitypw")
    app_id = os.getenv("appid")
    new_identity_session(base_url, username, password, app_id)
    print("new_identity_session: Success")

def test_new_identity_user():
    result = new_identity_user("testuser@training-us", "TestPassword123")
    print(f"new_identity_user: {result}")

def test_add_user_to_role():
    result = add_user_to_role("testuser_id", "testrole_id")
    print(f"add_user_to_role: {result}")

def test_set_additional_attribute():
    result = set_additional_attribute("testuser_id", "customAttribute", "customValue")
    print(f"set_additional_attribute: {result}")

def test_remove_identity_user():
    remove_identity_user("testuser_id")
    print("remove_identity_user: Success")

def test_reset_identity_password():
    result = reset_identity_password("testuser_id", "NewTestPassword123")
    print(f"reset_identity_password: {result}")

def test_create_organization():
    result = create_organization("TestOrg", "Test Organization Description")
    print(f"create_organization: {result}")

def test_delete_organization():
    result = delete_organization("9c08e30e-bcd8-4dcd-b3a2-5e5bae421ad5")
    print(f"delete_organization: {result}")

def test_get_organization():
    result = get_organization("9c08e30e-bcd8-4dcd-b3a2-5e5bae421ad5")
    print(f"get_organization: {result}")

if __name__ == "__main__":
    load_env()
    test_new_identity_session()
#    test_create_organization()
#    test_get_organization()
#    test_delete_organization()
    test_new_identity_user()