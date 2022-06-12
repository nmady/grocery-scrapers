'''Run as:
	> python walmart_scraper.py filepath

	or even
	> python walmart_scraper.py filepath --output mycart.csv
''' 

import json
import typer
import sys
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

	print("Quantity,Name,Link,Price Each,Price Subtotal,CRF,Deposit")

	for tag in soup.find_all(class_="css-z0lw7w enc9ah80"):
		quantitytag = tag.find(attrs={"data-automation":"quantity"})
		quantity = quantitytag.input.get('value')
		print(quantity + ",", end="")
		linktag = tag.find(attrs={"data-automation":"product-item-title"})
		print(linktag.string.replace(',','') + ',', end="")
		print(linktag.get('href') + ',', end="")
		eachpricetag = tag.find(class_="css-6a8gpu esdkp3p2")
		subtotalpricetag = tag.find(class_="css-s3vnpn esdkp3p2")
		if eachpricetag is not None:
			print(convert_possible_cents(eachpricetag.span.string) + ',', end="")
		elif int(quantity) == 1:
			print(convert_possible_cents(subtotalpricetag.span.string) + ',', end="")
		else:
			print("Error!", quantity, type(quantity) + ',', end="")
		print(convert_possible_cents(subtotalpricetag.span.string) + ',', end="")
		crftag = tag.find(attrs={"data-automation":"CRF"})
		if crftag is not None:
			print(convert_possible_cents(crftag.string) + ',', end="")
		else:
			print("0,", end="")
		deptag = tag.find(attrs={"data-automation":"Bev. Deposit"})
		if deptag is not None:
			print(convert_possible_cents(deptag.string) + ',', end="")
		else:
			print("0,", end="")
		print()


if __name__ == "__main__":
    typer.run(main)