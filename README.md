Yelp Scraper
============

What is it?
-----------

Yelp Scraper is a webscraper that collects query information from the user
and finds Yelp search results that match the user's input. The program then
opens up a maximum specified number of Yelp webpages in web browsers that
correspond to the given information.

Installation
------------

Yelp Scraper requires that the user have Beautiful Soup installed. There are
many simple ways of installation:

1. If you run Debian or Ubuntu, you can install Beautiful Soup with the system
package manager:  
    `$ apt-get install python-bs4`
2. Beautiful Soup 4 is published through Pypi, so if you can't install it with
the system packager, you can install it with `easy_install` or `pip`:  
    `$ easy_install beautifulsoup4`  
    `$ pip install beautifulsoup4`
3. If you don't have `easy_install` or `pip` installed, you can [download](https://www.crummy.com/software/BeautifulSoup/bs4/download/4.0/)
the Beautiful Soup 4 tarball and install it with `setup.py`:  
    `$ python setup.py install`

For more information, click [here](https://www.crummy.com/software/BeautifulSoup/bs4/doc/).

Usage
-----

After downloading the file from Github, run the program in the directory in
which the file is saved using:  
    `$ python3 web_scraper.py`  
Because the program opens up to the maximum number of Yelp webpage search
results requested by the user, take care to limit the number of results
requested in order to protect your computer from lagging or crashing.

A successful run of the program may look like this:  

    ```
    *** Welcome to Yelp Scraper, your Yelp-search aficionado. ***  
    At any time if you would like to restart your search, enter "start"  
    or "-s". If you would like to quit, enter "quit" or "-q".  
    What is your location? Input [city, state] for best results.  
    >> berkeley  
    What are you searching for?  
    >> food  
    What is your price range? Please enter input in the format  
    "[lower] to [upper]" or "[lower]-[upper]".  
    >> 0-50  
    What is the maximum number of results you would like to show?  
    >> 3  
    What is your target minimum rating? Please enter a number  
    0 through 5.  
    >> 4  
    At least how many customer reviews would you like on this request?  
    >> 1000  
    Found 3 results.
    ```

The webpages should automatically open in your browser.

Authors
-------

Annie Tsai
