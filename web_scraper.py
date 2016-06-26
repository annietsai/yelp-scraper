# import urllib
from bs4 import BeautifulSoup
from lxml import html
import requests
import time
import sys

PAGE = requests.get('http://www.yelp.com').content
SOUP = BeautifulSoup(PAGE, 'html.parser')

def main():
    """Main function for Yelp Scraper."""

    print('*** Welcome to Yelp Scraper, your Yelp-search aficionado. ***')
    print('At any time if you need help, enter "help" or "-h". If you would like')
    print('to restart your search, enter "start" or "-s". If you would like to')
    print('quit, enter "quit" or "-q".')
    time.sleep(1.5)

    def proceed(cont, counter):
        """Helper function that determines whether or not a search query continues.
        CONT determines whether or not the user wants to continue the request.
        COUNTER determines which question to prompt the user with.
        """
        if counter == 0:
            cont = input('There seem to be no matches to your request. '
                + 'Try again? Enter [y/n].\n>> ')
        elif counter > 0:
            cont = input('Please enter [y/n]\n>> ')

        if cont == 'y':
            return None
        elif cont == 'n':
            restart = 'q'
            while restart != 'y' and restart != 'n':
                restart = input('Would you like to restart your search?\n>> ')
                if restart == 'y':
                    return 'start'
                elif restart == 'n':
                    sys.exit()
                else:
                    print('Please enter [y/n].')
        else:
            counter += 1
            return proceed(cont, counter)

    # fix?? turn into function calls rather than huge while loop in main()
    result = None
    location = None
    i = 0
    while location != True:
        if i == 0:
            location = input('What is your location? Input [city, state] for '
                + 'best results.\n>> ')
        elif i > 0:
            location = input('There seems to be an error; please enter a valid '
                + 'location.\n>> ')
        else:
            print('There are multiple locations matching your search. Please try')
            location = input('inputting [city, state] or [city, country].\n>> ')

        # result = location_f(location)
        # or--> SOUP = new page with location??
        if result NOTVALID: #FIXME (if location not found)
            i = 10
            location = None
            continue
        elif result MULTVALID: #FIXME (if multiple locations matching search)
            i = -10
            location = None
            continue

        search = None
        while search != True:
            search = input('What are you searching for?\n>> ')
            # result = search_f(result, search)
            # or--> SOUP = new page with search
            if result ISVALID: #FIXME (if resulting page has matches)
                break
            search = proceed('q', 0)

            # while cont != 'y' and cont != 'n':
            #     if j == 0:
            #         cont = input('There seem to be no matches to your request. Try '
            #             + 'again? Enter [y/n].\n>> ')
            #     if j > 0:
            #         cont = input('Please enter [y/n].\n>> ')
            #     if cont == 'y':
            #         search = False
            #         break
            #     elif cont == 'n':
            #         restart = 'q'
            #         while restart != 'y' and restart != 'n':
            #             restart = input('Would you like to restart your search?\n>> ')
            #             if restart == 'y':
            #                 location = False
            #                 search = True
            #                 break
            #             elif restart == 'n':
            #                 sys.exit()
            #             else:
            #                 print('Please enter [y/n].')
            #     else:
            #         j += 1
        if search == 'start':
            location = None
            i = 0
            continue

        price = None
        j = 0
        while price != True:
            if j == 0:
                price = input('What is your price range? \n>> ')
            elif j > 0:
                price = input('There seems to be an error; please enter a valid '
                    + 'price range in the format "[lower] to [upper]" or '
                    + '"[lower]-[upper]".\n>> ')
            # parse price for $__ to $__ or $__-$__
            lower_bound = price[0] #FIXME
            upper_bound = price[1] #FIXME
            try:
                # if type(lower_bound) != int or type(upper_bound) != int:
                    # j += 1
                    # continue
                if lower_bound < 0 or lower_bound > upper_bound:
                    j += 1
                    continue
            except TypeError: # fix? catch any error for not numerals
                j += 1
                continue
            # result = price_f(result, price)
            # or--> SOUP = new page with price
            if result ISVALID: #FIXME (if resulting page has matches)
                if result ISNULL:
                    price = proceed('q', 0)
        if price == 'start':
            location = None
            i = 0
            continue

        quality = None
        k = 0
        while quality != True:
            if k == 0:
                quality = input('What is your target quality range? Please enter '
                    + 'a number 1 through 4.\n>> ')
            elif k > 0:
                quality = input('There seems to be an error; please enter a number '
                    + '1 through 4.\n>> ')
            try:
                if quality < 1 or quality > 4:
                    k += 1
                    continue
            except TypeError: # fix?
                k += 1
                continue
            # result = quality_f(result, quality)
            # or--> SOUP = new page with quality
            if result ISVALID:
                if result ISNULL:
                    quality = proceed('q', 0)
        if quality == 'start':
            location = None
            i = 0
            continue

        reviews = None
        l = 0
        while reviews != True:
            if l == 0:
                reviews = input('At least how many customer reviews would you like '
                    + 'on this request?\n>> ')
            elif l > 0:
                reviews = input('There seems to be an error; please enter a valid '
                    + 'number.\n>> ')
            try:
                if reviews < 0:
                    l += 1
                    continue
            except TypeError: # fix?
                l += 1
                continue
            # result = reviews_f(result, reviews)
            # or--> SOUP = new page with reviews
            if result ISVALID:
                if result ISNULL:
                    reviews = proceed('q', 0)
        if reviews == 'start':
            location = None
            i = 0
            continue

    return result
    

def location_f(loc):
    """Parses SOUP to find all results matching LOC."""


def search_f(results, search_request):
    """Looks at RESULTS to find all results matching SEARCH_REQUEST."""
    # may need to change RESULTS to next SOUP page


def price_f(results, price_range):
    """Parses PRICE_RANGE to find all results in RESULTS matching that
    range.
    """
    # change RESULTS to next SOUP page?


def quality_f(results, quality_range):
    """Looks at RESULTS to find all results matching QUALITY_RANGE."""
    # change RESULTS to next SOUP page?


def reviews_f(results, reviews_range):
    """Looks at RESULTS to find all results matching REVIEWS_RANGE."""
    # change RESULTS to next SOUP page?


main()
