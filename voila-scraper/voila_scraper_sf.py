'''
Designed for files downloaded with the SingleFile plugin.

Run as:
	> python voila_scraper_sf.py filepath

	or even
	> python voila_scraper_sf.py filepath --output mycart.csv
'''

import json
import typer
import sys
import csv
from bs4 import BeautifulSoup

def main(filepath: str,
	output: str = typer.Option(None, help="Path to save output csv file."),
	debug: bool = typer.Option(False, help="If True, prints the prettified html instead.")):
	"""
    Scrape your Voila order from a saved html file at FILEPATH.
    Visit your cart and save the website using the SingleFile plugin.

    """

	if output is not None:
		sys.stdout = open(output, "w")

	with open(filepath) as fp:
	    soup = BeautifulSoup(fp, 'html.parser')

	writer = csv.DictWriter(sys.stdout, fieldnames=["Quantity","Name","Link","Price Each","Deposit"])
	writer.writeheader()

	if debug:
		print(soup.prettify())
		return

	cart = soup.find(attrs={"data-synthetics": "product-list"})

	for item in cart:

		quantitytag = item.find(attrs={"data-test": "quantity-in-basket"})
		if not quantitytag: continue

		quantity = quantitytag.get("value")

		linktag = item.find(attrs={"data-test": "fop-product-link"})

		eachpricetag = item.find(attrs={"data-test": "fop-price"})

		deptagparent = item.find(attrs={"aria-label": "Deposit charge will be applied"})

		writer.writerow({
			"Quantity": str(quantity),
			"Name": linktag.string,
			"Link": linktag.get("href"),
			"Price Each": eachpricetag.contents[0],
			"Deposit": deptagparent.span.string[9:] if deptagparent else ""
		})


if __name__ == "__main__":
    typer.run(main)
