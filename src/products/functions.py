import requests
from bs4 import BeautifulSoup


def extract_information_from_url(url: str):
    company = url.split(".")[1]
    information_class = {"flipkart": {"price": "_30jeq3 _16Jk6d", "title": "B_NuCI"}}

    data = requests.get(url)
    html_content = data.content
    soup = BeautifulSoup(html_content, "html.parser")

    price = soup.find(class_=information_class[company]["price"]).get_text()
    title = soup.find(class_=information_class[company]["title"]).get_text()

    for symbol in ("₹", ","):
        price = price.replace(symbol, "")

    return {"title": str(title), "price": float(price)}
