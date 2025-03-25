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
    identity_query,
    generate_unique_password
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

for i in range(250):
    username = f"vi{str(i).zfill(3)}@impact2025.com"
    password = generate_unique_password(length=8,max_special=0,disallowed_chars="1iIlLoO0|")
    
    #add to group "Venafi Impact Users"

    

