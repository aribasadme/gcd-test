import logging
from datetime import datetime


def get_titles_playable_on_device(api_wrapper, device_platform: str) -> list:
    """
    Function to retrieve all titles that are playable on device_platform
    :param api_wrapper: An instance of the APIWrapper class
    :param device_platform: The platform for which to retrieve
                            titles (e.g., "ROKU", "ANDROID")
    :return: A list of dictionaries containing the titles
             playable on `device_platform`
    """
    logging.info(f"Retrieving titles playable on {device_platform}")
    platform_titles = []
    titles = api_wrapper.get_all_titles()
    for title in titles:
        for device in title["rights"]["terms"][0]["devices"]:
            if device["devicePlatform"] == device_platform:
                platform_titles.append(title)
                break
    logging.debug(f"{device_platform} titles: {platform_titles}")
    return platform_titles


def filter_active_items(titles: list) -> list:
    """
    Function to filter out items that are not active based on the current date
    :param titles: A list of dictionaries containing title information
    :return: A list of dictionaries containing the active titles
    """
    logging.info("Filtering active items based on current date")
    current_date = datetime.now().date()
    active_titles = []
    for title in titles:
        terms = title["rights"]["terms"][0]
        start_date = datetime.strptime(terms["startDateTime"],
                                       "%Y-%m-%dT%H:%M:%S.%fZ").date()
        end_date = datetime.strptime(terms["endDateTime"],
                                     "%Y-%m-%dT%H:%M:%S.%fZ").date()
        if start_date <= current_date <= end_date:
            active_titles.append(title)
    logging.debug(f"Active titles: {active_titles}")
    return active_titles


def get_level3_hd_manifest_paths(api_wrapper, active_titles: list) -> list:
    """
    Function to retrieve the Level3 HD manifest paths for active titles
    :param api_wrapper: An instance of the APIWrapper class
    :param active_titles: A list of dictionaries containing the active titles
    :return: A list of dictionaries containing the Level3 HD manifest paths
    """
    logging.info("Retrieving Level3 HD manifest paths for active titles")
    level3_paths = []
    for title in active_titles:
        title_id = title["contentId"]
        manifest_paths = api_wrapper.get_manifest_paths(title_id)
        for asset in manifest_paths[0]["assets"]:
            if (asset.get("videoFormat") == "HD" and
                    asset["endpoints"][0]["origin"] == "level3"):
                level3_paths.append(asset["endpoints"][0]["path"])
    logging.debug(f"Level3 HD manifest paths: {level3_paths}")
    return level3_paths
