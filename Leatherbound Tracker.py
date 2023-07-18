from math import prod
import requests
from bs4 import BeautifulSoup


url = "https://www.dragonsteelbooks.com/collections/leatherbound-books"


SignedYN = ""
go = True


def check_articles(url):
    
    bookavailability = "Leatherbound Availability \n"

    page = requests.get(url)
    

    # Makes sure that the page will load before extracting HTML from the webpage
    if page.status_code != 200:
        raise ValueError
    soup = BeautifulSoup(page.content, 'html.parser') # Parses through html
    counter = soup.find_all("div", {"class": "o-layout__item u-1/1 u-1/2@phab u-1/3@tab"}) #Provides the length counter as well as Sold Out information
    Pics = soup.find_all("div", {"class": "o-ratio__content"}) # Retrieves the photo data of the HTML code (Used to determine SIGNED vs UNSIGNED)


    # Iterates through the html of products to retrieve information
    for i in range(len(counter)):


        # Retrieves the Book Title
        title_obj = soup.find_all("h3", {"class": "product-card__title f-family--heading f-caps--true f-space--1"})[i]
      
        book_title = title_obj.text
        

        # Retrieves Availability.   
        isSoldOut = counter[i].findChild("p", {"class":"product-card__label-text label__text"})
        if isSoldOut is not None:
            isSO_bool = True
        else:
            isSO_bool = False
     
        
       
       # Checks whether copies are SIGNED or UNSIGNED
        Text = Pics[i].findChild("img", {"class":"product-card__img js-img-grid"})
        if "UNSIGNED" in str(Text):
            unsignedbool = True
        else:
            unsignedbool = False
               

        # Determines output of Soldout vs Available. Also informs if copy is SIGNED vs UNSIGNED
        if isSO_bool:
            if unsignedbool:
                bookavailability += "A(n) UNSIGNED copy of {} is still SOLD OUT... \n".format(book_title)
            else:
                bookavailability += "A(n) SIGNED copy of {} is still SOLD OUT...\n".format(book_title)
        else: 
            if unsignedbool:
                bookavailability += "A(n) UNSIGNED copy of {} is AVAILABLE, RUN! \n".format(book_title)
            else:
                bookavailability += "A(n) SIGNED copy of {} is AVAILABLE, RUN! \n".format(book_title)

    return bookavailability

print(check_articles(url))