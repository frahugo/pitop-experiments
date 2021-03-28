import multiprocessing
import os
import pathlib

from pitop.pma import Button, LED
from pitop.miniscreen import Miniscreen

class HudServer(multiprocessing.Process):
    def __init__(self, queue):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        self.assets_path = pathlib.Path(__file__).parent.absolute().as_posix()

    def run(self):
        self.button = Button("D0")
        self.led = LED("D1")
        self.miniscreen = Miniscreen()

        self.button.when_pressed = self.stop_blink

        while True:
            message = self.queue.get()
            if message is None:
                print('HUD Exiting')
                self.queue.task_done()
                break
            else:
                print('HUD Got message ', message)
                func = getattr(self, message)
                func()
                self.queue.task_done()

        return

    def welcome(self):
        print("HUD welcome")
        self.miniscreen.display_image_file(self.assets_path + "/welcome.gif")

    def start_blink(self):
        print("HUD blink")
        self.led.blink()
        self.miniscreen.display_multiline_text(
            "Blinking... Press button to stop", font_size=12)
        os.system("aplay " + self.assets_path + "/bell.wav")

    def stop_blink(self):
        print("HUD stop")
        self.led.off()
        os.system("espeak \"Excellent. I just turned off the led.\"")
        self.welcome()

    def goodbye(self):
        print("HUD goodbye")
        os.system("espeak \"Goodbye!\"")
