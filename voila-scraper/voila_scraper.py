'''Run as:
	> python voila_scraper.py filepath

	or even
	> python voila_scraper.py filepath --output mycart.csv
''' 

import json
import typer
import sys

def print_rec_dict(maybe_dict, level=0):
	''' This is a helper function to make it easier to look at the JSON output
	without having to see all of the strings and numbers and stuff 
	
	Inputs:
		maybe_dict: the dictionary you want to print
	'''
	if type(maybe_dict) is dict:
		for key in maybe_dict.keys():
			print("\t"*level + key + ": ")
			print_rec_dict(maybe_dict[key], level=level+1)
	elif type(maybe_dict) is list:
		print("\t"*level + '[]: ')
		for item in maybe_dict:
			print_rec_dict(item, level=level+1)
	else:
		print("\t"*level + str(type(maybe_dict)))

def main(filepath: str,
	output: str = typer.Option(None, help="Path to save output csv file."),
	debug: bool = typer.Option(False, help="If True, prints the JSON file instead.")):
	"""
    Scrape your Voila order from a saved html file at FILEPATH.
    Visit your cart and save the website an html file.

    """

	if output is not None:
		sys.stdout = open(output, "w")

	with open(filepath) as f:
		my_string = f.read()

	keyword = 'JSON.parse('
	pad = len(keyword)
	before = my_string.find(keyword)
	decoder = json.JSONDecoder()
	rep, idx = decoder.raw_decode(my_string[before+pad::])
	my_json = decoder.decode(rep)
	if debug:
		print(json.dumps(my_json, sort_keys=True, indent=4))
	else:
		print('BasketQuantity,BasketSpecQuantity,Name,Link,Price,Offer,OrigPrice,Deposit,')
		for productEntityKey in my_json["data"]["products"]["productEntities"]:
			for item in my_json["data"]["basket"]["items"]:
				if item["productId"] == productEntityKey:
					print(str(item["quantity"]["quantityInBasket"]) + ",", end="")
			for item in my_json["data"]["basketSpeculation"]["items"]:
				if item["productId"] == productEntityKey:
					print(str(item["quantity"]["quantityInBasket"]) + ",", end="")
			productEntity = my_json["data"]["products"]["productEntities"][productEntityKey]
			print(productEntity["name"] + ",", end="")
			print('https://voila.ca/products/' + productEntity["retailerProductId"] + '/details/,', end="")
			print(productEntity["price"]["current"]["amount"] + ',', end="")
			if "offer" in productEntity:
				print(productEntity["offer"]["description"] + ',', end="")
			else:
				print("No sale,", end="")
			if "original" in productEntity["price"]:
				print(productEntity["price"]["original"]["amount"] + ",", end="")
			else:
				print("NaN,", end="")
			if "depositPrice" in productEntity:
				print(productEntity["depositPrice"]["amount"] + ",", end="")
			else:
				print('0.00,', end="")
			print()


if __name__ == "__main__":
    typer.run(main)