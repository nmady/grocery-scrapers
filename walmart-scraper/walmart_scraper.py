'''Run as:
	> python voila_scraper.py filepath

	or even
	> python voila_scraper.py filepath --output mycart.csv
''' 

import json
import typer
import sys
from bs4 import BeautifulSoup

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

	print("Quantity,Name,Link,Price Each,Price Subtotal")

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
			print(eachpricetag.span.string + ',', end="")
		elif int(quantity) == 1:
			print(subtotalpricetag.span.string + ',', end="")
		else:
			print("Error!", quantity, type(quantity) + ',', end="")
		print(subtotalpricetag.span.string + ',', end="")
		print()

	# for tag in soup.find_all(attrs={"data-automation":"product-item-title"}):
	# 	print(tag)


	# for tag in soup.find_all(attrs={"data-test": "fop-product-link"}):
	# 	# print(tag.parent.parent.parent.prettify())
	# 	# print(tag.parent.parent.parent.parent.find(class_="text__Text-sc-1ddlex6-0 fWseoV"))
	# 	print(tag.parent.parent.parent.parent.find(attrs={"aria-label":"Deposit charge will be applied"}))
	# 	print(tag.parent.parent.parent.find('input')['value'])
	# 	for item in tag.parent.parent.find_all(attrs={"data-test": "fop-price"}):#has_data_test):
	# 		#if item['data-test'] == "fop-price":
	# 		print(item.string)
	# 	origPrice = tag.parent.parent.find(class_="base__StrikethroughPrice-sc-1m8b7ry-32 dLBXqd")
	# 	if origPrice:
	# 		print(origPrice.string)
	# 	else:
	# 		print('NaN')
	# 	print(tag['href'])
	# 	print(tag.string)
	# 	print()





if __name__ == "__main__":
    typer.run(main)