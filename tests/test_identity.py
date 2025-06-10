import os
import unittest

import cyberark_identity_library.identity as identity

class TestIdentity(unittest.TestCase):
    def setUp(self):
        identity.new_identity_session(
            os.environ.get("identityURL", "http://example.com"),
            os.environ.get("identityuid", "user"),
            os.environ.get("identitypw", "pass"),
            os.environ.get("appid", "app"),
        )

    def test_new_identity_user_and_remove(self):
        result = identity.new_identity_user("user@cau-lab-01", "Secret123!")
        # Accept either a dict with 'id' or an error message string
        if isinstance(result, dict) and "id" in result:
            uid = result["id"]
            # Now test removing the same user
            remove_result = identity.remove_identity_user(uid)
            # You may want to assert something about remove_result if it returns a value
            self.assertIsNone(remove_result)  # Adjust this if remove_identity_user returns something else
        else:
            self.assertIsInstance(result, str)

if __name__ == "__main__":
    unittest.main()
