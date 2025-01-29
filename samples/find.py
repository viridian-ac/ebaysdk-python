import ebaysdk
import os
import sys

from ebaysdk.finding import Connection
from ebaysdk.exception import ConnectionError

sys.path.append('/Applications/XAMPP/xamppfiles/htdocs/')
from paiuva.sdk import VAClassHelper as vach

class Find:

    conn: Connection =None
    request = None

    def __init__(self, domain="svcs.sandbox.ebay.com"):
        vach.Help.curr_callers()


        self.conn = Connection(
            siteid='EBAY-DE',
            domain=domain,  # "'svcs.ebay.com',  # domain='svcs.sandbox.ebay.com',
            appid='johannwe-test-SBX-e6628eb6f-5aa814cb',
            #config_file='ebay.yaml'
            config_file = None)

        self.request = {
            'keywords': "iPhone",
            'itemFilter': [
                {'name': 'Condition', 'value': 'Used'},
            ],
            'MaxEntries': "500"

        }

    def execute(self):

        response = self.conn.execute('findItemsByKeywords', self.request)

        if response.reply.ack == 'Success':
            print(response.reply)
            '''
        
            for item in response.reply.searchResult.item:
                print(
                    f"""
                    Title: {item.title}\n
                    Price: {item.sellingStatus.currentPrice.value} {item.sellingStatus.currentPrice.currencyId}\n
                    Location: {item.location}\n
                    Thumbnail: {item.galleryURL}\n"""
                    )
            '''

if __name__ == "__main__":
    # f= Find("api.ebay.com")
    f = Find()
    f.execute()
