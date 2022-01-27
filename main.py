from dataclasses import dataclass
from turtle import update
from github import Github

# import requests
# import json
import csv

# import matplotlib.pylab as plt
import os

from datetime import datetime

IMAGE_NAME = "prices.png"
DATA_NAME = "data.csv"
TODAY = datetime.today().strftime("%Y-%m-%d")


@dataclass
class ScriptTag:
    contents: str


# def _find_final_script_tag(content: str) -> ScriptTag:
#     script_start = content.rfind("<script")
#     content_start = content.find(">", script_start)
#     script_end = content.rfind("</script>")

#     return ScriptTag(contents=content[content_start + 1 : script_end])


# def _find_current_price_from_script_tag(scriptTag: ScriptTag):
#     """Dig through some nested JSON woop woop!"""
#     content = json.loads(scriptTag.contents)

#     # two keys we want the one thats not "ROOT_QUERY"
#     property_key = [
#         key
#         for key in content["props"]["pageProps"]["initialApolloState"].keys()
#         if key != "ROOT_QUERY"
#     ][0]

#     current_price = content["props"]["pageProps"]["initialApolloState"][property_key][
#         "details"
#     ]["estimate"]["sale"]["currentPrice"]
#     return current_price


def update_data(price: int):

    with open(DATA_NAME, "a") as csvfile:
        fieldnames = ["date", "price"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({"date": TODAY, "price": price})


# def _get_data_file_contents() -> list[dict[str, str]]:
#     with open(DATA_NAME) as csvfile:
#         fieldnames = ["date", "price"]
#         reader = csv.DictReader(csvfile, fieldnames=fieldnames)
#         content = [r for r in reader]
#     return content


# def draw_and_export():
#     content = _get_data_file_contents()
#     x = [r["date"] for r in content]
#     y = [int(r["price"]) for r in content]
#     plt.figure(figsize=(15, 10))

#     plt.plot(x, y)
#     plt.xlabel("date")
#     plt.ylabel("estimated price")
#     plt.title("Zoopla Property Estimate")

#     plt.savefig(IMAGE_NAME)


# def verify():
#     # Checks we have an out.png and data for todays date
#     file_present = os.path.exists(IMAGE_NAME)
#     content = _get_data_file_contents()
#     todays_date_present = any(r["date"] == TODAY for r in content)

#     print(f"::set-output name=completed::{file_present and todays_date_present}")

# def get_current_price():
#     property_uprn = os.getenv("INPUT_UPRN")
#     print(f"::set-output name=testOutput::{property_uprn}")

#     r = requests.get(f"https://www.zoopla.co.uk/property/uprn/{property_uprn}/")
#     content = r.text
#     tag = _find_final_script_tag(content)
#     return _find_current_price_from_script_tag(tag)

# def main():

#     current_price = get_current_price()
#     update_data(current_price)
#     draw_and_export()
#     verify()

def update_github():
    token = os.getenv("INPUT_REPO-TOKEN")
    repo_name = os.getenv("GITHUB_REPOSITORY")
    g = Github(token)
    repo = g.get_repo(repo_name)

    update_data(123)
    with open('data.csv', 'r') as f:
        contents = f.read()
    
    repo.create_file("data.csv", TODAY, contents)


if __name__ == "__main__":
    update_github()

    # main()
    
