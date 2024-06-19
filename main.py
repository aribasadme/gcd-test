import logging

from api_wrapper import APIWrapper
from utils import (get_titles_playable_on_device,
                   filter_active_items,
                   get_level3_hd_manifest_paths)
from config import (API_ENDPOINT_1,
                    API_ENDPOINT_2,
                    API_USER,
                    API_PASSWORD)

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    level=logging.DEBUG
)


def main():
    api_wrapper = APIWrapper(API_ENDPOINT_1,
                             API_ENDPOINT_2,
                             API_USER,
                             API_PASSWORD)

    roku_titles = get_titles_playable_on_device(api_wrapper, "ROKU")
    active_titles = filter_active_items(roku_titles)
    level3_hd_manifest_paths = get_level3_hd_manifest_paths(api_wrapper,
                                                            active_titles)

    for title, path in zip(active_titles, level3_hd_manifest_paths):
        title_name = title["localizableInformation"][0]["titleNameMedium"]
        print(f"{title_name}: {path}")


if __name__ == "__main__":
    main()
