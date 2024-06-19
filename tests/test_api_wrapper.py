import unittest
from unittest.mock import patch, MagicMock
import requests

from api_wrapper import APIWrapper


class TestAPIWrapper(unittest.TestCase):
    def setUp(self):
        self.endpoint_1 = "http://example.com/endpoint_1"
        self.endpoint_2 = "http://example.com/endpoint_2"
        self.username = "user"
        self.password = "pass"
        self.api = APIWrapper(self.endpoint_1,
                              self.endpoint_2,
                              self.username,
                              self.password)

    @patch('requests.get')
    def test_make_request_success(self, mock_get):
        # Mock the response to return a successful JSON response
        mock_response = MagicMock()
        mock_response.json.return_value = {"results": ["data"]}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        response = self.api.make_request("http://example.com/test")
        self.assertEqual(response, {"results": ["data"]})

    @patch('requests.get')
    def test_make_request_http_error_retry(self, mock_get):
        # Mock the response to simulate HTTP 500 error and then a success
        mock_response_500 = MagicMock()
        mock_response_500.raise_for_status.side_effect = requests.exceptions.HTTPError("Internal Server Error")
        mock_response_500.status_code = 500

        mock_response_success = MagicMock()
        mock_response_success.json.return_value = {"results": ["data"]}
        mock_response_success.raise_for_status = MagicMock()

        mock_get.side_effect = [mock_response_500, mock_response_success]

        response = self.api.make_request("http://example.com/test")
        self.assertEqual(response, {"results": ["data"]})
        self.assertEqual(mock_get.call_count, 2)  # Ensure it retried once

    @patch('requests.get')
    def test_make_request_http_error_fail(self, mock_get):
        # Mock the response to always return an HTTP error
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Internal Server Error")
        mock_response.status_code = 500

        mock_get.return_value = mock_response

        with self.assertRaises(Exception) as context:
            self.api.make_request("http://example.com/test")

        self.assertIn("Max retries exceeded", str(context.exception))
        self.assertEqual(mock_get.call_count, 5)  # Ensure it retried 5 times

    @patch('requests.get')
    def test_get_all_titles(self, mock_get):
        # Mock the response to return a successful JSON response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "results": [
                {"serviceKey": 1, "contentId": "Title 1"},
                {"serviceKey": 2, "contentId": "Title 2"},
                {"serviceKey": 3, "contentId": "Title 3"}
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        titles = self.api.get_all_titles()
        self.assertEqual(len(titles), 3)
        self.assertIn({"serviceKey": 1, "contentId": "Title 1"}, titles)
        self.assertIn({"serviceKey": 2, "contentId": "Title 2"}, titles)
        self.assertIn({"serviceKey": 3, "contentId": "Title 3"}, titles)

    @patch('requests.get')
    def test_get_manifest_paths(self, mock_get):
        # Mock the response to return a successful JSON response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "results": [
                {"contentId": "1", "assets": [{"path": "path1",
                                               "videoFormat": "HD"}]},
                {"contentId": "2", "assets": [{"path": "path2",
                                               "videoFormat": "SD"}]},
                {"contentId": "3", "assets": [{"path": "path3",
                                               "videoFormat": "HD"}]}
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        manifest_paths = self.api.get_manifest_paths("2")
        self.assertEqual(len(manifest_paths), 1)
        self.assertEqual(manifest_paths, [
            {"contentId": "2", "assets": [{"path": "path2",
                                           "videoFormat": "SD"}]}
        ])


if __name__ == '__main__':
    unittest.main()
