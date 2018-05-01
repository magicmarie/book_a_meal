from tests.base import BaseTestCase
import json


class Test_menu_options(BaseTestCase):
    def test_add_menu(self):
        with self.client:
            response = self.add_menu()
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data.get('message'), "Menu successfully created")
            # Add the same menu and see...
            res = self.add_menu()
            print(res)
            data1 = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 400)
            self.assertEqual(data1.get('message'), "Menu name already  exists")

    def test_get_menu(self):
        with self.client:
            pass
