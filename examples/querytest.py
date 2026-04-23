import os
import cyberark_identity_library as id
from dotenv import load_dotenv
import csv
import time
    
load_dotenv()

#Login to Identity
base_url = os.getenv("identityURL")
username = os.getenv("identityuid")
password = os.getenv("identitypw")
app_id = os.getenv("appid")
id.new_identity_session(base_url, username, password, app_id)
print("new_identity_session: Success")

result = id.identity_query("SELECT * FROM orgs")

print(result)