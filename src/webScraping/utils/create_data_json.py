from pathlib import Path
import json


OUTPUT_PATH = Path("./data") / "output"


def get_file_name(id):
    return f"jobinfo_{id}.json"


def check_folder_path(path):
    folder_exists = path.exists()
    if not folder_exists:
        path.mkdir(parents=True)


def get_file_path(id, platform):
    folder_path = OUTPUT_PATH / platform
    check_folder_path(folder_path)
    return folder_path / get_file_name(id)


def create_data_json(data, platform):
    id = data["id"]
    with open(get_file_path(id, platform), "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
