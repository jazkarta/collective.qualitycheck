import json

from lxml.html import fromstring
from plone import api
from plone.app.linkintegrity.utils import getOutgoingLinks
from Products.CMFPlone.browser.syndication.adapters import SearchFeed
from zope.component import queryMultiAdapter


class QualityCheckContent(BrowserView):

    def __call__(self):

        valid = True
        for link in getOutgoingLinks(self.context):
            state = api.content.get_state(obj=link.to_object, default='published')
            if state != 'published':
                valid = False
                break

        headers_ordered = True

        try:
            feed = SearchFeed(api.portal.get())
            adapter = queryMultiAdapter((self.context, feed), IFeedItem)
            html = adapter.render_content_core().strip()
        except Exception:
            html = ''

        if html:
            dom = fromstring(html)
            last = 1
            for el in dom.cssselect('h1,h2,h3,h4,h5,h6'):
                idx = int(el.tag[-1])
                if idx - last > 1:
                    # means they skipped from say h1 -> h5
                    # h1 -> h2 is allowed
                    headers_ordered = False
                    break
                last = idx

        self.request.response.setHeader('Content-type', 'application/json')
        return json.dumps({
            'title': self.context.Title(),
            'id': self.context.getId(),
            'description': self.context.Description(),
            'linksValid': valid,
            'headersOrdered': headers_ordered,
            'html': html_parser.unescape(html)
        })
