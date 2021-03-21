#!/usr/bin/env python3
from pitop.display import Display
from pitop.miniscreen import Miniscreen
from time import sleep

display = Display()

display.blank()

miniscreen = Miniscreen()
miniscreen.display_multiline_text("Hello, world!", font_size=20)
sleep(1)

