import datetime
import os
import sys
from pathlib import Path

# from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection


sys.path.append('/Applications/XAMPP/xamppfiles/htdocs/')
from paiuva.sdk import VAEbayError as ee


try:
    api = Connection(appid='johannwe-test-SBX-e6628eb6f-5aa814cb', config_file='ebay.yaml')

    response = api.execute('findItemsAdvanced', {'keywords': 'legos'})

    assert(response.reply.ack == 'Success')
    assert(type(response.reply.timestamp) == datetime.datetime)
    assert(type(response.reply.searchResult.item) == list)

    item = response.reply.searchResult.item[0]
    assert(type(item.listingInfo.endTime) == datetime.datetime)
    assert(type(response.dict()) == dict)

except ee.ConnectionError as e:
    print(e)
    print(e.response.dict())
