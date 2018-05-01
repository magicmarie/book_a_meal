# import unittest
# # import os
# import json
# from flask import jsonify
# from .app import app, create_app
# from app.api.models.user import User

# # config_name = os.getenv('FLASK_CONFIG', 'development')


# # class Test_auth(unittest.TestCase):
# #     def setUp(self):
# #         self.app = create_app('testing')
# #         self.client = self.app.test_client()
# #         with app.app_context():
# #             pass

# #     def tearDown(self):
# #         self.app_context.pop()

# #     def test_signup(self):
# #         response = self.client.post(
# #             'api/v1/auth/signup',
# #             data=jsonify(
# #                 dict(
# #                     name="mariam",
# #                     email="marie@live.com",
# #                     password="magic", confirm_password="magic")
# #             )
# #         )
# #         # convert byte data to json or dictionary
# #         data = json.loads(response.data)
# #         self.assertEqual(response.status_code, 201)
# #         self.assertEqual(data.get('message'), "signup successful")
# #         # Add the same user and see...
# #         response = self.client.post(
# #             'api/v1/auth/signup',
# #             data=jsonify(
# #                 dict(
# #                     name="mariam",
# #                     email="marie@live.com",
# #                     password="magic", confirm_password="magic")
# #             )
# #             # content_type="application/json"
# #         )
# #         data = json.loads(response.data)
# #         self.assertEqual(response.status_code, 200)
# #         self.assertEqual(data.get('message'), "user already exists")
