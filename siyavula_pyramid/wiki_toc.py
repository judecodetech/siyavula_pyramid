"""
This class implements a wiki method that
accepts a wikipedia url and returns its table
of content.
"""

# import inbuilt python modules first
from collections import defaultdict
from urllib.parse import urlparse

# import third party modules after python modules
from bs4 import BeautifulSoup
from requests import get as request_get
from sortedcontainers import SortedDict


BASE_URL = 'https://en.wikipedia.org/wiki/'


def isfloat(value):
    """
    Returns true if a given value is a float
    otherwise returns false.
    """
    try:
        float(value)
        return True
    except ValueError:
        return False

def map_links(links=None):
    """
    This function maps links into a dictionary,
    in a ul-li format.
    it returns a sorted dictionary of keys
    and values in the following format:

    {
        '1 key': [value1, value2],
        '2 key': [value1]
    }
    """
    links_dict = defaultdict(set)
    link_no = 0
    a_ul = ''
    for link in links:
        split_link = link.text.split()
        for s in split_link:
            if s.isdigit():
                a_ul = link.text
                link_no = int(s)
                links_dict[a_ul]

            for b in link.text.split():
                ul_no = '{}.'.format(link_no)
                if (isfloat(b) and isfloat(b) !=
                        link_no and b.startswith(ul_no)):
                    links_dict[a_ul].add(link.text)

    for key, value in links_dict.items():
        links_dict[key] = sorted(value)

    return SortedDict(links_dict)

class Wiki(object):
    """
    Implements two public methods and one private
    method. All work together to scrape the table
    of content from a wikipedia url.
    """

    def get_toc(self, wiki_url=''):
        """
        toc -- means table of content. It is abbreviated
        to avoid a long method name.

        This method receives a wikipedia url and returns
        it's table of content
        """
        if wiki_url and (not urlparse(wiki_url).scheme):
            wiki_url = "https://" + wiki_url

        invalid_url = 'Invalid Wiki URL: {}'.format(wiki_url)
        error_message = {
            'error': invalid_url
        }

        if BASE_URL in wiki_url:
            # get contents from url
            content = request_get(wiki_url).content
            # get soup
            soup = BeautifulSoup(content, 'lxml')  # choose lxml parser
            # find the tag : <div class="toc">
            tag = soup.find('div', {'class': 'toc'})  # id="toc" also works

            if not tag:
                no_toc = 'The wiki url {} does not have '\
                         'a table of content'.format(wiki_url)
                error_message = {
                    'error': no_toc
                }
            else:
                # get all the links
                links = tag.findAll('a')  # <a href='/path/to/div'>topic</a>
                return map_links(links)
        return error_message
