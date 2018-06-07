import sys, os, requests
import smtplib
from bs4 import BeautifulSoup
from HuurwoningenScraper.smtp import send_mail

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
        print(url + " => Request succeeded: returned " + str(response.status_code))

        # Use BeatifulSoup to parse the HTML response
        soup = BeautifulSoup(response.text, "html.parser")

        results = []

        # Huurwoningen.nl made it pretty easy to fetch items from the their search results.
        # The class 'listing' gets passed to every item, so that's what we should use to query the response!
        soup_results = soup.findAll("section", attrs={"class": "listing"})
        
        for i in range (0, len(soup_results)):
            if i == 5: # TODO: add a MaxResults ini variable? 
               break

            results.append(SearchResult(soup_results[i]))

        # TODO: Check if there is a backlog for the chosen min/max values, and compare the last registered result with the scraper result
        send_mail(results, config)
    else:
        print(url + " => Request failed: returned " + str(response.status_code))
        exit(0)


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

