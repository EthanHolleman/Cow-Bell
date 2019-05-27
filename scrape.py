import requests
from bs4 import *
url = 'https://www.cattle-exchange.com/'

def scrape():
    breedList = []
    headList = []
    entries = []
    counter = 0

    req = requests.get(url) #requests the cattle exchange homepage
    homePage = BeautifulSoup(req.text, 'html.parser')
    breeds = (homePage.find("ul", {"class" : "views-summary"})).contents


    for b in breeds:
        #creates list of urls for all breed listings
        stringer = str(b)
        if "breeds" in stringer:
            list = stringer.split('"')
            breedList.append(url+list[1])


    for breed in breedList:
        #requests all breed pages to get listings
        reqCow = requests.get(breed)
        breedPage = BeautifulSoup(reqCow.text, 'html.parser')
        listings = breedPage.find_all("div", {"class" : "field-content"})


        for list in listings:
            #collects links to each listing on the breedpage
            if counter % 25 == 0: print("Number listings = " + str(counter))
            entry = (str(list)).split('"')
            headList.append(url+entry[3])
            counter += 1

    with open("Listings.txt", "w") as listings:


        for head in headList:
            #requests each listing page and gets listing info
            reqHead = requests.get(head)
            headPage = BeautifulSoup(reqHead.text, 'html.parser')
            info = headPage.find_all("div", {"class" : "field-item even"})

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
                listings.write(id + "," + name + "," + email + "," + phone + "," + location + "," + descrip +','+ head + "\n")
                print(id + ' ' + email + ' ' + ' ' + ' ' + location)

            except IndexError:
                continue


def clean(string):
    replaceList = ["</h5","</div","<p>","</p>","<h5>",'<br/','class="field-item even"',
                    "Listing #: ",">","</", ',','"', '=','\n']
    for word in replaceList:
        string = string.replace(word,"")
    return string.strip()
