# -*- coding: utf-8 -*-
'''
Copyright 2012-2019 eBay Inc.
Authored by: Tim Keefer
Licensed under CDDL 1.0
'''

import os
import sys
from optparse import OptionParser

sys.path.insert(0, '%s/../' % os.path.dirname(__file__))

from common import dump

import ebaysdk
from ebaysdk.finding import Connection as finding
# from ebaysdk.exception import ConnectionError

sys.path.append('/Applications/XAMPP/xamppfiles/htdocs/')
from paiuva.sdk import VAEbayError as ee

def init_options():
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)

    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug", default=False,
                      help="Enabled debugging [default: %default]")
    parser.add_option("-y", "--yaml",
                      dest="yaml", default='ebay.yaml',
                      help="Specifies the name of the YAML defaults file. [default: %default]")
    parser.add_option("-a", "--appid",
                      dest="appid", default=None,
                      help="Specifies the eBay application id to use.")
    parser.add_option("-n", "--domain",
                      dest="domain", default='svcs.ebay.com',
                      help="Specifies the eBay domain to use (e.g. svcs.sandbox.ebay.com).")
    (opts, args) = parser.parse_args()
    return opts, args


def run(opts):

    try:
        api = finding(debug=opts.debug, appid=opts.appid, domain=opts.domain,
                      config_file=opts.yaml, warnings=True)

        api_request = {
            #'keywords': u'niño',
            'keywords': u'GRAMMY Foundation®',
            'itemFilter': [
                {'name': 'Condition',
                 'value': 'Used'},
                {'name': 'LocatedIn',
                 'value': 'GB'},
            ],
            'affiliate': {'trackingId': 1},
            'sortOrder': 'CountryDescending',
        }

        response = api.execute('findItemsAdvanced', api_request)

        dump(api)
    except ee.ConnectionError as e:
        print(e)
        print(e.response.dict())


def run_unicode(opts):

    try:
        api = finding(debug=opts.debug, appid=opts.appid, domain=opts.domain,
                      config_file=opts.yaml, warnings=True)

        api_request = {
            'keywords': u'Kościół',
        }

        response = api.execute('findItemsAdvanced', api_request)
        for i in response.reply.searchResult.item:
            if i.title.find(u'ś') >= 0:
                print("Matched: %s" % i.title)
                break

        dump(api)

    except ee.ConnectionError as e:
        print(e)
        print(e.response.dict())

if __name__ == "__main__":
    print("Unicode samples for SDK version %s" % ebaysdk.get_version())
    (opts, args) = init_options()
    run_unicode(opts)
