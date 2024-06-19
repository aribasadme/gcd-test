import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from utils import (get_titles_playable_on_device,
                   filter_active_items,
                   get_level3_hd_manifest_paths)


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.api_wrapper = MagicMock()

    def test_get_titles_playable_on_device(self):
        # Mock the get_all_titles method
        self.api_wrapper.get_all_titles.return_value = [
            {
                "serviceKey": 1,
                "contentId": "Title 1",
                "rights": {
                    "terms": [
                        {
                            "devices": [
                                {"devicePlatform": "ROKU"},
                                {"devicePlatform": "ANDROID"}
                            ]
                        }
                    ]
                }
            },
            {
                "serviceKey": 2,
                "contentId": "Title 2",
                "rights": {
                    "terms": [
                        {
                            "devices": [
                                {"devicePlatform": "IOS"},
                                {"devicePlatform": "WEB"}
                            ]
                        }
                    ]
                }
            },
            {
                "serviceKey": 3,
                "contentId": "Title 3",
                "rights": {
                    "terms": [
                        {
                            "devices": [
                                {"devicePlatform": "ROKU"},
                                {"devicePlatform": "ANDROID"},
                                {"devicePlatform": "IOS"}
                            ]
                        }
                    ]
                }
            }
        ]

        device_platform = "ROKU"
        roku_titles = get_titles_playable_on_device(self.api_wrapper,
                                                    device_platform)
        self.assertEqual(len(roku_titles), 2)
        self.assertIn({
            "serviceKey": 1,
            "contentId": "Title 1",
            "rights": {
                "terms": [
                    {
                        "devices": [
                            {"devicePlatform": "ROKU"},
                            {"devicePlatform": "ANDROID"}
                        ]
                    }
                ]
            }}, roku_titles)
        self.assertIn({
            "serviceKey": 3,
            "contentId": "Title 3",
            "rights": {
                "terms": [
                    {
                        "devices": [
                            {"devicePlatform": "ROKU"},
                            {"devicePlatform": "ANDROID"},
                            {"devicePlatform": "IOS"}
                        ]
                    }
                ]
            }}, roku_titles)

    def test_filter_active_items(self):
        # Create sample titles with different start and end dates
        titles = [
            {
                "serviceKey": 1,
                "contentId": "Active Title",
                "rights": {
                    "terms": [
                        {
                            "startDateTime": "2024-01-01T00:00:00.000Z",
                            "endDateTime": "2024-12-31T23:59:59.000Z"
                        }
                    ]
                }
            },
            {
                "serviceKey": 2,
                "contentId": "Expired Title",
                "rights": {
                    "terms": [
                        {
                            "startDateTime": "2022-01-01T00:00:00.000Z",
                            "endDateTime": "2022-12-31T23:59:59.000Z"
                        }
                    ]
                }
            },
            {
                "serviceKey": 3,
                "contentId": "Future Title",
                "rights": {
                    "terms": [
                        {
                            "startDateTime": "2025-01-01T00:00:00.000Z",
                            "endDateTime": "2025-12-31T23:59:59.000Z"
                        }
                    ]
                }
            }
        ]

        # Patch the datetime.now() function to control the current date
        with patch('utils.datetime', wraps=datetime) as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 6, 1)

            active_titles = filter_active_items(titles)
            self.assertEqual(len(active_titles), 1)
            self.assertIn({
                "serviceKey": 1,
                "contentId": "Active Title",
                "rights": {
                    "terms": [
                        {
                            "startDateTime": "2024-01-01T00:00:00.000Z",
                            "endDateTime": "2024-12-31T23:59:59.000Z"
                         }
                    ]
                }}, active_titles)

    def test_get_level3_hd_manifest_paths(self):
        # Mock the get_manifest_paths method
        self.api_wrapper.get_manifest_paths.return_value = [
            {"assets": [
                {
                    "videoFormat": "HD",
                    "endpoints": [
                        {
                            "origin": "level3",
                            "path": "/skyplayer/level3/path-1/hd/Manifest"
                        }
                    ]
                },
                {
                    "videoFormat": "SD",
                    "endpoints": [
                        {
                            "origin": "level3",
                            "path": "/skyplayer/level3/path-2/sd/Manifest"
                        }
                    ]
                },
                {
                    "videoFormat": "HD",
                    "endpoints": [
                        {
                            "origin": "akamai",
                            "path": "/skyplayer/level3/path-3/hd/Manifest"
                        }
                    ]
                }
            ]}
        ]

        active_titles = [
            {"serviceKey": 1, "contentId": "title1"}
        ]

        manifest_paths = get_level3_hd_manifest_paths(self.api_wrapper,
                                                      active_titles)
        self.assertEqual(len(manifest_paths), 1)
        self.assertIn("/skyplayer/level3/path-1/sd/Manifest", manifest_paths)


if __name__ == '__main__':
    unittest.main()
