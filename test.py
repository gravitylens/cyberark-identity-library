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
    get_organization,
    get_organizations,
    get_organization_roles,
    get_role,
    assign_role_adminrights,
    create_role,
    update_org_admins,
    identity_query
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
    result = new_identity_user("testuser@impact2025.com", "TestPassword123")
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

def test_get_role():
    result = get_organizations()
    print(f"get_organizations: {result}")
    result= get_organization("92ae59cd-e0e2-47c7-982a-7a3335b74c66")
    result= get_organization_roles("92ae59cd-e0e2-47c7-982a-7a3335b74c66")
    print(f"get_organization_roles: {result}")
    result = get_role("e58993ef-55c1-40cc-8159-ef5cafc0b41c")
    print(f"get_role: {result}")


if __name__ == "__main__":
    load_env()
    test_new_identity_session()
    orgpath = "TestOrg"
    org_id = create_organization(orgpath, f"{orgpath} Organization Description")
    role_id = create_role("TestRole", orgpath)
    assign_role_adminrights(role_id, "/lib/rights/appman.json")
    assign_role_adminrights(role_id, "/lib/rights/roleman.json")
    admin_uid = new_identity_user("testadmin@impact2025.com", "TestAdminPassword123", orgpath)
    add_user_to_role(admin_uid, role_id)
    add_user_to_role(admin_uid, "Privilege_Cloud_Users_ID")
    #TODO:Add user to SWSRole
    update_org_admins(org_id, admin_uid)
    end_uid = new_identity_user("testenduser@impact2025.com", "TestEndUserPassword123", orgpath)
    add_user_to_role(end_uid, "Privilege_Cloud_Users_ID")
    #TODO:Add user to SWSRole




