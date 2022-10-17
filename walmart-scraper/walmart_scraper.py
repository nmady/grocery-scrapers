'''Run as:
	> python walmart_scraper.py filepath

	or even
	> python walmart_scraper.py filepath --output mycart.csv
''' 

import json
import typer
import sys
import csv
from bs4 import BeautifulSoup

def convert_possible_cents(price_string):
	if price_string[-1] == u'\xa2':
		encoded = price_string.encode("ascii", "ignore")
		decoded = encoded.decode()
		return '0.' + str(decoded).zfill(2)
	else:
		return price_string
	

def main(filepath: str,
	output: str = typer.Option(None, help="Path to save output csv file."),
	debug: bool = typer.Option(False, help="If True, prints the JSON file instead.")):
	"""
    Scrape your Voila order from a saved html file at FILEPATH.
    Visit your cart and save the website an html file.

    """

	if output is not None:
		sys.stdout = open(output, "w")


	with open(filepath) as fp:
	    soup = BeautifulSoup(fp, 'html.parser')

	writer = csv.DictWriter(sys.stdout, fieldnames=["Quantity","Name","Link","Price Each","Price Subtotal","CRF","Deposit"])
	writer.writeheader()
	
	cart = soup.find(attrs={"data-automation": "active-cart"})
	
	for row in cart.find_all(attrs={"data-automation": "product-item-row"}):

		item = row.parent
		
		quantitytag = item.find(attrs={"data-automation": "quantity"})
		quantity = int(quantitytag.input.get("value"))

		linktag = item.find(attrs={"data-automation": "product-item-title"})

		eachpricetag = (item.find(attrs={"data-automation": "product-each-price-with-savings"}) or
				item.find(attrs={"data-automation": "product-each-price"}))

		subtotalpricetag = (item.find(attrs={"data-automation": "product-subtotal-price-with-savings"}) or
				    item.find(attrs={"data-automation": "product-subtotal-price"}))

		pricetag = eachpricetag
		if not pricetag:
			assert quantity == 1
			pricetag = subtotalpricetag

		crftag = item.find(attrs={"data-automation": "CRF"})
		deptag = item.find(attrs={"data-automation": "Bev. Deposit"})

		writer.writerow({
			"Quantity": str(quantity),
			"Name": linktag.string,
			"Link": linktag.get("href"),
			"Price Each": convert_possible_cents(pricetag.string),
			"Price Subtotal": convert_possible_cents(subtotalpricetag.string),
			"CRF": convert_possible_cents(crftag.string) if crftag else "",
			"Deposit": convert_possible_cents(deptag.string) if deptag else ""
		})


if __name__ == "__main__":
    typer.run(main)
