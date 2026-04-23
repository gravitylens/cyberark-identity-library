#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cyberark_identity_library.identity import new_identity_session, add_user_to_role
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

def test_api_user_assignment():
    # Get credentials from .env file
    base_url = os.getenv("identityURL")
    app_id = os.getenv("appid")
    username = os.getenv("identityuid")
    password = os.getenv("identitypw")
    
    print("=== Test: Add api@epmlab.local to EPM_Role-80004 ===")
    print(f"Connecting to: {base_url}")
    
    try:
        # Step 1: Authenticate
        print("\n--- Authentication ---")
        new_identity_session(base_url, username, password, app_id)
        print("✅ Session created successfully!")
        
        # Step 2: Test assignment with new user/role combination
        target_user = "api@epmlab.local"
        target_role = "EPM_Role-80004"
        
        print(f"\n--- Assignment Test ---")
        print(f"👤 User: {target_user}")
        print(f"🏷️  Role: {target_role}")
        print(f"🔧 Calling: add_user_to_role('{target_user}', '{target_role}')")
        
        # Call the improved function
        result = add_user_to_role(target_user, target_role)
        
        print(f"\n📄 Full Result:")
        print(json.dumps(result, indent=2))
        
        if result.get("success"):
            print(f"\n🎉 SUCCESS!")
            print(f"✅ Message: {result.get('message')}")
            print(f"📋 User Details:")
            print(f"   - ID: {result.get('user_id')}")
            print(f"   - Name: {result.get('user_name')}")
            print(f"📋 Role Details:")
            print(f"   - ID: {result.get('role_id')}")
            print(f"   - Name: {result.get('role_name')}")
            
            return True
            
        else:
            print(f"\n❌ ASSIGNMENT FAILED!")
            print(f"❌ Error Type: {result.get('error_type')}")
            print(f"❌ Error Message: {result.get('error_message')}")
            
            if result.get('details'):
                print(f"ℹ️  Details: {result.get('details')}")
            
            # Show what we found during lookup
            if result.get('user_id'):
                print(f"📋 User was found: {result.get('user_name')} (ID: {result.get('user_id')})")
            
            if result.get('role_id'):
                print(f"📋 Role was found: {result.get('role_name')} (ID: {result.get('role_id')})")
            
            # If it's a role not found error, let's see what roles are available
            if result.get('error_type') == 'role_not_found':
                print(f"\n🔍 Checking for similar EPM roles...")
                from cyberark_identity_library.identity import identity_query
                
                try:
                    epm_roles = identity_query("SELECT Name, Description FROM Role WHERE Name LIKE '%EPM%'", page_size=15)
                    if epm_roles and not epm_roles.get('error'):
                        print(f"   Available EPM roles:")
                        for role in epm_roles.get('Results', []):
                            role_data = role['Row']
                            print(f"     • {role_data.get('Name')} - {role_data.get('Description', 'No description')}")
                except Exception as e:
                    print(f"   ❌ Error listing roles: {e}")
            
            return False
        
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_api_user_assignment()
    
    if success:
        print(f"\n🎯 TEST SUCCESSFUL!")
        print(f"✅ api@epmlab.local successfully assigned to EPM_Role-80004")
        print(f"✅ The improved add_user_to_role function works perfectly!")
    else:
        print(f"\n❌ Test completed with issues - see details above")
        print(f"💡 Function still provides detailed error information for troubleshooting")