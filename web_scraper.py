# import urllib
from bs4 import BeautifulSoup
from lxml import html
import requests
import time
import sys

# url = "http://www.yelp.com"
PAGE = requests.get('http://www.yelp.com').content
SOUP = BeautifulSoup(PAGE, 'html.parser')

def main():
    """Main function for Yelp Scraper."""
    print('*** Welcome to Yelp Scraper, your Yelp-search aficionado. ***')
    print('At any time if you need help, enter "help" or "-h". If you would like')
    print('to restart your search, enter "start" or "-s". If you would like to')
    print('quit, enter "quit" or "-q".')
    time.sleep(1.5)
    location = False
    i = 0
    while location == False:
        if i == 0:
            location = input('What is your location?\n>> ')
        if i > 0:
            location = input('There seems to be an error; please enter a valid '
                + 'location.\n>> ')
        # do the search using location
        if location != 'berkeley': #FIXME (if location not found)
            i += 1
            location = False
            continue;
        # result = locate(location)
        # or--> SOUP = new page with location??
        search = input('What are you searching for?\n>> ')
        while search != 'dinner': #FIXME (if search not found)
            cont = 'q'
            j = 0
            while cont != 'y' and cont != 'n':
                if j == 0:
                    cont = input('There seem to be no matches to your request. Try '
                        + 'again? Enter [y/n].\n>> ')
                if j > 0:
                    cont = input('Please enter [y/n].\n>> ')
                if cont == 'y':
                    search = input('What are you searching for?\n>> ')
                elif cont == 'n':
                    restart = 'q'
                    while restart != 'y' and restart != 'n':
                        restart = input('Would you like to restart your search?\n>> ')
                        if restart == 'y':
                            location = False
                            search = 'dinner' #FIXME (= False)
                            break
                        elif restart == 'n':
                            sys.exit()
                        else:
                            print('Please enter [y/n].')
                else:
                    j += 1

    # result = searcher(result, search) # move before while loop?



def locate(loc):
    """Parses SOUP to find all results matching LOC."""


def searcher(loc_results, search_req):
    """Parses loc_results to find all results matching SEARCH_REQ."""
    # may need to change loc_results to next SOUP page

main()
