import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

data_table = {
    "title": [],
    "type": [],
    "issue": [],
    "date": [],
}

page_num = 1

while True:
    print(f"Scraping page {page_num} ...")
    response = requests.get(f"https://trumpwhitehouse.archives.gov/news/page/{page_num}")
    
    if response.status_code != 200:
        print("Ending...")
        break
    
    soup = BeautifulSoup(response.content, "html.parser")

    for article in soup.find_all("article"):
        article_class = article["class"][0]
        type_ = article.find("p", class_=f"{article_class}__type")
        issue_ = article.find("p", class_="issue-flag")

        data_table["title"].append(article.find("h2", class_=f"{article_class}__title").text.strip())
        data_table["type"].append(type_.text.strip() if type_ is not None else "Other")
        data_table["issue"].append(issue_.text.strip() if issue_ is not None else "Other")
        data_table["date"].append(article.find("time").text.strip())

        time.sleep(0.5)

    page_num += 1

print(len(data_table["title"]))
print(len(data_table["type"]))
print(len(data_table["issue"]))
print(len(data_table["date"]))

df = pd.DataFrame(data_table)
df.to_csv("white-house-data.csv")
