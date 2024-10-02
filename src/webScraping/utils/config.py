from webScraping.platforms.git_get_data_entry import (
    git_get_data_entry,
    git_create_jobfile,
)
from webScraping.platforms.idd_get_data_entry import (
    idd_get_data_entry,
    idd_create_jobfile,
)


job_platform_dict = {
    "get-in-it": {
        "request_supported": True,
        "get_data_entry": git_get_data_entry,
        "write_json_file": git_create_jobfile,
    },
    "indeed": {
        "request_supported": False,
        "get_data_entry": idd_get_data_entry,
        "write_json_file": idd_create_jobfile,
    },
}
