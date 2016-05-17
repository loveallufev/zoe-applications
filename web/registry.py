import tornado.httpclient
import tornado.gen

from web.config import get_conf


@tornado.gen.coroutine
def retrieve_image_list():
    http_client = tornado.httpclient.AsyncHTTPClient()
    res = yield http_client.fetch(get_conf().registry_url + "/v2/_catalog")
    return res
