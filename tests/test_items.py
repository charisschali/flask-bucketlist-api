"""test_bucketlistitems.py."""
import json
from tests.test_setup import BaseTestCase


class ItemsTestCase(BaseTestCase):
    """This class contains tests for items."""

    def test_create_new_Item(self):
        """Test for successful creation of an item."""
        payload = {'item_name': 'The Louvre',
                   'description': 'Largest museum in Paris'}
        response = self.client.post("/api/v1/bucketlists/1/items",
                                    data=json.dumps(payload),
                                    headers=self.auth_header,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual("Item created successfully", str(response.data))

    def test_create_Item_with_invalid_name_format(self):
        """Test for creation of an item with an invalid name format."""
        payload = {'item_name': '1234%$#@!^&',
                   'description': 'Largest museum in Paris'}
        response = self.client.post("/api/v1/bucketlists/1/items",
                                    data=json.dumps(payload),
                                    headers=self.auth_header,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual("Invalid format", str(response.data))

    def test_create_Item_that_exists(self):
        """Test for creation of an item that already exists."""
        payload = {'item_name': 'The Eiffel Tower',
                   'description': 'Wrought iron lattice tower in France'}
        response = self.client.post("/api/v1/bucketlists/1/items",
                                    data=json.dumps(payload),
                                    headers=self.auth_header,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 409)
        self.assertIn("This item already exists", str(response.data))

    def test_create_Item_with_non_existent_bucketlist(self):
        """Test creation of an item with non existent bucketlist."""
        payload = {'item_name': 'The Louvre',
                   'description': 'Largest museum in Paris'}
        response = self.client.post("/api/v1/bucketlists/15/items",
                                    data=json.dumps(payload),
                                    headers=self.auth_header,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual("Bucketlist cannot be found", str(response.data))

    def test_get_all_BucketListItems(self):
        """Test retrieval of items successfully."""
        response = self.client.get("/api/v1/bucketlists/1/items")
        self.assertEqual(response.status_code, 200)
        self.assertIn("The Eiffel Tower", str(response.data))

    def test_get_Items_with_invalid_BucketList_Id(self):
        """Test retrieval of items with invalid bucketlist ID."""
        response = self.client.get("/api/v1/bucketlists/15/items",
                                   headers=self.auth_header)
        self.assertEqual(response.status_code, 404)
        self.assertEqual("Bucketlist cannot be found", str(response.data))

    def test_get_Items_by_id(self):
        """Test retrieval of an item by ID."""
        response = self.client.get("/api/v1/bucketlists/1/items/1",
                                   headers=self.auth_header)
        self.assertEqual(response.status_code, 200)

    def test_update_Item_by_id(self):
        """Test updating an item by ID."""
        payload = {'item_name': 'The Eiffel Tower',
                   'description': 'Tallest building in France'}
        response = self.client.put("/api/v1/bucketlists/1/items/1",
                                   data=json.dumps(payload),
                                   headers=self.auth_header,
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual("Item succesfully updated", str(response.data))

    def test_update_Items_with_invalid_BucketList_Id(self):
        """Test updating an item with invalid Bucketlist ID."""
        payload = {'item_name': 'The Eiffel Tower',
                   'description': 'Tallest building in France'}
        response = self.client.put("/api/v1/bucketlists/15/items/1",
                                   data=json.dumps(payload),
                                   headers=self.auth_header,
                                   content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual("Bucketlist cannot be found", str(response.data))

    def test_update_Item_that_does_not_exist(self):
        """Test updating an item that does not exist."""
        payload = {'item_name': 'The Eiffel Tower',
                   'description': 'Tallest building in France'}
        response = self.client.put("/api/v1/bucketlists/1/items/15",
                                   data=json.dumps(payload),
                                   headers=self.auth_header,
                                   content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual("Item cannot be found", str(response.data))

    def test_update_Item_with_same_data(self):
        """Test updating an item with the same data."""
        payload = {'item_name': 'The Eiffel Tower',
                   'description': 'Wrought iron lattice tower in France'}
        response = self.client.put("/api/v1/bucketlists/1/items/1",
                                   data=json.dumps(payload),
                                   headers=self.auth_header,
                                   content_type="application/json")
        self.assertEqual(response.status_code, 409)
        self.assertEqual("No updates detected",
                         str(response.data))

    def test_delete_Item_by_id(self):
        """Test deleting an item by ID."""
        response = self.client.delete("/api/v1/bucketlists/1/items/1",
                                      headers=self.auth_header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual("Item succesfully deleted", str(response.data))

    def test_delete_Item_that_does_not_exist(self):
        """Test deleting an item that does not exist."""
        response = self.client.delete("/api/v1/bucketlists/1/items/15",
                                      headers=self.auth_header,)
        self.assertEqual(response.status_code, 404)
        self.assertEqual("Item cannot be found", str(response.data))

    def test_delete_Items_with_invalid_BucketList_Id(self):
        """Test deleting an item with an invalid bucketlist ID."""
        response = self.client.delete("/api/v1/bucketlists/5/items/1",
                                      headers=self.auth_header,)
        self.assertEqual(response.status_code, 404)
        self.assertEqual("Bucketlist cannot be found", str(response.data))

    def test_change_Item_status(self):
        pass
