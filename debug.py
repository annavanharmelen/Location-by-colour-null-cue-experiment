"""
This script is used to test random aspects
of the 'null-cue gaze bias' experiment.

made by Anna van Harmelen, 2023
"""

from psychopy import visual
from math import atan2, degrees
import time
from set_up import get_monitor_and_dir, get_settings
from trial import generate_stimuli_characteristics, single_trial
from block import create_blocks
from response import get_response

monitor, directory = get_monitor_and_dir(True)
settings = get_settings(monitor, directory)

try:
    get_response("colour", 45, "#ff0000", "congruent", "left", settings, True, None)
except Exception as e:
    print(e)

# stop here
import sys

sys.exit()

blocks = create_blocks(6)
print(blocks)

window = settings["window"]
deg2pix = settings["deg2pix"]

stimuli_characteristics: dict = generate_stimuli_characteristics(
    "right", "incongruent", "location"
)

# Generate trial
report: dict = single_trial(
    **stimuli_characteristics,
    settings=settings,
    testing=True,
    eyetracker=None,
)

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
