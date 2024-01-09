'''Run as:
        > python walmart_scraper.py filepath

        or even
        > python walmart_scraper.py filepath --output mycart.csv
'''

import json
import typer
import sys
import csv
from decimal import Decimal
from bs4 import BeautifulSoup

def parse_price(price_string):
        price_string = price_string.removesuffix("/ea").removeprefix("$")
        if price_string.endswith("¢"):
                price_string = "0." + price_string.removesuffix("¢").zfill(2)
        return Decimal(price_string)

def main(filepath: str,
         output: str = typer.Option(None, help="Path to save output csv file."),
         """
         Scrape your Voila order from a saved html file at FILEPATH.
         Visit your cart and save the website an html file.
         """

        if output is not None:
                sys.stdout = open(output, "w")

        with open(filepath) as fp:
                soup = BeautifulSoup(fp, 'html5lib')

        writer = csv.DictWriter(sys.stdout, fieldnames=["Quantity","Name","Link","Price Each","Price Subtotal","Savings"])
        writer.writeheader()

        cart = soup.find(attrs={"data-testid": "product-tile-container"}).find("ul")
        
        for item in cart.children:

                linktag = item.find("a", {"link-identifier": "itemClick"})

                eachpricestr = item.find("div", {"data-testid": "productDescription"}).text
                eachprice = parse_price(eachpricestr)
                
                discountedpricetag = item.find(attrs={"data-testid": "item-price"})
                discountedprice = parse_price(discountedpricetag.string) if discountedpricetag \
                        else None

                actualprice = discountedprice or eachprice

                subtotalstr = item.find("div", {"class": "ml-auto"}).find("span").string
                subtotal = parse_price(subtotalstr)
                
                quantitystepper = item.find(attrs={"data-testid": "quantity-stepper"})
                quantitytag = quantitystepper.find("button").next_sibling
                quantity = int(quantitytag.string)

                savings = quantity * (eachprice - actualprice)
                assert(savings >= 0)

                writer.writerow({
                        "Quantity": str(quantity),
                        "Name": linktag.text,
                        "Link": linktag.get("href"),
                        "Price Each": actualprice,
                        "Price Subtotal": subtotal,
                        "Savings": str(savings) if savings else ""
                })

        writer.writerow({})
        for feeitem in soup.find_all(attrs={"data-testid": "fee"}):
                feetype = feeitem.string
                amount = parse_price(feeitem.next_sibling.string)
                writer.writerow({
                        "Name": feetype,
                        "Price Subtotal": amount
                })


if __name__ == "__main__":
        typer.run(main)
