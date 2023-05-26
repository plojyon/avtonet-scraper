# avtonet-scraper.py
import os
import requests
from bs4 import BeautifulSoup


def get_summaries(page):
    with open("url.txt", "r") as f:
        url = f.read().replace("\t", "").replace("\n", "") + "&stran=" + str(page)
    print(url)
    html_doc = requests.get(url)
    soup = BeautifulSoup(html_doc, "html.parser")

    """
    .GO-Results-Row
        a.stretched-link.href -> .col-12.p-3.GO-Rounded.innertext
        .GO-Results-Naziv.innertext
        .GO-Results-Price.innertext
        table.table
    """

    result_divs = soup.find_all("div", class_="GO-Results-Row")
    results = []
    for result in result_divs:
        details_url = result.find("a", class_="stretched-link").get("href")
        title = result.find("div", class_="GO-Results-Naziv").text
        price = result.find("div", class_="GO-Results-Price").text
        results.append({"title": title, "price": price, "url": details_url})

    return results


def get_details(url):
    details_html_doc = requests.get(url)
    details = BeautifulSoup(details_html_doc, "html.parser")
    return details.find("div", class_="col-12 p-3 GO-Rounded").text



if __name__ == "__main__":
    if not os.path.exists("summaries.txt"):
        summaries = []
        for page in range(1, 5):
            print(f"Getting page {page} ...")
            summaries += get_summaries(page)
        with open("summaries.txt", "w") as f:
            f.write(summaries)

    print("Summaries written.")

    with open("summaries.txt", "r") as f:
        summaries = f.read()
        details = []
        for summary in summaries:
            print(f"Getting details for {summary['title']} ...")    
            details.append({**summary, "details": get_details(summaries)})

        with open("details.txt", "w") as f:
            f.write(details)

    print("Details written.")
