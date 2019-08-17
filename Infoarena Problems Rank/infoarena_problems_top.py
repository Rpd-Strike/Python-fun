import numpy as np
from bs4 import BeautifulSoup as bs4
import requests, functools, operator, colorama, datetime, time
import traceback as tb

class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def my_print(string, toFile = 0):
	print(string)
	if toFile != 0:
		fo.write(string.encode('utf_8'))

def pune_data(offset, batches, batch_size):
	my_print("As of " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\n", 1)
	my_print("Jobs checked from " + str(offset + 1) + " to " + str(offset + batches * batch_size) + "\n\n", 1)
	my_print("   The top problems are:\n", 1)

def get_query_url(start, end):
	### recommended to have |start - end| <= 250
	url = "https://" + "infoarena.ro/monitor?job_begin=" + str(start) + "&job_end=" + str(end) + "&display_entries=250&score_begin=100"
	return url

def afiseaza(my_sorted_list, runda):
	my_print("Problem count: " + str(len(clasamente[runda])) + "\n\n", 1)
	for i, key in enumerate(my_sorted_list):
		my_print(str(i + 1) + ": " + key + " - " + str(len(clasamente[runda][key])) + "\n", 1)

def process(the_top, runda):
	my_print("\n\n ---->  " + runda + "\n", 1)
	my_sorted_list = sorted(the_top, key = lambda k: len(the_top[k]), reverse = True)
	afiseaza(my_sorted_list, runda)


def adauga(start, end):
	global nr_of_wrongs
	global clasamente
	nr_entries = 0

	my_print(BColors.WARNING + "job list: " + str(start) + " - " + str(end) + BColors.ENDC)

	r = requests.get(get_query_url(start, end))
	webtext = r.text
	soup = bs4(webtext, "lxml")

	table = soup.find("table", {"class" : "monitor"})
	if table is None:
		my_print(BColors.FAIL + "Monitor table missing\n" + BColors.ENDC)
		return

	table = table.find("tbody")
	if table is None:
		my_print(BColors.FAIL + "Monitor table missing\n" + BColors.ENDC)
		return 

	rows = table.findAll("tr")

	for _, row in enumerate(rows):
		data = row.findAll("td")
		if len(data) < 3:
			continue

		problema = ""
		username = ""
		runda = ""
		bad_problem = 0
		for i, cell in enumerate(data):
			#print(cell.prettify())
			if i == 1:
				username = cell.findAll("a")[1].text

			if i == 2:
				my_a_tag = cell.find("a")
				if not hasattr(my_a_tag, 'text'):
					print(BColors.FAIL + "Getting problem name on " + str(i + 1) + " -th td i have this: ")
					print(cell.prettify() + BColors.ENDC)
				else:
					problema = my_a_tag.text
				
				if problema == "":
					bad_problem = 1
			
			if i == 3:
				runda = cell.find("a").text
				#print("Problema " + problema + " este in " + runda)

		if runda not in clasamente:
			clasamente[runda] = dict()

		if problema not in clasamente[runda]:
			clasamente[runda][problema] = {username : 1}
		else:
			clasamente[runda][problema][username] = 1

		nr_entries += 1
		nr_of_wrongs += bad_problem

	colMsg = BColors.OKGREEN
	if r.status_code == 404:
		colMsg = BColors.FAIL

	my_print(colMsg + "I got this status code: " + str(r.status_code) + BColors.ENDC)

	my_print("nr_entries: " + str(nr_entries))
	my_print("nr_of_wrongs: " + str(nr_of_wrongs) + "\n")

clasamente = dict()
fo = open("top_problems.txt", "wb")
nr_of_wrongs = 0

def main():
	start_time = time.time()

	colorama.init()

	my_print(BColors.HEADER + "Opening message" + BColors.ENDC)

	batch_size = 250 # Maximum amount allowed by infoarena on a single monitor page
	batches = 10000  # just make sure batch_size * batches is more than the amount of submissions xD
	offset = 0       # go figure

	for i in range(offset + 1, offset + batches * batch_size, batch_size):
		print(BColors.BOLD + "Batch " + str(i // batch_size + 1) + "/" + str(batches))
		adauga(i, i + batch_size - 1)

	pune_data(offset, batches, batch_size)

	print(clasamente)

	for key in clasamente:
		process(clasamente[key], key)

	my_print(BColors.OKBLUE + "\nYou can also check the file top_problems.txt\n" + BColors.ENDC)

	my_print("Total time taken for this amazing work: " + str(datetime.timedelta(seconds = time.time() - start_time)), 1)

	fo.close()

if __name__ == "__main__":
	main()
