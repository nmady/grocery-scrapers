'''
Designed for files downloaded from S-Kaupat > Tilaukset (save as complete web page).

Run as:
	> python prisma_scraper.py filepath

	or even
	> python prisma_scraper.py filepath --output mycart.csv
'''

import locale
import typer
import sys
import csv
from bs4 import BeautifulSoup

def main(filepath: str,
	output: str = typer.Option(None, help="Path to save output csv file."),
	debug: bool = typer.Option(False, help="If True, prints the prettified html instead.")):
	"""
    Scrape your Prisma order from a saved html file at FILEPATH.

    """
	locale.setlocale(locale.LC_ALL, "fi_FI")

	if output is not None:
		sys.stdout = open(output, "w")

	with open(filepath) as fp:
	    soup = BeautifulSoup(fp, 'html.parser')

	writer = csv.DictWriter(sys.stdout, fieldnames=["Quantity","Name","Total"])
	writer.writeheader()

	if debug:
		print(soup.prettify())
		return

	cart = soup.find(attrs={"class": "sc-49f5fd84-1 gaXFIj"}) # this might need to be changed

	for item in cart:

		quantitytag = item.find(attrs={"data-test-id": "product-item-count"})
		if not quantitytag: continue
		quantity = quantitytag.span.span
		
		titletag = item.find(attrs={"data-test-id": "product-card__orderConfirmation__productName"})
		
		eachpricetag = item.find(attrs={"data-test-id": "product-price__dynamic-unitPrice"})

		writer.writerow({
			"Quantity": quantity.string,
			"Name": titletag.string,
			"Total": locale.atof(eachpricetag.string.split(" ")[0])
		})


if __name__ == "__main__":
    typer.run(main)