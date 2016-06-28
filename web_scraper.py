from bs4 import BeautifulSoup
# from lxml import html
import requests
import time
import sys
import re

URL = 'http://www.yelp.com'
# PAGE = requests.get(URL).content
# SOUP = BeautifulSoup(PAGE, 'html.parser')

def main():
    """Main function for Yelp Scraper."""

    print('*** Welcome to Yelp Scraper, your Yelp-search aficionado. ***')
    print('At any time if you would like to restart your search, enter "start"')
    print('or "-s". If you would like to quit, enter "quit" or "-q".')
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
            cont = input('Please enter [y/n].\n>> ')

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
            return proceed(cont, counter + 1)

    def startquit(string):
        """Helper function that checks if user inputted a STRING to restart the search
        or quit.
        """
        if string == 'start' or string == '-s':
            return 'start'
        elif string == 'quit' or string == '-q':
            sys.exit()
        return None

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

        if startquit(location) == 'start':
            i = 0
            location = None
            continue

        location = re.sub('\s+', '+', location)
        loc_url = 'find_loc=' + location
        new_url = URL + 'search?' + loc_url
        page = requests.get(new_url).content
        soup = BeautifulSoup(page, 'html.parser')
        result = soup.body.select('#wrap')[0].select('.main-content-wrap--full')[0]
        result = result.select('.top-shelf-grey')[0].select('.content-container')[0]
        result = result.select('.search-page-top')[0].select('.column-alpha')[0]
        result = result.select('.clearfix')[0].h1.getText()

        if 'No Results' in result:
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

            if startquit(search) == 'start':
                break

            search = re.sub('\s+', '+', search)
            search_url = 'find_desc=' + search
            new_url = URL + 'search?' + search_url + '&' + loc_url

            if result ISVALID: #FIXME (if resulting page has matches)
                break
            search = proceed('q', 0)

        if search == 'start':
            location = None
            i = 0
            continue

        price = None
        j = 0
        while price != True:
            if j == 0:
                print('What is your price range? Please enter input in the format')
                price = input('"[lower] to [upper]" or "[lower]-[upper]".\n>> ')
            elif j > 0:
                new_url = URL + 'search?' + search_url + '&' + loc_url
                price = input('There seems to be an error; please enter a valid price '
                    + 'range.\n>> ')

            if startquit(price) == 'start':
                break

            price_lst = []
            if 'to' in price:
                price_lst = price.split(' ')
                price_lst.remove('to')
            elif '-' in price:
                price_lst = price.split('-')
            price_lst[:] = (value for value in price_lst if value != '')
            price_lst = ([p.replace('$', '') for p in price_lst])

            try:
                lower_bound = int(price_lst[0])
                upper_bound = int(price_lst[1])
                if lower_bound < 0 or lower_bound > upper_bound:
                    j += 1
                    continue
                new_url = new_url + '&start=0&attrs='
                if upper_bound <= 10:
                    new_url = new_url + 'RestaurantsPriceRange2.1,'
                if upper_bound <= 30:
                    new_url = new_url + 'RestaurantsPriceRange2.2,'
                if upper_bound <= 60:
                    new_url = new_url + 'RestaurantsPriceRange2.3,'
                if lower_bound > 60:
                    new_url = new_url + 'RestaurantsPriceRange2.4,'
            except:
                j += 1
                continue

            if result ISVALID: #FIXME (if resulting page has matches)
                if result ISNULL:
                    price = proceed('q', 0)

        if price == 'start':
            location = None
            i = 0
            continue

        quality = None
        k = 0
        old_url = new_url
        while quality != True:
            if k == 0:
                print('What is your target ratings range? Please enter a number')
                quality = input('1 through 4.\n>> ')
            elif k > 0:
                new_url = old_url
                quality = input('There seems to be an error; please enter a number '
                    + '1 through 4.\n>> ')

            if startquit(quality) == 'start':
                break

            try:
                if quality < 1 or quality > 4:
                    k += 1
                    continue
            except:
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

            if startquit(reviews) == 'start':
                break

            try:
                if reviews < 0:
                    l += 1
                    continue
            except: # fix?
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

        num_results = input('How many results would you like to show?\n>> ')
        if startquit(num_results) == 'start':
            location = None
            i = 0
            continue

        # for loop to show this many results

    return result
    


def quality_f(results, quality_range):
    """Looks at RESULTS to find all results matching QUALITY_RANGE."""
    # change RESULTS to next SOUP page?


def reviews_f(results, reviews_range):
    """Looks at RESULTS to find all results matching REVIEWS_RANGE."""
    # change RESULTS to next SOUP page?


main()

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
