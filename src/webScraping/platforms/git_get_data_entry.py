from webScraping.utils.get_soup import get_soup, get_content_soup
from webScraping.utils.get_encoded_id import get_encoded_id
from webScraping.utils.data_structure_template import database_structure_template
from webScraping.utils.create_data_json import create_data_json
from webScraping.utils.check_existence import json_file_exists
import json


def git_create_jobfile(dic):
    soup = get_content_soup(dic["content"])
    url = dic["url"]
    platform = dic["platform"]
    if not json_file_exists(url, platform):
        data_entry = git_create_data_entry(url, soup)
        print("Writing json file ...")
        create_data_json(data_entry, platform)
    else:
        print(f"Jobfile already exists for {url}")


def git_get_data_entry(dic):
    soup = get_content_soup(dic["content"])
    url = dic["url"]
    data_entry = git_create_data_entry(url, soup)
    return data_entry


def git_create_data_entry(url, soup):
    print(f"Getting content from {url} and converting data ...")
    data_entry = database_structure_template
    data_entry["id"] = get_encoded_id(url)
    data_entry["jobLink"] = url
    data_entry.update(git_get_jobhead_information(soup, data_entry))
    data_entry.update(git_get_json(soup, data_entry))
    # data_entry.update(git_get_job_description(soup, data_entry))
    return data_entry


def git_get_jobhead_information(data, template):
    jobhead = data.select("[class*='JobHeaderRegular']")
    checklist = ["jobTitle", "jobLocation", "homeOffice"]
    for item in jobhead:
        for entry in checklist:
            if entry in item["class"][0]:
                if entry == "homeOffice":
                    if item.text == "Home-Office":
                        template[entry] = True
                    else:
                        template[entry] = False
                else:
                    template[entry] = item.text
    return template


def git_get_job_description(data, template):
    div_container = data.select_one("div[class*='JobDescription_jobDescription']")
    sections = div_container.find_all("section")

    if div_container:
        jobdescription = []
        for item in sections:
            h2 = item.find("h2")
            if h2:
                next_element = h2.find_next_sibling()
                content_text = ""

                if next_element == "li":
                    content_text += "- " + next_element.text
                else:
                    content_text += next_element.text
                entry = {"title": h2.text, "description": content_text}
                jobdescription.append(entry)
        template["jobDescription"] = jobdescription

    return template


def git_get_json(data, template):
    json_content = data.select("script[type='application/ld+json']")

    if json_content:
        for content in json_content:
            json_string = content.string
            json_data = json.loads(json_string)

        checklist = [
            # "datePosted",
            "directApply",
            "employmentType",
            "hiringOrganization",
            "skills",
        ]

        for item in checklist:
            if item == "hiringOrganization":
                item_container = json_data.get(item, {})
                template["companyInfos"]["name"] = item_container.get("name")
                template["companyInfos"]["website"] = item_container.get("url")
            elif item == "skills":
                template["qualifications"] = json_data.get(item, {})
            else:
                template[item] = json_data.get(item, {})

        template["companyInfos"]["branch"] = git_get_additional_company_infos(data)
    return template


def git_get_additional_company_infos(data):
    job_company_info_site = data.select_one("a[class*='JobContact_button']").get("href")
    if job_company_info_site:
        company_info_soup = get_soup("https://www.get-in-it.de" + job_company_info_site)

        top_fact_container = company_info_soup.select("div[class*='TopFact_body'] li")
        basic_fact_container = company_info_soup.select(
            "div[class*='BasicFact_body'] li"
        )

        if top_fact_container:
            branch = ", ".join(item.text for item in top_fact_container)
        elif basic_fact_container:
            branch = ", ".join(item.text for item in basic_fact_container)
        else:
            branch = ""

        return branch
