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
roleid = create_role("Venafi Users", None)

# Open CSV file for logging
with open("venafi_out.csv", mode="w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    # Write header row
    csv_writer.writerow(["username", "password"])

    for i in range(250):
        username = f"vi{str(i).zfill(3)}@impact2025.com"
        password = generate_unique_password(length=8, max_special=0, disallowed_chars="1iIlLoO0|")
        
        # Log variables to CSV
        csv_writer.writerow([username, password])
        
        uid = new_identity_user(username, password)
        time.sleep(1)
        add_user_to_role(uid, roleid)

