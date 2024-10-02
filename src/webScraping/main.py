from webScraping.utils.get_content import get_content
from webScraping.utils.config import job_platform_dict


def webscraping(dic):
    platform_name = dic["platform"]

    if platform_name in job_platform_dict:
        return job_platform_dict[platform_name]["get_data_entry"](dic)


def write_json_file(dic):
    platform_name = dic["platform"]

    if platform_name in job_platform_dict:
        return job_platform_dict[platform_name]["write_json_file"](dic)


def get_content_dict_list(url_list):
    dict_list = []
    for url in url_list:
        platform = get_platform(url)
        content_dict = {"url": url, "content": None, "platform": platform}

        if platform:
            if job_platform_dict[platform]["request_supported"]:
                content_dict["content"] = get_content(url)

        dict_list.append(content_dict)

    return dict_list


def get_platform(url):
    for platform in job_platform_dict.keys():
        if platform in url:
            return platform

    return None
