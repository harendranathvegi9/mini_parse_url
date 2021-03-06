import re
from tld import get_tld

MAX_URL_LEN = 1000
MIN_URL_LEN = 4

class URLParsed(object):
    """
    Returns parsed URL with attributes:
    
    subdomain
    suffix
    tld
    domain
    path
    local (bool)

    """
    def get_subdomain(self):
        try:
            sub = get_tld(self.url, as_object=True).subdomain
            if sub and len(sub):
                return sub
            return None
        except:
            return None

    def get_suffix(self):
        try:
            suffix = get_tld(self.url, as_object=True).suffix
            if suffix and len(suffix):
                return suffix
        except:
            return None

    def parse_tld(self):
        try:
            parsed = get_tld(self.url, as_object=True)
            if parsed.suffix and len(parsed.suffix):
                return parsed.tld
            return None
        except:
            return None

    def get_domain(self):
        if self.subdomain and len(self.subdomain):
            return self.subdomain + '.' + self.tld
        elif self.tld and len(self.tld):
            return self.tld
        return None

    def get_path(self):
        """
        Appends local '/' where doesn't exist

        """
        try:
            path = self.original.rsplit(self.domain,1)[1]
        except AttributeError:
            return None
        except:
            path = self.original.rsplit(self.domain,1)[0]

        if len(path):
            if path[:1] != '/':
                return '/' + path
            return path
        return None

    def get_path_list(self):
        """
        Returns list of elements in the path
        Removes query string

        """
        try:
            str_path = self.path.strip('/').split('/')
        except:
            return None

        # if it exists, assign query string and strip it
        last_elem = str_path[-1]

        # if it's a query string, strip and return it
        if '?' in last_elem:
            position = last_elem.find('?')
            last_path_elem = last_elem[:position]
            self.query_string = last_elem[position+1:] # remove '?'
            return str_path[:-1] + [last_path_elem]
            # TODO add query string parser to dict

        return str_path

    def get_local(self):
        return False if self.domain else True

    def sanitize_url(self, url=None):
        """
        Remove non-link '/' edge case urls
        add 'http://' for tld parsing trickery

        - javascript
        - urls longer than 1000 chars
        - urls shorter than 4 chars

        """
        str_url = url.strip() # strip whitespace
        # outlying cases
        if len(str_url) > MAX_URL_LEN or len(str_url) < MIN_URL_LEN or str_url[:10] == 'javascript':
            return None
        elif str_url[:4] != 'http':
            return 'http://' + str_url
        return str_url

    def __init__(self, url, test=False):
        self.original = url # store original url but process sanitized url
        self.url = self.sanitize_url(url)
        self.subdomain = None
        self.suffix = None
        self.tld = None
        self.domain = None
        self.path = None
        self.local = None
        self.path_list = None
        self.query_string = None

        if self.url:
            self.subdomain = self.get_subdomain()
            self.suffix = self.get_suffix()
            self.tld = self.parse_tld()
            self.domain = self.get_domain()
            self.path = self.get_path()
            self.local = self.get_local()
            self.query_string = None
            self.path_list = self.get_path_list()

        if test:
            print 'url: ', self.url
            print 'subdomain: ', self.subdomain
            print 'suffix: ', self.suffix
            print 'tld: ', self.tld
            print 'domain: ', self.domain
            print 'path: ', self.path
            print 'local: ', self.local
            print 'path_list: ', self.path_list
            print 'query_string: ', self.query_string
