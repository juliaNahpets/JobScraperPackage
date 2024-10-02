from webScraping.utils.get_encoded_id import get_encoded_id
from webScraping.utils.create_data_json import get_file_path


def json_file_exists(url, platform):
    id = get_encoded_id(url)
    json_file = get_file_path(id, platform)
    return json_file.exists()
