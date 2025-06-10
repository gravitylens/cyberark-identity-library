import os
from cyberark_identity_library.identity import (
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
import csv
import time
    
load_dotenv()

#Login to Identity
base_url = os.getenv("identityURL")
username = os.getenv("identityuid")
password = os.getenv("identitypw")
app_id = os.getenv("appid")
new_identity_session(base_url, username, password, app_id)
print("new_identity_session: Success")

# Open CSV file for logging
with open("identity_out.csv", mode="w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    # Write header row
    csv_writer.writerow(["orgpath", "adminuid", "adminpw", "enduid", "endpw"])

    # Loop to create a new organization, role, and users
    for i in range(250):
        orgpath = f"Impact{str(i).zfill(3)}"
        adminusername = f"admin{str(i).zfill(3)}@impact2025.com"
        adminpassword = generate_unique_password(length=8, max_special=0, disallowed_chars="1iIlLoO0|")
        endusername = f"enduser{str(i).zfill(3)}@impact2025.com"
        endpassword = generate_unique_password(length=8, max_special=0, disallowed_chars="1iIlLoO0|")

        # Log variables to CSV
        csv_writer.writerow([orgpath, adminusername, adminpassword, endusername, endpassword])

        # Create organization, role, and users
        org_id = create_organization(orgpath, f"{orgpath} Organization Description")
        role_id = create_role(f"Role{str(i).zfill(3)}", orgpath)
        assign_role_adminrights(role_id, "/lib/rights/appman.json")
        assign_role_adminrights(role_id, "/lib/rights/roleman.json")
        admin_uid = new_identity_user(adminusername, adminpassword, orgpath)
        add_user_to_role(admin_uid, role_id)
        add_user_to_role(admin_uid, "Privilege_Cloud_Admins_ID")

        update_org_admins(org_id, admin_uid)
        end_uid = new_identity_user(endusername, endpassword, orgpath)
        add_user_to_role(end_uid, "Privilege_Cloud_Users_ID")

        #TODO: Add user to SWS Role
        
        time.sleep(2)