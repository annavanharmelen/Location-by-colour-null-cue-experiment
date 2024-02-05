"""
This script is used to test random aspects
of the 'null-cue gaze bias' experiment.

made by Anna van Harmelen, 2023
"""

from psychopy import visual
from math import atan2, degrees
import time
from set_up import get_monitor_and_dir, get_settings

monitor, directory = get_monitor_and_dir(True)
settings = get_settings(monitor, directory)
window = settings["window"]
deg2pix = settings["deg2pix"]

capture_cue = visual.Rect(
    win=window,
    units='pix',
    width=deg2pix(2),
    height=deg2pix(2),
    pos=(0,0),
    lineColor = 'red',
    lineWidth = deg2pix(0.1),
    fillColor = None,
)

capture_cue.draw()
window.flip()
time.sleep(2)

# stop here
import sys
sys.exit()

monitor = {
        "resolution": (1920, 1080),  # in pixels
        "Hz": 239,  # screen refresh rate in Hz
        "width": 53,  # in cm
        "distance": 70,  # in cm
    }

degrees_per_pixel = degrees(atan2(0.5 * monitor["width"], monitor["distance"])) / (
    0.5 * monitor["resolution"][0]
)

print(degrees_per_pixel)
