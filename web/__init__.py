import tornado.web

from web.pages.root import RootHandler
from web.pages.new_app import NewAppHandler
from web.pages.gen_app import GenAppHandler


def make_app():
    return tornado.web.Application([
        (r'/', RootHandler),
        (r'/new_app', NewAppHandler),
        (r'/gen_app', GenAppHandler),
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': 'web_logger/pages/static'}),
    ], debug=True)
