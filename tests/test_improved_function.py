#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cyberark_identity_library.identity import new_identity_session, add_user_to_role
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

def test_improved_function():
    # Get credentials from .env file
    base_url = os.getenv("identityURL")
    app_id = os.getenv("appid")
    username = os.getenv("identityuid")
    password = os.getenv("identitypw")
    
    print("=== Testing Improved add_user_to_role Function ===")
    print(f"Connecting to: {base_url}")
    
    try:
        # Step 1: Authenticate
        print("\n--- Authentication ---")
        new_identity_session(base_url, username, password, app_id)
        print("✅ Session created successfully!")
        
        # Step 2: Test the improved function with string parameters
        print(f"\n--- Testing add_user_to_role with string parameters ---")
        
        target_user = "u80003@epmlab.local"  # We know this user exists
        target_role = "EPM_Role-80003"       # We know this role exists
        
        print(f"👤 User: {target_user}")
        print(f"🏷️  Role: {target_role}")
        print(f"🔧 Calling: add_user_to_role('{target_user}', '{target_role}')")
        
        # Call the improved function - now it's just one simple call!
        result = add_user_to_role(target_user, target_role)
        
        print(f"\n📄 Result:")
        print(json.dumps(result, indent=2))
        
        if result.get("success"):
            print(f"\n🎉 SUCCESS!")
            print(f"✅ {result.get('message')}")
            print(f"📋 User ID: {result.get('user_id')}")
            print(f"📋 Role ID: {result.get('role_id')}")
        else:
            print(f"\n❌ FAILED!")
            print(f"❌ Error: {result.get('error_message')}")
            print(f"🔍 Error Type: {result.get('error_type')}")
            if result.get('details'):
                print(f"ℹ️  Details: {result.get('details')}")
        
        # Step 3: Test with non-existent user (error handling)
        print(f"\n--- Testing Error Handling (Non-existent user) ---")
        
        result2 = add_user_to_role("nonexistent@test.com", target_role)
        print(f"📄 Error result:")
        print(json.dumps(result2, indent=2))
        
        # Step 4: Test with non-existent role (error handling) 
        print(f"\n--- Testing Error Handling (Non-existent role) ---")
        
        result3 = add_user_to_role(target_user, "NonExistentRole")
        print(f"📄 Error result:")
        print(json.dumps(result3, indent=2))
        
        print(f"\n--- Summary ---")
        print(f"✅ Function now accepts string parameters (username, role_name)")
        print(f"✅ Automatic ID lookup built-in")
        print(f"✅ Detailed error handling and reporting")
        print(f"✅ Single function call instead of 3 separate API calls")
        print(f"\n💡 Usage is now as simple as:")
        print(f"   result = add_user_to_role('username', 'rolename')")
        
        return result.get("success", False) if result else False
        
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_improved_function()
    
    if success:
        print(f"\n🎯 DEMONSTRATION COMPLETE!")
        print(f"✅ The improved function successfully handles user-role assignment")
    else:
        print(f"\n❌ Test failed - see details above")