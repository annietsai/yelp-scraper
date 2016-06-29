from bs4 import BeautifulSoup
import webbrowser
import requests
import time
import sys
import re

URL = 'http://www.yelp.com'

def proceed(counter):
    """Determines whether or not a search query continues. COUNTER determines
    which question to prompt the user with.
    """
    if counter == 0:
        cont = input('There seem to be no matches to your request. '
            + 'Try again? Enter [y/n].\n>> ')
    else:
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
        return proceed(counter + 1)

def startquit(string):
    """Checks if the user inputted a STRING to restart the search or quit."""
    if string == 'start' or string == '-s':
        return 'start'
    elif string == 'quit' or string == '-q':
        sys.exit()
    return None

def result_soup(url, query):
    """Takes in a string URL and turns it into soup, which is then dissected
    to find particular strings. The QUERY determines which path to take.
    """
    page = requests.get(url).content
    soup = BeautifulSoup(page, 'html.parser')
    main_content = soup.body.select('#wrap')[0].select('.main-content-wrap--full')[0]
    if query == 'location':
        try:
            result = main_content.select('#super-container')[0]\
                .select('.container')[0].select('.search-exception')[0]\
                .select('.column-alpha')[0].select('.content')[0].h2.getText()
        except:
            result = 'ok'
    else:
        result = main_content.select('.top-shelf-grey')[0]\
            .select('.content-container')[0].select('.search-page-top')[0]\
            .select('.column-alpha')[0].select('.clearfix')[0].h1.getText()
    return result

def quality_f(url, quality, reviews, maximum, search, attrs):
    """Looks at URL to find all results matching QUALITY and REVIEWS. Returns the
    MAXIMUM number of results or less. SEARCH provides the url text before 'start?'
    and ATTRS provifes the url text after 'start?'.
    """
    results = []
    i = 0
    while len(results) < int(maximum):
        page = requests.get(url).content
        soup = BeautifulSoup(page, 'html.parser')
        main_content = soup.body.select('#wrap')[0].select('.main-content-wrap--full')[0]

        businesses = main_content.select('#super-container')[0]\
            .select('.container')[0].select('.search-results-block')[0]\
            .select('.column-alpha')[0].select('.indexed-biz-archive')[0]\
            .select('.search-results-content')[0]
        try:
            businesses = businesses.select('.no-results')[0]
            break
        except:
            businesses = businesses.select('ul .regular-search-result')

        for biz in businesses:
            biz_info = biz.select('.natural-search-result')[0]\
                .select('.biz-listing-large')[0].select('.main-attributes')[0]\
                .select('.media-block--12')[0].select('.media-story')[0]

            try:
                rating = biz_info.select('.biz-rating')[0].select('.rating-large')[0].i
                stars = str(rating).split(' ')[2].split('_')[1].strip('"')
                if int(quality) <= int(stars):
                    biz_rating = biz_info.select('.biz-rating')[0].span.getText()
                    rating_num = biz_rating.split(' ')
                    rating_num[:] = (value for value in rating_num if value != '')

                    if int(rating_num[1]) >= int(reviews):
                        link = URL + biz_info.h3.span.select('a[href]')[0]['href']
                        results.append(link)
            except:
                pass

        i += 10
        url = URL + search + '&start=' + str(i) + attrs

    bound = max(len(results), int(maximum))
    if bound > int(maximum):
        bound = int(maximum)
    return results[:bound]

def main():
    """Main function for Yelp Scraper."""

    print('*** Welcome to Yelp Scraper, your Yelp-search aficionado. ***')
    time.sleep(1)
    print('At any time if you would like to restart your search, enter "start"')
    print('or "-s". If you would like to quit, enter "quit" or "-q".')
    time.sleep(1.5)

    i = 0
    location = None
    while location is None:
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
        new_url = URL + '/search?' + loc_url
        result = result_soup(new_url, 'location')

        if 'Sorry' in result:
            i = 10
            location = None
            continue
        elif 'found multiple' in result:
            i = -10
            location = None
            continue

        search = None
        while search is None:
            search = input('What are you searching for?\n>> ')

            if startquit(search) == 'start':
                search = 'start'
                break

            search = re.sub('\s+', '+', search)
            search_url = 'find_desc=' + search
            new_url = URL + '/search?' + search_url + '&' + loc_url
            result = result_soup(new_url, 'search')

            if 'No Results' not in result:
                break
            search = proceed(0)

        if search == 'start':
            i = 0
            location = None
            continue

        j = 0
        price = None
        while price is None:
            if j == 0:
                print('What is your price range? Please enter input in the format')
                price = input('"[lower] to [upper]" or "[lower]-[upper]".\n>> ')
            else:
                new_url = URL + '/search?' + search_url + '&' + loc_url
                price = input('There seems to be an error; please enter a valid price '
                    + 'range.\n>> ')

            if startquit(price) == 'start':
                price = 'start'
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
                    price = None
                    continue
                price_url = '&attrs='
                if lower_bound <= 10:
                    price_url = price_url + 'RestaurantsPriceRange2.1,'
                if upper_bound > 10 and lower_bound <= 30:
                    price_url = price_url + 'RestaurantsPriceRange2.2,'
                if upper_bound > 30 and lower_bound <= 60:
                    price_url = price_url + 'RestaurantsPriceRange2.3,'
                if upper_bound > 60:
                    price_url = price_url + 'RestaurantsPriceRange2.4,'
                new_url = new_url + '&start=0' + price_url
            except:
                j += 1
                price = None
                continue

            result = result_soup(new_url, 'price')

            if 'No Results' in result:
                price = proceed(0)
                if price is None:
                    j = 0

        if price == 'start':
            i = 0
            location = None
            continue

        k = 0
        num_results = None
        while num_results is None:
            if k == 0:
                num_results = input('What is the maximum number of results you would '
                    + 'like to show?\n>> ')
            else:
                num_results = input('There seems to be an error; please enter a valid '
                    + 'number.\n>> ')

            if startquit(num_results) == 'start':
                num_results = 'start'
                break

            try:
                int(num_results)
            except:
                num_results = None
                k += 1
                continue

        if num_results == 'start':
            i = 0
            location = None
            continue

        l = 0
        quality = None
        while quality is None:
            if l == 0:
                quality = input('What is your target minimum rating? Please enter '
                    + 'a number 1 through 4.\n>> ')
            else:
                quality = input('There seems to be an error; please enter a number '
                    + '1 through 4.\n>> ')

            if startquit(quality) == 'start':
                quality = 'start'
                break

            try:
                if int(quality) < 1 or int(quality) > 4:
                    l += 1
                    quality = None
                    continue
            except:
                l += 1
                quality = None
                continue

        if quality == 'start':
            i = 0
            location = None
            continue

        m = 0
        reviews = None
        while reviews is None:
            if m == 0:
                reviews = input('At least how many customer reviews would you like '
                    + 'on this request?\n>> ')
            else:
                reviews = input('There seems to be an error; please enter a valid '
                    + 'number.\n>> ')

            if startquit(reviews) == 'start':
                reviews = 'start'
                break

            try:
                if int(reviews) < 0:
                    m += 1
                    reviews = None
                    continue
            except:
                m += 1
                reviews = None
                continue

            search_location_url = '/search?' + search_url + '&' + loc_url
            result_lst = quality_f(new_url, quality, reviews, num_results,
                search_location_url, price_url)
            if len(result_lst) == 0:
                reviews = proceed(0)
                if reviews is None:
                    m = 0

        if reviews == 'start':
            i = 0
            location = None
            continue

    print('Found ' + str(len(result_lst)) + ' results.')
    for r in result_lst:
        webbrowser.open(r)

main()
