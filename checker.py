import requests
from bs4 import BeautifulSoup

from redmail import outlook
import pandas as pd
outlook.username = ""
outlook.password = ""


URL = 'https://www.nike.com/t/blazer-mid-77-vintage-mens-shoes-nw30B2/BQ6806-100'


def check_price():
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    price = soup.find("div", {"class": "product-price"}).get_text()
    converted_price = float(price[1:4])
    title = soup.find("h1", {"id": "pdp_product_title"}).get_text()
    csv_dict = {
        'title': [],
        'price': [],
    }
    csv_dict['title'].append(title)
    csv_dict['price'].append(converted_price)
    df = pd.DataFrame(csv_dict)
    df.to_csv('price.csv', index=False)
    # get price from csv
    df = pd.read_csv('price.csv')
    price = df['price'][0]
    title = df['title'][0]
    print(title)
    if (converted_price < price):
        send_mail(title)


def send_mail(title):

    outlook.send(

        subject='Price fell down! for '+title,
        receivers=['www.example@gmail.com'],
        html="""<h1>Hello!</h1>
                <p> The price has dropped</p>
                <a href="https://www.nike.com/t/blazer-mid-77-vintage-mens-shoes-nw30B2/BQ6806-100">Price Dropped!!</a>
        """
    )


check_price()
