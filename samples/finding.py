# -*- coding: utf-8 -*-
'''
Copyright 2012-2019 eBay Inc.
Authored by: Tim Keefer
Licensed under CDDL 1.0
'''

import os
import sys
from optparse import OptionParser


sys.path.append('/Applications/XAMPP/xamppfiles/htdocs/')
from paiuva.sdk import VAEbayError as ee

from common import dump

import ebaysdk
from ebaysdk.finding import Connection as finding
# from ebaysdk.exception import ConnectionError


def init_options():

    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)

    # Debug option
    parser.add_option("-d", "--debug", action="store_true",
                      help="Enable debugging [default: %(default)s]", default=False)

    # YAML file option
    parser.add_option("-y", "--yaml", type=str, default='ebay.yaml',
                      help="Specifies the name of the YAML defaults file [default: %(default)s]")

    # App ID option
    parser.add_option("-a", "--appid", type=str, default=None,
                      help="Specifies the eBay application ID to use")

    # Domain option
    parser.add_option("-n", "--domain", type=str, default='svcs.ebay.com',
                      help="Specifies the eBay domain to use (e.g., svcs.sandbox.ebay.com) [default: %(default)s]")

    # Parse arguments
    (opts, args) = parser.parse_args()
    # print(opts)  # {'debug': False, 'yaml': 'ebay.yaml', 'appid': None, 'domain': 'svcs.ebay.com'}
    print(args)  # []
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
    except ConnectionError as e:
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

    except ConnectionError as e:
        print(e)
        print(e.response.dict())


def run2(opts):
    try:
        api = finding(debug=opts.debug, appid=opts.appid, domain=opts.domain,
                      config_file=opts.yaml)

        response = api.execute('findItemsByProduct',
                               '<productId type="ReferenceID">53039031</productId><paginationInput><entriesPerPage>1</entriesPerPage></paginationInput>')

        dump(api)

    except ConnectionError as e:
        print(e)
        print(e.response.dict())


def run_motors(opts):
    api = finding(siteid='EBAY-MOTOR', debug=opts.debug, appid=opts.appid, config_file=opts.yaml,
                  domain=opts.domain, warnings=True)

    api.execute('findItemsAdvanced', {
        'keywords': 'tesla',
    })

    if api.error():
        raise Exception(api.error())

    if api.response_content():
        print("Call Success: %s in length" % len(api.response_content()))

    print("Response code: %s" % api.response_code())
    print("Response DOM: %s" % api.response_dom())

    dictstr = "%s" % api.response_dict()
    print("Response dictionary: %s..." % dictstr[:250])

if __name__ == "__main__":
    print("Finding samples for SDK version %s" % ebaysdk.get_version())
    (opts, args) = init_options()
    run(opts)
    run2(opts)
    run_motors(opts)
    run_unicode(opts)
