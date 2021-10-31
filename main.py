from selenium import webdriver
from selenium import common
from selenium.webdriver.common.action_chains import ActionChains
import speech_recognition as sr
from functions import *
import time


# user variables
NAME = ""
PASSWORD = ""
PROFILE_DIR = ""

# global variables
LOGIN_LINK = "https://lichess.org/login?referrer=/"
NAME_DICT  = {"n": "knight", "r": "rook", "b": "bishop", "q": "queen", "k": "king",}
IT_DICT = {"uno": "1", "due": "2", "tre": "3", "quattro": "4", "cinque": "5", "sei": "6", "sette": "7", "otto": "8",
    "hp ": "cavallo", "cavallo ": "n", "alfiere ": "b", "torre ": "r", "regina ": "q", "re ": "k",
    "ci ": "c", "di ": "d", "e ": "e", "a ": "a", " ": ""}


# loads Chrome profile or creates one
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=" + PROFILE_DIR)
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# loads login page
driver = webdriver.Chrome(chrome_options=options)
driver.maximize_window()
driver.get(LOGIN_LINK)

# if the login is not cached
try:
    # insert username and password and login
    driver.find_element_by_id("form3-username").send_keys(NAME)
    driver.find_element_by_id("form3-password").send_keys(PASSWORD)
    driver.find_element_by_class_name("submit.button").click()
# if the login is cached
except common.exceptions.NoSuchElementException:
    pass

# waits for the player to be ready
input("Begin a game and press enter\n")

# find player color
white_label = driver.find_element_by_class_name("player.color-icon.is.white.text")
if NAME in white_label.find_element_by_class_name("user-link").text:
    COLOR = "white"
else:
    COLOR = "black"

# voice recognition setup
r = sr.Recognizer()
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)

    print("Ready to listen")
    # main loop
    while True:

        # input handling
        audio = r.listen(source)
        try:
            inp = r.recognize_google(audio, language="it-IT").lower()
            for key in IT_DICT.keys():
                if key in inp:
                    inp = inp.replace(key, IT_DICT[key])
        except sr.UnknownValueError:
            print("Unknown words")
            continue
        
        print("I understood: ", inp)
        
        # check if the match finished
        if len(driver.find_elements_by_class_name("status")) > 0:
            input("Match ended\n")
            break

        # exit keyword
        if inp == "exit":
            break

        # normal move
        elif validpos(inp):

            # waits if it's the opponent turn
            while True:
                if "your turn" in driver.title.lower():
                    break
                else:
                    print("Wait for your turn...")
                    time.sleep(1)

            # characteristics of the move asked
            if inp[0] in NAME_DICT:
                piece = NAME_DICT[inp[0]]
                inp = inp[1:]
            else:
                piece = "pawn"

            # get piece list
            pieces_list = driver.find_elements_by_class_name(COLOR + "." + piece)
            if len(pieces_list) == 0:
                print("Piece not found")
                continue
            
            # dummy variable to control whether it moved or not
            done = False
            # disambiguating move
            if len(inp) == 4:
                for p in pieces_list:
                    # blocks if already done
                    if done:
                        break
                    
                    if inp[0:2] == tochess(getcoords(p), COLOR, p.size["width"]):
                        
                        # click on the piece selected to see its possible moves
                        ActionChains(driver).move_to_element(p).click().perform()
                        
                        # iterates moves to find if there is the one requested
                        for m in driver.find_elements_by_class_name("move-dest"):

                            if inp[2:4] == tochess(getcoords(m), COLOR, p.size["width"]):
                                
                                # click on the destination
                                ActionChains(driver).move_to_element(m).click().perform()
                                done = True
                                break
            
            # normal move
            elif len(inp) == 2:
                for p in pieces_list:
                    # blocks if already done
                    if done:
                        break
                    
                    # click on the piece selected to see its possible moves
                    ActionChains(driver).move_to_element(p).click().perform()

                    # iterates moves to find if there is the one requested
                    for m in driver.find_elements_by_class_name("move-dest"):
                        
                        if inp == tochess(getcoords(m), COLOR, p.size["width"]):
                            
                            # click on the destination
                            ActionChains(driver).move_to_element(m).click().perform()
                            done = True
                            break
            if not done:
                print("Invalid move")
        
        else:
            print("Invalid command")
