import requests
from requests.auth import HTTPBasicAuth
import time
import logging


class APIWrapper:
    def __init__(self,
                 endpoint_1: str,
                 endpoint_2: str,
                 username: str,
                 password: str):
        self.endpoint_1 = endpoint_1  # Contains manifest data
        self.endpoint_2 = endpoint_2  # Contains titles data
        self.auth = HTTPBasicAuth(username, password)

    def make_request(self, url: str):
        """
        Function to make a request to the API and handle retries if needed
        :param url: URL to make the request to
        :return: JSON response from the API
        """
        max_retries = 5
        for attempt in range(max_retries):
            try:
                logging.debug(f"Attempt {attempt + 1} for URL: {url}")
                response = requests.get(url, auth=self.auth)
                response.raise_for_status()
                logging.debug(f"Response received: {response.json()}")
                return response.json()
            except requests.exceptions.HTTPError as e:
                logging.error(f"HTTPError: {response.reason} "
                              f"(status code: {response.status_code})")
                if response.status_code == 500:
                    logging.info(f"Retrying after {2 ** attempt} seconds...")
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    raise e
            except requests.exceptions.RequestException as e:
                logging.error(f"RequestException encountered: {e}")
                raise e
        raise Exception("Max retries exceeded")

    def get_all_titles(self):
        """
        Function to fetch all titles from the API
        :return: List of titles
        """
        logging.info(f"Fetching titles from endpoint: {self.endpoint_2}")
        titles = []
        response = self.make_request(self.endpoint_2)
        for result in response["results"]:
            titles.append(result)
        return titles

    def get_manifest_paths(self, title_id: int):
        """
        Function to fetch manifest paths for a given title ID
        :param title_id: ID of the title
        :return: List of manifest paths
        """
        logging.info(f"Fetching manifest paths for title ID: {title_id}")
        manifest_paths = []
        response = self.make_request(self.endpoint_1)
        for result in response["results"]:
            if result["contentId"] == title_id:
                manifest_paths.append(result)
        return manifest_paths
