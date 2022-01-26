from dataclasses import dataclass
import requests
import json
import csv
from datetime import datetime
import matplotlib.pylab as plt


@dataclass
class ScriptTag:
    contents: str


def _find_final_script_tag(content: str) -> ScriptTag:
    script_start = content.rfind("<script")
    content_start = content.find(">", script_start)
    script_end = content.rfind("</script>")

    return ScriptTag(contents=content[content_start + 1 : script_end])


def _find_current_price_from_script_tag(scriptTag: ScriptTag):
    """Dig through some nested JSON woop woop!"""
    content = json.loads(scriptTag.contents)

    # two keys we want the one thats not "ROOT_QUERY"
    property_key = [
        key
        for key in content["props"]["pageProps"]["initialApolloState"].keys()
        if key != "ROOT_QUERY"
    ][0]

    current_price = content["props"]["pageProps"]["initialApolloState"][property_key][
        "details"
    ]["estimate"]["sale"]["currentPrice"]
    return current_price


def update_data(price: int):
    today = datetime.today().strftime("%Y-%m-%d")

    with open("data.csv", "a") as csvfile:
        fieldnames = ["date", "price"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({"date": today, "price": price})


def draw_and_export():
    with open("data.csv") as csvfile:
        fieldnames = ["date", "price"]
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        content = [r for r in reader]

    x = [r["date"] for r in content]
    y = [int(r["price"]) for r in content]
    plt.figure(figsize=(15, 10))

    plt.plot(x, y)
    plt.xlabel("date")
    plt.ylabel("estimated price")
    plt.title("Zoopla Property Estimate")

    plt.savefig("out.png")


def main(property_uprn: str):
    r = requests.get(
        f"https://www.zoopla.co.uk/property/uprn/{property_uprn}/",
        headers={"accept": "application/json"},
    )
    content = r.text
    tag = _find_final_script_tag(content)
    current_price = _find_current_price_from_script_tag(tag)
    update_data(current_price)


if __name__ == "__main__":
    main()
    
