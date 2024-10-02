from webScraping.utils.get_soup import get_content_soup
from webScraping.utils.get_encoded_id import get_encoded_id
from webScraping.utils.create_data_json import create_data_json
from webScraping.utils.check_existence import json_file_exists
from webScraping.utils.data_structure_template import database_structure_template
import json


def idd_create_jobfile(dic):
    soup = get_content_soup(dic["content"])
    url = dic["url"]
    platform = dic["platform"]
    if not json_file_exists(url, platform):
        data_entry = idd_create_data_entry(url, soup)
        print("Writing json file ...")
        create_data_json(data_entry, platform)
    else:
        print(f"Jobfile already exists for {url}")


def idd_get_data_entry(dic):
    soup = get_content_soup(dic["content"])
    url = dic["url"]
    data_entry = idd_create_data_entry(url, soup)
    return data_entry


def idd_create_data_entry(url, soup):
    print(f"Getting content from {url} and converting data ...")
    data_entry = database_structure_template
    data_entry["id"] = get_encoded_id(url)
    data_entry["jobLink"] = url
    data_entry["qualifications"] = idd_get_skills(soup)
    data_entry = idd_get_json(soup, data_entry)
    return data_entry


# Content Verarbeitung
def idd_get_job_description(data):
    pass


def idd_get_skills(data):
    qualifications = []
    missing_skills_container = data.select(
        "div[aria-label=Fähigkeiten] button[aria-label*='Fehlende Qualifikation']"
    )

    if missing_skills_container:
        for missing_skill in missing_skills_container:
            qualifications.append(missing_skill.text)

    matching_skills_container = data.select(
        "div[aria-label=Fähigkeiten] button[aria-label*='Passende Qualifikation'] div > div:nth-child(2)"
    )

    if matching_skills_container:
        for matching_skill in matching_skills_container:
            qualifications.append(matching_skill.text)

    return qualifications


def idd_get_json(data, template):
    json_content = data.select("script[type='application/ld+json']")

    if json_content:
        for content in json_content:
            json_string = content.string
            json_data = json.loads(json_string)

        checklist = [
            "title",
            # "datePosted",
            "directApply",
            "jobLocation",
        ]

        for item in checklist:
            if item == "title":
                template["jobTitle"] = json_data.get(item)
            elif item == "jobLocation":
                template["jobLocation"] = json_data[item]["address"]["addressLocality"]
            else:
                template[item] = json_data.get(item)

        if "hiringOrganization" in json_data:
            item_container = json_data["hiringOrganization"]
            template["companyInfos"]["name"] = item_container.get("name")

        homeOffice_text, employmentType_text = idd_get_missing_data(data)

        data_head = {
            "homeOffice": "homeoffice" in homeOffice_text.lower()
            if homeOffice_text
            else False,
            "employmentType": employmentType_text or "",
        }

        template.update(data_head)

        return template

    else:
        return idd_get_data_without_json(data, template)


def idd_get_missing_data(data):
    homeOffice = data.select_one("[data-testid*='inlineHeader-companyName']")

    if not homeOffice:
        homeOffice = data.select_one(
            "[data-testid='jobsearch-JobInfoHeader-companyLocation']"
        )
    else:
        homeOffice = homeOffice.parent.find_next_sibling()

    employmentType = data.select_one("[id='salaryInfoAndJobType']")

    homeOffice_text = homeOffice.text if homeOffice else ""
    employmentType_text = employmentType.text if employmentType else ""

    return homeOffice_text, employmentType_text


def idd_get_data_without_json(data, template):
    jobTitel = data.select_one("[data-testid='jobsearch-JobInfoHeader-title']")
    companyName = data.select_one("[data-testid='inlineHeader-companyName']")
    jobLocation = data.select_one(
        "[data-testid='jobsearch-JobInfoHeader-companyLocation']"
    )
    homeOffice, employmentType = idd_get_missing_data(data)

    data_head = {
        "jobTitle": jobTitel.text if jobTitel else "",
        "homeOffice": True if "homeoffice" in homeOffice.text.lower() else False,
        "jobLocation": jobLocation.text if jobLocation else "",
        "employmentType": employmentType.text if employmentType else "",
        "directApply": False,
    }

    data_company = {"companyInfos": {"name": companyName.text if companyName else ""}}

    template.update(data_head)
    template["companyInfos"].update(data_company["companyInfos"])

    return template
