"""Unit tests for the counter service."""
from unittest import TestCase
from service import app
from service import routes
from service.common import status


class CounterTest(TestCase):
    """Counter service tests"""

    def setUp(self):
        routes.COUNTERS.clear()
        self.client = app.test_client()

    def test_index(self):
        """It should return the service index"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_health(self):
        """It should report healthy"""
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.get_json()["status"], "OK")

    def test_create_a_counter(self):
        """It should create a counter"""
        resp = self.client.post("/counters/foo")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.get_json()["counter"], 0)

    def test_duplicate_a_counter(self):
        """It should not create a duplicate counter"""
        self.client.post("/counters/bar")
        resp = self.client.post("/counters/bar")
        self.assertEqual(resp.status_code, status.HTTP_409_CONFLICT)

    def test_list_counters(self):
        """It should list counters"""
        self.client.post("/counters/a")
        resp = self.client.get("/counters")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("a", resp.get_json())

    def test_read_a_counter(self):
        """It should read a counter"""
        self.client.post("/counters/foo")
        resp = self.client.get("/counters/foo")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.get_json()["counter"], 0)

    def test_read_missing_counter(self):
        """It should return 404 for a missing counter"""
        resp = self.client.get("/counters/nope")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_a_counter(self):
        """It should increment a counter"""
        self.client.post("/counters/foo")
        resp = self.client.put("/counters/foo")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.get_json()["counter"], 1)

    def test_update_missing_counter(self):
        """It should return 404 when incrementing a missing counter"""
        resp = self.client.put("/counters/nope")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_a_counter(self):
        """It should delete a counter"""
        self.client.post("/counters/foo")
        resp = self.client.delete("/counters/foo")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        resp = self.client.get("/counters/foo")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
