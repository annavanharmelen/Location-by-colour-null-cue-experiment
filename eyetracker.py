"""
This file contains the functions necessary for
connecting and using the eyetracker.
To run the 'null-cue gaze bias' experiment, see main.py.

made by Anna van Harmelen, 2023, using code by Rose Nasrawi
"""

from lib import eyelinker
from psychopy import event
import os


class Eyelinker:
    """
    usage:

       from eyetracker import Eyelinker

    To initialise:

       eyelinker = Eyelinker(participant, session, window, directory)
       eyelinker.calibrate()
    """

    def __init__(self, participant, session, window, directory) -> None:
        """
        This also connects to the tracker
        """
        self.directory = directory
        self.window = window
        self.tracker = eyelinker.EyeLinker(
            window=window, eye="RIGHT", filename=f"{session}_{participant}.edf"
        )
        self.tracker.init_tracker()

    def start(self):
        self.tracker.start_recording()

    def calibrate(self):
        self.tracker.calibrate()

    def stop(self):
        os.chdir(self.directory)

        self.tracker.stop_recording()
        self.tracker.transfer_edf()
        self.tracker.close_edf()


def get_trigger(frame, probe_form, capture_form, congruency, target_position):
    condition_marker = {"location_probe": 1, "colour_probe": 9}[probe_form]

    if capture_form == "colour_cue":
        condition_marker += 4

    if congruency == "incongruent":
        condition_marker += 2

    if target_position == "right":
        condition_marker += 1

    return {
        "just_code_please": "",
        "stimuli_onset": "1",
        "capture_cue_onset": "2",
        "probe_cue_onset": "3",
        "response_onset": "4",
        "response_offset": "5",
        "feedback_onset": "6",
    }[frame] + str(condition_marker)
