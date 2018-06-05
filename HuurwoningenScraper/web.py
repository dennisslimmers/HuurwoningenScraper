import sys, os, requests
import smtplib
from bs4 import BeautifulSoup
from HuurwoningenScraper.email import send_mail

def init(config):
    """Make the web request and parse the response"""

    try:
        url = config.get_huurwoningen_url(config)
        response = requests.get(url)
    except:
        e = sys.exc_info()[0]
        print(e)
        exit(0)

    if response.status_code == 200:
        # Use BeatifulSoup to parse the HTML response
        soup = BeautifulSoup(response.text, "html.parser")

        # Huurwoningen.nl made it pretty easy to fetch items from the their search results.
        # The id 'first-listing' gets passed to the first item, so that's what we use to query the response!
        result = SearchResult(soup.find("section", attrs={"id": "first-listing"}))

        # TODO: Check if there is a backlog for the chosen min/max values, and compare the last registered result with the scraper result
        send_mail(result)


class SearchResult:
    """Class that represents a Huurwoningen.nl search result (rent, location, link etc)"""

    def __init__(self, soup):
        self.map_html(soup)


    def map_html(self, soup):
        """Use BeautifulSoup to map all the necessary search result values"""

        self.rent = soup.find("span", attrs={"class": "price__value"}).text
        self.dwelling = soup.find("span", attrs={"class": "listing__dwelling"}).text
        self.location = soup.find("span", attrs={"class": "listing-address__city"}).text
        self.street = soup.find("span", attrs={"class": "listing-address__street"}).text
        self.subtitle = soup.find("div", attrs={"class": "listing__subtitle"}).text
        self.description = soup.find("p", attrs={"class": "listing__description"}).text
        self.link = self.get_result_link(soup)

    
    def get_result_link(self, soup):
        pass

