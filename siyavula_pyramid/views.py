from pyramid.view import (
    view_config,
    view_defaults
)

from .wiki_toc import Wiki


@view_defaults(renderer='templates/home.jinja2')
class WikiViews:

    def __init__(self, request):
        self.request = request
        self.view_name = 'WikiViews'

    @view_config(route_name='home')
    def home(self):
        """
        Root view
        """
        return {'project': 'siyavula_pyramid'}

    @view_config(
        route_name='content',
        request_method='POST',
        renderer='templates/content.jinja2')
    def content(self):
        """
        This view accepts a post request and
        sends back a wiki table of content or
        an error message.
        """
        wiki_url = self.request.POST.get('wiki_url')
        wiki = Wiki()
        links = wiki.get_toc(wiki_url)
        if 'error' not in links.keys():
            return {'toc': links}
        return {
            'error_message': links['error']
        }
