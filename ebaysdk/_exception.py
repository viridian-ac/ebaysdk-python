# -*- coding: utf-8 -*-


class EbayError(Exception):

    def __init__(self, msg, response=None):
        super(EbayError, self).__init__(u'%s' % msg)
        self.message = u'%s' % msg
        self.response = response

    def __str__(self):
        return repr(self.message)


class ConnectionError(EbayError):
    pass


class ConnectionConfigError(EbayError):
    pass


class ConnectionResponseError(EbayError):
    pass


class RequestPaginationError(EbayError):
    pass


class PaginationLimit(EbayError):
    pass
