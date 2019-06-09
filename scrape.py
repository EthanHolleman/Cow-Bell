import requests
import urllib.request
import os
from bs4 import *

url = 'https://www.cattle-exchange.com'


def scrape():
    breedList = []
    headList = []
    counter = 0

    req = requests.get(url)  # requests the cattle exchange homepage
    homePage = BeautifulSoup(req.text, 'html.parser')
    breeds = (homePage.find("ul", {"class": "views-summary"})).contents

    for b in breeds:
        # creates list of urls for all breed listings
        stringer = str(b)
        if "breeds" in stringer:
            list = stringer.split('"')
            breedList.append(url+list[1])

    for breed in breedList:
        # requests all breed pages to get listings
        reqCow = requests.get(breed)
        breedPage = BeautifulSoup(reqCow.text, 'html.parser')
        listings = breedPage.find_all("div", {"class": "field-content"})

        for list in listings:
            # collects links to each listing on the breedpage

            entry = (str(list)).split('"')
            headList.append(url+entry[3])
            counter += 1
            if counter % 25 == 0:
                print("Number listings = " + str(counter))

    return headList


def get_listings_text(headList):

    with open("Listings.txt", "w") as listings:
        entries = []
        for head in headList:
            # requests each listing page and gets listing info
            reqHead = requests.get(head)
            headPage = BeautifulSoup(reqHead.text, 'html.parser')
            info = headPage.find_all("div", {"class": "field-item even"})

            splitA = (str(info)).split(">")
            splitB = (str(info).split(">p"))
            splitC = (str(info).split("<div"))

            try:
                id = clean(splitA[2])
                name = clean(splitC[3])
                email = clean(splitA[5].split(" ")[2])
                descrip = clean(splitB[-1].split("div")[-2])
                phone = clean(splitC[4].split(">")[1])
                location = clean(splitC[5].split(">")[1])

                entries.append((id, email, phone, location, descrip, head))
                listings.write(id + "," + name + "," + email + "," + phone +
                               "," + location + "," + descrip + ',' + head + "\n")
                print(id + ' ' + email + ' ' + ' ' + location)

            except IndexError:
                continue


def get_listing_image(listing_url):
    images_dir = get_image_dir()

    try:
        req = requests.get(listing_url, headers={'User-Agent': 'Mozilla/5.0'})
        page = BeautifulSoup(req.text, 'html.parser')
        image_html = page.findAll("div", {"class": "gallery-frame"})

        image_link = (str(image_html))
        image_link = image_link.split('src=')[-1]
        image_link = image_link.split('title')[0].replace('"', '')

        if image_link != '[]':
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)

            image_path = os.path.join(images_dir, os.path.basename(listing_url) + '.jpeg')
            urllib.request.urlretrieve(image_link, image_path)

            return image_path

    except urllib2.HTTPError, e:
        checksLogger.error('HTTPError = ' + str(e.code))
    except urllib2.URLError, e:
        checksLogger.error('URLError = ' + str(e.reason))
    except httplib.HTTPException, e:
        checksLogger.error('HTTPException')
    except Exception:
        import traceback
        checksLogger.error('generic exception: ' + traceback.format_exc())


def get_listings_images(headList):
    # ID should be listing number (line number in file) and breed ex 2_american.jpg
    images_dir = get_image_dir()
    for head_url in headList:
        get_listing_image(head_url)


def remove_defualt_cow_images():
    image_dir = get_image_dir()
    defualt_image_size = '16536'

    image_list = os.listdir(image_dir)

    for image in image_list:
        image_path = os.path.join(image_dir, image)
        if str(os.stat(image_path).st_size) == defualt_image_size:
            os.remove(image_path)


def get_image_dir():
    return os.path.join(os.path.dirname(__file__), 'images')


def clean(string):
    replaceList = ["</h5", "</div", "<p>", "</p>", "<h5>", '<br/', 'class="field-item even"',
                   "Listing #: ", ">", "</", ',', '"', '=', '\n']
    for word in replaceList:
        string = string.replace(word, "")
    return string.strip()
