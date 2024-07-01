import logging

from api_wrapper import APIWrapper
from utils import (get_titles_playable_on_device,
                   filter_active_items,
                   get_level3_hd_manifest_paths)
from config import (API_ENDPOINT_MANIFESTS,
                    API_ENDPOINT_TITLES,
                    API_USER,
                    API_PASSWORD)

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    level=logging.DEBUG
)


def main():
    Titles = APIWrapper(API_ENDPOINT_TITLES, API_USER, API_PASSWORD)
    Manifests = APIWrapper(API_ENDPOINT_MANIFESTS, API_USER, API_PASSWORD)

    roku_titles = get_titles_playable_on_device(Titles, "ROKU")
    active_titles = filter_active_items(roku_titles)
    level3_hd_manifest_paths = get_level3_hd_manifest_paths(Manifests,
                                                            active_titles)

    for title, path in zip(active_titles, level3_hd_manifest_paths):
        title_name = title["localizableInformation"][0]["titleNameMedium"]
        print(f"{title_name}: {path}")


if __name__ == "__main__":
    main()
