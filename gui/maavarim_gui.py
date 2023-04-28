import threading

import PySimpleGUI as sg


class State:
    def __init__(self):
        self.run = True

    def stop(self):
        self.run = False


class GUI:

    def start_scrappers(self, state, fns):
        threads = []
        for f in fns:
            # Start the thread for f
            t = threading.Thread(target=f, args=(state,))
            t.start()
            threads.append(t)
        return threads

    def stop_scrappers(self, running_scrappers):
        for scrapper in running_scrappers:
            scrapper.join()

    def gui(self, state, fns):
        sg.theme('DefaultNoMoreNagging')  # Set the GUI theme

        # Define the GUI layout
        status = 'Maavarim - Hate speech Detector'
        layout = [
            [sg.Text(status, key='-status-')],
            [sg.Button('Exit')]
        ]

        # Create the GUI window
        window = sg.Window('Maavarim - Hate speech Detector', layout)

        running_scrappers = self.start_scrappers(state, fns)
        # Event loop to process events and update the window
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Exit':
                answer = sg.popup_ok_cancel('Do you want to close Maavarim?', title='Close Maavarim!')
                if answer == 'OK':
                    state.stop()
                    sg.popup_auto_close("Closing !!!", auto_close_duration=1)
                    break

        # Close the window and clean up
        window.close()
        self.stop_scrappers(running_scrappers)
