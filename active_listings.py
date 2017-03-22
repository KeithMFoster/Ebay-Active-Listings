import json
import sys
import time
from requests.exceptions import ConnectionError
from ebay_api.ebay_api import EbayAPI
from pprint import pprint

def parse_dict(file_name):
    with open(file_name) as data_file:
            data = json.load(data_file)

    mySku = data['Item']
    for item in mySku:
        print item['ItemID']

def main():
    api = EbayAPI('old_glory')

    try:
        page_number = int(sys.argv[1])
    except:
        page_number = 1

    while True:
        print 'on page {}'.format(str(page_number))

        fname = "active_ebay_inventory_{}.json".format(str(page_number))
        try:
            results = api.get_my_ebay_selling(str(page_number))
        except ConnectionError:
            time.sleep(10)
            results = api.get_my_ebay_selling(str(page_number))

        data = results.dict()


        total_number_of_pages = int(data['ActiveList']['PaginationResult']['TotalNumberOfPages'])
        pretty_json = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

        with open(fname, 'w') as f:
            f.write(pretty_json)

        parse_dict(fname)

        page_number += 1
        if page_number > total_number_of_pages:
            break



if __name__ == "__main__":
    main()

__author__ = 'Dev'
