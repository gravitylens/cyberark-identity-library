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
from dotenv import load_dotenv
    
load_dotenv()

#Login to Identity
base_url = os.getenv("identityURL")
username = os.getenv("identityuid")
password = os.getenv("identitypw")
app_id = os.getenv("appid")
new_identity_session(base_url, username, password, app_id)
print("new_identity_session: Success")

#Loop to create a new organization, role, and users

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