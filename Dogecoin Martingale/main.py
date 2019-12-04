# Sets up a browser, plays fkn HI-LO for DOGE COINS

import os, time, random
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

THE_URL = 'https://freebitco.in'
TIME_TO_LOGIN = 20
NUMBER_OF_MARTINGALE = 30

driver = None
I_lost_everything = False

def login():
	global driver

	dir = os.path.dirname(__file__)
	chrome_driver_path = dir + "\chromedriver.exe"
	driver = webdriver.Chrome(executable_path=r"chromedriver.exe")
	driver.maximize_window()

	driver.get(THE_URL)
	driver.find_element(By.CSS_SELECTOR, "li.login_menu_button").click()

	input("Press Enter after you login...")


def go_to_pacanele():
	global driver

	driver.find_element(By.CSS_SELECTOR, "a.double_your_btc_link").click()
	time.sleep(1)
	print("Am ajuns pe pagina de pacanele")

def try_your_luck():
	global driver, I_lost_everything

	double_bet = driver.find_element_by_id("double_your_btc_2x")
	minim_bet  = driver.find_element_by_id("double_your_btc_min")
	bet_high   = driver.find_element_by_id("double_your_btc_bet_hi_button")
	bet_low    = driver.find_element_by_id("double_your_btc_bet_lo_button")
	msg_win    = driver.find_element_by_id("double_your_btc_bet_win")
	msg_lose   = driver.find_element_by_id("double_your_btc_bet_lose")  # ma rog, folosesc doar mesajul de win dar asta e
	balance    = driver.find_element_by_id("balance")

	minim_bet.click()
	print("Am apasat minimum_bet")
	time.sleep(1)

	i_am_a_loser = True
	am_i_a_big_loser = False
	while i_am_a_loser is True:
		# bet high or low
		if random.randint(1, 1000) % 2 == 0:
			bet_high.click()
			print("am apasat high_bet")
		else:
			bet_low.click()
			print("am apasat low_bet")
		# wait because i want to
		time.sleep(3)
		# Did we lose everything?
		value_of_balance = driver.find_element_by_id("balance").text
		print("I have this balance: " + value_of_balance)
		time.sleep(2)

		if float(str(value_of_balance)) < 0.00000005:
			am_i_a_big_loser = True
			break
		# If not, it was a win or a fail?
		# text of win message
		text_of_win = driver.find_element_by_id("double_your_btc_bet_win").text.strip()
		print("Text of win: " + text_of_win)
		time.sleep(2)

		if len(text_of_win) > 10:
			i_am_a_loser = False
		else:
			double_bet.click()
			print("am apasat double_bet")
			time.sleep(0.3)

	# that's it, game over :C
	if am_i_a_big_loser:
		I_lost_everything = True

def play_the_pacanele():
	for _ in range(NUMBER_OF_MARTINGALE):
		try_your_luck()
		if I_lost_everything:
			break
		else:
			print("Yay, ai facut o runda, time for the next:\n\n")



#-------------------------------------------------------------------------------------
login()
go_to_pacanele()

while True:
	input("\nStart some pacanele? press Enter...")
	play_the_pacanele()

if I_lost_everything:
	print("You've fucked this hard, you DONT HAVE ANY bulsshit crypto that you gambled, but thank you for using our services!!")
else:
	print("Holy shit, you didn't screw this up, here, take the free money LOL")
	print("Total earnings should be " + str(NUMBER_OF_MARTINGALE) + " times the minimal amount")

print("\nHere, take a minute (Literally) to look at what you have done, won or lost? HEHE XD")

time.sleep(60)