__author__ = 'Marnee Dearman'


class GraphLabel.Component(object):
    def process_request(self, req, resp):
        """process the request.  check for token status and access restrictions
        should I check restrictions here?  I dunno
        what should happen if the user is not authorized -- change the uri?
        req.uri
        """
        # if (access_restricted()):


def access_restricted():
    return True
