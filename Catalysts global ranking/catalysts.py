import numpy as np
from bs4 import BeautifulSoup as bs4
import requests, functools

def hh_mm_ss(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

def compare(a, b):
	if a['problems'] > b['problems']:
		return -1
	if a['problems'] < b['problems']:
		return 1
	if a['time'] < b['time']:
		return -1
	return 1

teamsWithProblems = [0] * 10
medals = [0] * 5
namedMedals = {"gold" : 3,
			   "silver" : 2,
			   "bronze" : 1,
			   "" : 0}

print(teamsWithProblems)

allTeams = []

for hub in range(1, 49):

	url = "register.codingcontest.org/contest/1/results?hostId=" + str(hub)

	r = requests.get("https://" + url)

	webtext = r.text

	soup = bs4(webtext, "lxml")

	print("Trying hostId nr: " + str(hub))

	all_rows = soup.find_all("div", {"class" : "row"})

	if len(all_rows) < 1:
		print("Page has no table\n")
		continue

	all_rows = all_rows[0]


	#print(type(all_rows))

	##print(all_rows[1])

	for cell in all_rows.find_all("tr"):
		all_td = cell.find_all("td")

		#print("Lg: " + str( len( all_td)) ) 

		if len(all_td) < 5: 
			continue

		#print("=========================================================\n")

		# print(all_td.text)

		#getting information
		place = int(all_td[0].text)
		team = all_td[1].text
		time = all_td[3].text.strip()
		problems = int(all_td[4].text)

		if time != "-":
			time = hh_mm_ss(time)
		else:
			time = 1e9

		src = all_td[0].find("img", src=True)
		if src is not None:
			src = src['src']
		else:
			src = ""
		medal = max([0] + [namedMedals[ x ] for x in ["bronze", "silver", "gold"] if x in src])

		#updating allTeams
		allTeams.append({"place": place,
						 "team" : team,
						 "time" : time,
						 "problems" : problems,
						 "medal" : medal})

		#aggregate data
		medals[medal] += 1
		teamsWithProblems[problems] += 1

for i in range(10):
	print("Probleme: " + str(i) + "  -  " + str(teamsWithProblems[i]) + " echipe\n")

print("\n")

print("gold medals: " + str(medals[3]) + "\n")
print("silver medals: " + str(medals[2]) + "\n")
print("bronze medals: " + str(medals[1]) + "\n")
print("fraieri: " + str(medals[0]) + "\n")

allTeams = sorted(allTeams, key = functools.cmp_to_key(compare))

message = ""

someTeams = [
	"Game of Threads",
	"retrograd",
	" ⇮ ⇮ ⇮Bronze Promo ⇮ ⇮ ⇮",
	"Flower Power",
	"Tractoristii_ICHB",
	"georgerapeanu"
]

for i, team in enumerate(allTeams):
	if team['team'] in someTeams:
		print(team['team'] + ": Place " + str(i + 1) + "\n")
	#print("problems: " + str(team['problems']) + " - " + str(team['time']) + "\n")