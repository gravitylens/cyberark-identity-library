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

    def test_new_identity_user(self):
        result = identity.new_identity_user("user@example.com", "Secret123!")
        self.assertEqual(result["id"], "dummy")

if __name__ == "__main__":
    unittest.main()
