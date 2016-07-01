                            Yelp Scraper

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
the system packager, you can install it with `easy-install` or `pip`:
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

Authors
-------

Annie Tsai
