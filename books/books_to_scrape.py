import requests
from bs4 import BeautifulSoup
from csv import DictWriter

def raw_data(url):
    response=requests.get(url)
    return response.content.decode()

def parsed_data():
    base_url="https://books.toscrape.com/"
    page_url=""
    name_price=[]
    page="catalogue/"
    while (True):
        response=raw_data(base_url+page_url)
        soup=BeautifulSoup(response,"html.parser")
        books=soup.select(".product_pod")
        for book in books:
            book_name=book.select_one('h3 a')['title']
            book_price=book.select_one(".price_color").text
            name_price.append({"book_name":book_name,"book_price":book_price})
        try:
            page_url=soup.select_one("li.next a")["href"]
            if (page_url == "catalogue/page-2.html"):
                page_url=soup.select_one("li.next a")["href"]
            else:
                page_url=page+page_url
        except TypeError:
            break
    return name_price
        
def main():
    parsed=parsed_data()
    with open("books.csv","w") as file:
        writer= DictWriter(file,fieldnames=["book_name","book_price"])
        writer.writeheader()
        for i in parsed:
            writer.writerow(i)

if __name__ == "__main__":
    main()