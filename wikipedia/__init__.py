import logging
import optparse
import urllib2
import simplejson as js
import locale
from locale import gettext as _
locale.textdomain('wikipedia')

from singlet.lens import SingleScopeLens, IconViewCategory, ListViewCategory

from wikipedia import wikipediaconfig

class WikipediaLens(SingleScopeLens):
    wiki="https://ajax.googleapis.com/ajax/services/search/web?v=2.0&q="
    url="https://www.imdb.com/title/"
    class Meta:
        name = 'wikipedia'
        description = 'Wikipedia Lens'
        search_hint = 'Search google'
        icon = 'wikipedia.svg'
        search_on_blank=True

    # TODO: Add your categories
    articles_category = ListViewCategory("Articles from Google", 'dialog-information-symbolic')
    articles1_category=ListViewCategory("Articles from Imdb", 'dialog-information-symbolic')
    def wikipedia_query(self,search):
	try:
		#search=search.replace(" "," ")
		url = ("%s%s" % (self.wiki, search))
		results=js.loads(urllib2.urlopen(url).read())
		print "Searching google for %s"% (search)
		print url
		return results['responseData']['results']
	except:
		return []
    def imdb_query(self,search):
	try:
		url="http://www.omdbapi.com/?t="+search
		results=js.loads(urllib2.urlopen(url).read())
		print type(results)
		return results
	except:
		return {}
    def search(self, search, results):
        # TODO: Add your search results
	for article in self.wikipedia_query(search):
		results.append("%s" % (article['unescapedUrl']),
                    "http://www.meganga.com/wp-content/uploads/2014/01/chrome-icon-150x150.jpg",
                    self.articles_category,
                    "text/html",
                    article['content'],
                    "Wikipedia Article",
                    "%s" % (article['unescapedUrl']))
	pass
	for article in self.imdb_query(search):
		results.append("%s" % (self.url+article['imdbID']),
                    "http://www.meganga.com/wp-content/uploads/2014/01/chrome-icon-150x150.jpg",
                    self.articles1_category,
                    "text/html",
                    article['Title'],
                    "IMDB Article",
                    "%s" % (self.url+article['imdbID']))
	pass
	
