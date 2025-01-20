import ebaysdk
from ebaysdk.finding import Connection

api = Connection(
    siteid='EBAY-DE',
    domain="svcs.sandbox.ebay.com",  # "'svcs.ebay.com',  # domain='svcs.sandbox.ebay.com',
    appid='johannwe-test-SBX-e6628eb6f-5aa814cb',
    config_file=None)

request = {
    'keywords': "iPhone",
    'itemFilter': [
        {'name': 'Condition', 'value': 'Used'},
    ]
}


response = api.execute('findItemsByKeywords', request)

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
    ...