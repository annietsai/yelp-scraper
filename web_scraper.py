from bs4 import BeautifulSoup
import webbrowser
import requests
import time
import sys
import re

URL = 'http://www.yelp.com'
SEARCH = '/search?'
START = 'start'
START_SEARCH_AT = '&start='
DEFAULT = 0

def proceed(counter):
    """Determines whether or not a search query continues, restarts, or quits.
    Returns None to continue, 'start' to restart, or exits program to quit.
    COUNTER determines which question to prompt the user with.
    """
    if counter == 0:
        try_again = input('There seem to be no matches to your request. '
                          'Try again?\nEnter [y/n].\n>> ')
    elif counter > 0:
        try_again = input('Please enter [y/n].\n>> ')
    else:
        print('There seem to be no matches to your request. Here are some\n'
              'suggestions on how to improve your search:\n- Search with a '
              'broader price range\n- Search with a lower target minimum '
              'rating\n- Search with a lower minimum of customer reviews')
        try_again = 'n'

    if try_again == 'y':
        return None
    elif try_again == 'n':
        i = DEFAULT
        restart = None
        while restart != 'y' and restart != 'n':
            if i == 0:
                restart = input('Would you like to restart your search? '
                                'Enter [y/n].\n>> ')
            else:
                restart = input('Please enter [y/n].\n>> ')

            if restart == 'y':
                return START
            elif restart == 'n':
                sys.exit()
            else:
                i += 1
    else:
        return proceed(counter + 1)

def string_url_converter(query, string):
    """Takes in a QUERY and converts all spaces to '+'. Returns the string
    'find_STRING=' with the converted query.
    """
    converted_query = re.sub('\s+', '+', query)
    find_url = 'find_' + string + '=' + converted_query
    return find_url

def start_quit_check(string):
    """Checks if the user inputted a STRING to restart the search or quit.
    Returns None to continue, 'start' to restart, or exits program to quit.
    """
    if string == 'start' or string == '-s':
        return START
    elif string == 'quit' or string == '-q':
        sys.exit()
    return None

def main_content(url):
    """Takes in a URL and parses HTML for corresponding webpage. Returns the path
    to the main content of the webpage.
    """
    page = requests.get(url).content
    soup = BeautifulSoup(page, 'html.parser')
    return soup.body.select('#wrap')[0].select('.main-content-wrap--full')[0]

def result_soup(url, query):
    """Takes in a string URL and returns text associated with whether or not the
    webpage corresponding to that url has any results. The QUERY determines which
    path to take.
    """
    content = main_content(url)
    if query == 'location':
        try:
            result = content.select('#super-container')[0]\
                            .select('.container')[0]\
                            .select('.search-exception')[0]\
                            .select('.column-alpha')[0]\
                            .select('.content')[0].h2.getText()
        except:
            result = ''
    else:
        result = content.select('.top-shelf-grey')[0]\
                        .select('.content-container')[0]\
                        .select('.search-page-top')[0]\
                        .select('.column-alpha')[0]\
                        .select('.clearfix')[0].h1.getText()
    return result

def price_category_url(price_low, price_high):
    """Takes in a lower bound price range PRICE_LOW and an upper bound price
    range PRICE_HIGH and creates a url snippet corresponding to the appropriate
    price category. Returns this url snippet accompanied with the price category
    bounds represented in number of dollar signs on Yelp.
    """
    price_url = '&attrs='
    one_dollar_sign = 10
    two_dollar_sign = 30
    three_dollar_sign = 60
    low_dollars = 1
    high_dollars = 1

    if price_low <= one_dollar_sign:
        price_url += 'RestaurantsPriceRange2.1'

    if price_high > one_dollar_sign and price_low <= two_dollar_sign:
        price_url += ',RestaurantsPriceRange2.2'
        if price_low > one_dollar_sign:
            low_dollars = 2
        high_dollars = 2

    if price_high > two_dollar_sign and price_low <= three_dollar_sign:
        price_url += ',RestaurantsPriceRange2.3'
        if price_low > two_dollar_sign:
            low_dollars = 3
        high_dollars = 3

    if price_high > three_dollar_sign:
        price_url += ',RestaurantsPriceRange2.4'
        if price_low > three_dollar_sign:
            low_dollars = 4
        high_dollars = 4

    return price_url, low_dollars, high_dollars

def find_results(url, quality, reviews, maximum, search, attrs, low_dollars,
                 high_dollars):
    """Looks at the webpage at URL to find all results matching the user's requested
    QUALITY and REVIEWS. Returns the MAXIMUM number of results or less. SEARCH provides
    the url string before '/start?' and ATTRS provifes the url string after '/start?'.
    LOW_DOLLARS is the lower bound of the target price range category and HIGH_DOLLARS
    is the upper bound of the target price range category. Returns a list of urls for
    webpages that correspond to the user's search qualifications.
    """
    results = []
    item_number = DEFAULT
    while len(results) < maximum:
        content = main_content(url)
        try:
            businesses = content.select('#super-container')[0]\
                                .select('.container')[0]\
                                .select('.search-results-block')[0]\
                                .select('.column-alpha')[0]\
                                .select('.indexed-biz-archive')[0]\
                                .select('.search-results-content')[0]
        except:
            break

        try:
            businesses.select('.no-results')[0]
            break
        except:
            businesses = businesses.select('ul .regular-search-result')

        for biz in businesses:
            biz_info = biz.select('.natural-search-result')[0]\
                          .select('.biz-listing-large')[0]\
                          .select('.main-attributes')[0]\
                          .select('.media-block--12')[0]\
                          .select('.media-story')[0]

            try:
                rating = biz_info.select('.biz-rating')[0].select('.rating-large')[0].i
                stars = int(str(rating).split(' ')[2].split('_')[1].strip('"'))
                if quality <= stars:
                    biz_rating_str_lst = biz_info.select('.biz-rating')[0]\
                                                 .span.getText().split(' ')
                    biz_rating_str_lst = [value for value in biz_rating_str_lst if
                                          value != '']
                    biz_rating = int(biz_rating_str_lst[1])

                    if biz_rating >= reviews:
                        price_category = biz_info.select('.price-category')[0]\
                                                 .select('.bullet-after')[0]\
                                                 .select('.price-range')[0].getText()
                        len_price_category = len(price_category)

                        if (len_price_category >= low_dollars
                                and len_price_category <= high_dollars):
                            link = URL + biz_info.h3.span.select('a[href]')[0]['href']
                            results.append(link)
            except:
                pass

        item_number += 10
        url = URL + search + START_SEARCH_AT + str(item_number) + attrs

    bound = max(len(results), maximum)
    if bound > maximum:
        bound = maximum
    return results[:bound]

def location_prompt(counter):
    """Takes in a COUNTER to determine which question to prompt the user with.
    Calls on the search_prompt function and returns the result.
    """
    if counter == 0:
        location = input('What is your location? Input [city, state] for best '
                         'results.\n>> ')
    elif counter > 0:
        location = input('There seems to be an error; please enter a valid '
                         'location.\n>> ')
    else:
        location = input('There are multiple locations matching your search. '
                         'Please try\ninputting [city, state] or [city, country].'
                         '\n>> ')

    if start_quit_check(location) == START:
        return location_prompt(DEFAULT)

    location_url = string_url_converter(location, 'loc')
    new_url = URL + SEARCH + location_url
    result = result_soup(new_url, 'location')

    if 'Sorry' in result:
        return location_prompt(1)
    elif 'found multiple' in result:
        return location_prompt(-1)
    return search_prompt(location_url)

def search_prompt(location_url):
    """Takes in the LOCATION_URL to form the new resulting url after user is
    prompted with search item. Calls on the price_prompt function and returns the
    result.
    """
    search = input('What are you searching for?\n>> ')

    if start_quit_check(search) == START:
        return location_prompt(DEFAULT)

    search_url = string_url_converter(search, 'desc')
    search_location_url = SEARCH + search_url + '&' + location_url
    new_url = URL + SEARCH + search_url + '&' + location_url
    search_result = result_soup(new_url, 'search')

    if 'No Results' not in search_result:
        return price_prompt(search_url, location_url, search_location_url, DEFAULT)

    search = proceed(DEFAULT)
    if search == START:
        return location_prompt(DEFAULT)
    return search_prompt(location_url)

def price_prompt(search_url, location_url, search_location_url, counter):
    """Takes in the SEARCH_URL and LOCATION_URL strings for the corresponding
    search and location information to form a new url based on the user's desired
    price category. COUNTER determines which question to prompt the user with.
    Calls on and passes SEARCH_LOCATION_URL into the num_results_prompt function
    and returns the result.
    """
    new_url = URL + SEARCH + search_url + '&' + location_url
    if counter == 0:
        price = input('What is your price range? Please enter input in the '
                      'format\n"[lower] to [upper]" or "[lower]-[upper]".\n'
                      '>> ')
    else:
        price = input('There seems to be an error; please enter a valid price '
                      'range.\n>> ')

    if start_quit_check(price) == START:
        return location_prompt(DEFAULT)

    price_text = []
    try:
        if 'to' in price:
            price_text = price.split(' ')
            price_text.remove('to')
        elif '-' in price:
            if price.startswith('-'):
                return price_prompt(search_url, location_url, search_location_url,
                                    counter + 1)
            price_text = price.split('-')

        price_text = [string for string in price_text if string != '']
        price_text = [string.replace('$', '') for string in price_text]

        price_low = int(price_text[0])
        price_high = int(price_text[1])
        if price_low < 0 or price_low > price_high:
            return price_prompt(search_url, location_url, search_location_url,
                                counter + 1)

        price_url, low_dollars, high_dollars = price_category_url(price_low,
                                                                  price_high)
        new_url += START_SEARCH_AT + str(DEFAULT) + price_url
    except:
        return price_prompt(search_url, location_url, search_location_url,
                            counter + 1)

    result = result_soup(new_url, 'price')

    if 'No Results' in result:
        price = proceed(DEFAULT)
        if price is None:
            return price_prompt(search_url, location_url, search_location_url,
                                counter)
        if price == START:
            return location_prompt(DEFAULT)
    return num_results_prompt(new_url, search_location_url, price_url,
                              low_dollars, high_dollars, DEFAULT)

def num_results_prompt(url, search_location_url, price_url, low_dollars,
                       high_dollars, counter):
    """Queries user for the maximum number of results on the search. Takes in
    the final URL for the search as well as the SEARCH_LOCATION_URL and PRICE_URL
    to pass into the function quality_prompt. LOW_DOLLARS and HIGH_DOLLARS are
    also passed into quality_prompt. COUNTER determines which question to prompt
    the user with. Calls and returns the result of the quality_prompt function.
    """
    if counter == 0:
        num_results = input('What is the maximum number of results you would '
                            'like to show?\n>> ')
    else:
        num_results = input('There seems to be an error; please enter a valid '
                            'number.\n>> ')

    if start_quit_check(num_results) == START:
        return location_prompt(DEFAULT)

    try:
        num_results_int = int(num_results)
    except:
        return num_results_prompt(url, search_location_url, price_url,
                                  low_dollars, high_dollars, counter + 1)

    return quality_prompt(url, num_results_int, search_location_url,
                          price_url, low_dollars, high_dollars, DEFAULT)

def quality_prompt(url, num_results, search_location_url, price_url,
                   low_dollars, high_dollars, counter):
    """Queries user for the target minimum rating on the search. Takes in the
    final URL for the search as well as the SEARCH_LOCATION_URL and PRICE_URL
    to pass into the function reviews_prompt. NUM_RESULTS, LOW_DOLLARS, and
    HIGH_DOLLARS are also passed into reviews_prompt. COUNTER determines which
    question to prompt the user with. Calls and returns the result of the
    reviews_prompt function.
    """
    if counter == 0:
        quality = input('What is your target minimum rating? Please enter a '
                        'number\n1 through 4.\n>> ')
    else:
        quality = input('There seems to be an error; please enter a number '
                        '1 through 4.\n>> ')

    if start_quit_check(quality) == START:
        return location_prompt(DEFAULT)

    try:
        quality_int = int(quality) #turn to float?
        if quality_int < 1 or quality_int > 4:
            return quality_prompt(url, num_results, search_location_url,
                                  price_url, low_dollars, high_dollars,
                                  counter + 1)
    except:
        return quality_prompt(url, num_results, search_location_url,
                              price_url, low_dollars, high_dollars,
                              counter + 1)

    if quality == START:
        return location_prompt(DEFAULT)
    return reviews_prompt(url, quality_int, num_results,
                          search_location_url, price_url, low_dollars,
                          high_dollars, DEFAULT)

def reviews_prompt(url, quality, num_results, search_location_url,
                   price_url, low_dollars, high_dollars, counter):
    """Queries user for the minimum number of customer reviews on the search.
    Takes in the final URL for the search as well as the SEARCH_LOCATION_URL
    and PRICE_URL to pass into the function find_results. QUALITY, NUM_RESULTS,
    LOW_DOLLARS, and HIGH_DOLLARS are also passed into find_results. COUNTER
    determines which question to prompt the user with. Calls and returns the
    result of the find_results function.
    """
    if counter == 0:
        reviews = input('At least how many customer reviews would you like '
                        'on this request?\n>> ')
    else:
        reviews = input('There seems to be an error; please enter a valid '
                        'number.\n>> ')

    if start_quit_check(reviews) == START:
        return location_prompt(DEFAULT)

    try:
        reviews_int = int(reviews)
        if reviews_int < 0:
            return reviews_prompt(url, quality, num_results, search_location_url,
                                  price_url, low_dollars, high_dollars,
                                  counter + 1)
    except:
        return reviews_prompt(url, quality, num_results, search_location_url,
                              price_url, low_dollars, high_dollars, counter + 1)

    result_lst = find_results(url, quality, reviews_int, num_results,
                              search_location_url, price_url, low_dollars,
                              high_dollars)
    if len(result_lst) == 0:
        reviews = proceed(-1)

    if reviews == START:
        return location_prompt(DEFAULT)
    return result_lst

def main():
    """Main function for Yelp Scraper."""

    print('*** Welcome to Yelp Scraper, your Yelp-search aficionado. ***')
    time.sleep(1)
    print('At any time if you would like to restart your search, enter "start"\n'
          'or "-s". If you would like to quit, enter "quit" or "-q".')
    time.sleep(1.5)

    results = location_prompt(DEFAULT)

    results_len = len(results)
    if results_len == 1:
        print('Found 1 result.')
    else:
        print('Found ' + str(results_len) + ' results.')
    for result in results:
        webbrowser.open(result)

main()
