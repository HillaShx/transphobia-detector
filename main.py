import time
from dotenv import load_dotenv
from gui.maavarim_gui import GUI, State

load_dotenv()


def fb_scapper(state):
    while state.run:
        time.sleep(5)
        print("hello")


def tweeter_scrapper(state):
    while state.run:
        time.sleep(3)
        print("tweet")


gui = GUI()
state = State()

if __name__ == "__main__":
    scrappers = [fb_scapper, tweeter_scrapper]
    state = State()
    gui.gui(state, scrappers)
