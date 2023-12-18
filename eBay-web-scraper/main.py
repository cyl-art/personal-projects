"""
A web scraper for eBay. This project is tailored to scrape details of the
iphone case search page and can be used to conveniently compare prices and
filter entries based on the desired parameters. The resultant dataset is stored
in the .csv file. The project is written in Python, it uses 'requests' module
for request handling, 'bs4' module for html parsing, and 'pandas' module for
data manipulation.
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd

def get_title(soup: BeautifulSoup) -> str:
    """
    Get the title of the current entry.

    Args:
        soup (BeautifulSoup): parsed html for the current link

    Returns:
        str: title of this entry
    """
    h1 = soup.find("h1", attrs={"class": "x-item-title__mainTitle"})
    span = h1.find("span", attrs={"class": "ux-textspans ux-textspans--BOLD"})
    return span.text

def get_price(soup: BeautifulSoup) -> str:
    """
    Get price for the current entry.

    Args:
        soup (BeautifulSoup): parsed html for the current link

    Returns:
        str: price of this entry
    """
    price_div = soup.find("div", attrs = {"class": "x-price-primary"})
    price_span = price_div.find("span", attrs={"class": "ux-textspans"})
    return price_span.text

def get_condition(soup: BeautifulSoup) -> str:
    """
    Get condition of the current entry.

    Args:
        soup (BeautifulSoup): parsed html for the current link

    Returns:
        str: condition of this entry
    """
    div = soup.find("div", attrs = {"class": "x-item-condition-text"})
    div = div.find("div", attrs={"class": "ux-icon-text"})
    span = div.find("span", attrs={"class": "clipped"})
    return span.text

def main():
    """
    Main function to get initialize request to the main search page, assemble
    links for individual entries, and construct the resultant dataset.
    """
    # main link to the ihpone cases search page
    url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p4432023.m570.l1313&_nkw=iphone+cases&_sacat=0"

    # headers for https request
    headers = ({"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
                "accept-language": "en-US, en;q=0.5"})
    # https request
    page = requests.get(url, headers=headers, timeout=10)
    print("Main search page received.")

    # parse the server response
    soup = BeautifulSoup(page.text, "html.parser")

    # get all links from the page
    links_info = soup.find_all("a", attrs={"class" :"s-item__link", "_sp": "p2351460.m1686.l7400"})
    links = [link.get("href") for link in links_info]
    info = {"Title": [], "Price": [], "Condition": []}

    # scrape required information from each link
    for link in links:
        web_page = requests.get(link, headers=headers, timeout=10)
        new_soup = BeautifulSoup(web_page.text, "html.parser")

        info["Title"].append(get_title(new_soup))
        info["Condition"].append(get_condition(new_soup))
        info["Price"].append(get_price(new_soup))

    # create dataset
    df = pd.DataFrame.from_dict(info)
    df.to_csv("test.csv", header=True, index=False)
    print("Finished creating the dataset.")

if __name__ == "__main__":
    main()
