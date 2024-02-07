"""
This file contains the functions necessary for
practising the trials and the use of the report dial.
To run the 'null-cue gaze bias' experiment, see main.py.

made by Anna van Harmelen, 2023
"""

from trial import (
    single_trial,
    generate_stimuli_characteristics,
    show_text,
)
from stimuli import make_one_bar, create_fixation_dot
from response import get_response, wait_for_key
from psychopy import event
from psychopy.hardware.keyboard import Keyboard
from time import sleep
import random


def practice(settings):
    # Show explanation
    show_text(
        f"Welcome to the practice trials. You will practice each part until you press Q. \
            \nPress SPACE to start the practice session.",
        settings["window"],
    )
    settings["window"].flip()
    wait_for_key(["space"], settings["keyboard"])

    # Practice dial until user chooses to stop
    try:
        while True:
            target_bar = random.choice(["left", "right"])
            congruency = "congruent"
            cue_form = ""
            target = generate_stimuli_characteristics(target_bar, congruency, cue_form)

            practice_bar = make_one_bar(
                target["target_orientation"], "#eaeaea", "middle", settings
            )

            report: dict = get_response(
                "colour_probe",
                target["target_orientation"],
                None,
                1,
                target_bar,
                settings,
                True,
                None,
                [practice_bar],
            )

            create_fixation_dot(settings)
            show_text(
                f"{report['performance']}",
                settings["window"],
                (0, settings["deg2pix"](0.5)),
            )
            settings["window"].flip()
            sleep(0.5)

    except KeyboardInterrupt:
        show_text(
            "You decided to stop practising the response dial. "
            "Press SPACE to start practicing full trials."
            "\nRemember to press Q to stop practising these trials and move on to the final practice part.",
            settings["window"],
        )
        settings["window"].flip()
        wait_for_key(["space"], settings["keyboard"])

    # Decide which type of block to practice first
    blocks = ["colour_probe", "location_probe"]
    random.shuffle(blocks)

    # Practice first probe-type trials until user chooses to stop
    try:
        while True:
            target_bar = random.choice(["left", "right"])
            congruency = random.choice(["congruent", "incongruent"])
            cue_form = random.choice(["colour_cue", "location_cue"])

            stimulus = generate_stimuli_characteristics(
                target_bar, congruency, cue_form
            )

            report: dict = single_trial(
                **stimulus, probe_form=blocks[0], settings=settings, testing=True
            )

    except KeyboardInterrupt:
        show_text(
            "You decided to stop practising the response dial. "
            "Press SPACE to start practicing full trials."
            "\nRemember to press Q to stop practising these trials once you feel comfortable starting the real experiment.",
            settings["window"],
        )
        settings["window"].flip()
        wait_for_key(["space"], settings["keyboard"])

    wait_for_key(["space"], settings["keyboard"])

    # Practice second probe-type trials until user chooses to stop
    try:
        while True:
            target_bar = random.choice(["left", "right"])
            congruency = random.choice(["congruent", "incongruent"])
            cue_form = random.choice(["colour_cue", "location_cue"])

            stimulus = generate_stimuli_characteristics(
                target_bar, congruency, cue_form
            )

            report: dict = single_trial(
                **stimulus, probe_form=blocks[1], settings=settings, testing=True
            )

    except KeyboardInterrupt:
        show_text(
            f"You decided to stop practicing the trials.\nPress SPACE to start the experiment.",
            settings["window"],
        )
        settings["window"].flip()

    wait_for_key(["space"], settings["keyboard"])
