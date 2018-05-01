from tests.base import BaseTestCase
import json


class Test_auth(BaseTestCase):
    def test_signup(self):
        with self.client:
            response = self.client.post(
                'api/v1/auth/signup',
                data=json.dumps(
                    dict(
                        name="mariam",
                        email="marie@live.com",
                        password="magic",
                        confirm_password="magic",
                        isAdmin="true"
                    )
                ),
                content_type='application/json'
            )
            # convert byte data to json or dictionary
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data.get('message'), "User successfully created")
            # Add the same user and see...
            response = self.client.post(
                'api/v1/auth/signup',
                data=json.dumps(
                    dict(
                        name="mariam",
                        email="marie@live.com",
                        password="magic",
                        confirm_password="magic",
                        isAdmin="true"
                    )
                ),
                content_type="application/json"
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data.get('message'), "email already in use")
