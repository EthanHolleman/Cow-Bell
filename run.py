import time, dropbox, os, datetime
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError
from scrape import *
from BellBot import *

listings = 'Listings.txt'
client = dropbox.Dropbox('key')
counter = 0

while True:
    if counter == 3:
        counter = 0
        try:
            print('scraping cattle exchange now')
            listings = scrape()
            print('getting cattle listings')
            get_listings_text(listings)
            print('scrape is complete')
        except:
            print('exception occured')

        # upload to one drive folder
        with open(listings, 'rb') as f:
            dest_path = datetime.datetime.today().strftime('%d-%m-%Y')
            dest_path = '/Cowbell/{}_listings.txt'.format(dest_path)
            try:
                client.files_upload(f.read(),dest_path, mode=WriteMode('add'))
            except ApiError:
                print('API Error occured')

    times = 28800
    print('Seconds to next post')
    while times != 0:
        if times % 900 == 0: print(times)
        time.sleep(1)
        times -= 1
    try:
        post()
        counter += 1
    except:
        print('Post failed')
