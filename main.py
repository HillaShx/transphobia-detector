import time
from dotenv import load_dotenv
from gui.maavarim_gui import GUI, State
from routers.scraping import scrape_facebook, scrap_every_interval

load_dotenv()


def tweeter_scrapper():
    pass


gui = GUI()
state = State()


def main():
    timed_fb = scrap_every_interval(60, scrape_facebook)
    timed_tweeter = scrap_every_interval(10, tweeter_scrapper)
    scrappers = [timed_fb, timed_tweeter]
    state = State()
    gui.gui(state, scrappers)


if __name__ == "__main__":
    main()
