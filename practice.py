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
from block import show_block_type
import random


def practice(type, settings):
    # Check practice type
    if type == "start":
        # Decide which type of block to practice first
        blocks = ["colour_probe", "location_probe"]
        random.shuffle(blocks)

        # Practice response dial
        practice_dial(blocks[0], settings)

        # Practice separate block types (random order)
        practice_indefinitely(blocks[0], True, settings)
        practice_indefinitely(blocks[1], False, settings)

    elif type in ("colour_probe", "location_probe"):
        practice_n_trials(type, 8, settings)

    else:
        raise Exception("Don't understand practice type.")


def practice_dial(next_block, settings):
    # Show explanation
    show_text(
        f"Welcome to the practice session. You will practice all three parts until you press Q. \
            \n\nPress SPACE to start practicing the response dial.",
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
                cue_form,
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
                (0, settings["deg2pix"](0.7)),
            )
            settings["window"].flip()
            sleep(0.5)

    except KeyboardInterrupt:
        show_text(
            "You decided to stop practising the response dial. "
            "Press SPACE to start practicing the second part: "
            f"{'colour ' if next_block == 'colour_probe' else 'location '} trials."
            "\n\nRemember to press Q to stop practising these trials and move on to the final practice part.",
            settings["window"],
        )
        settings["window"].flip()
        wait_for_key(["space"], settings["keyboard"])


def practice_indefinitely(block_type, first_block, settings):
    # Practice first probe-type trials until user chooses to stop
    try:
        # Show block type
        show_block_type(block_type, settings, None)

        while True:
            target_bar = random.choice(["left", "right"])
            congruency = random.choice(["congruent", "incongruent"])
            cue_form = random.choice(["colour_cue", "location_cue"])

            stimulus = generate_stimuli_characteristics(
                target_bar, congruency, cue_form
            )

            report: dict = single_trial(
                **stimulus, probe_form=block_type, settings=settings, testing=True
            )

    except KeyboardInterrupt:
        if first_block:
            show_text(
                "You decided to stop practising the "
                f"{'colour ' if block_type == 'colour_probe' else 'location '} trials. "
                "Press SPACE to start practicing the final part: "
                f"{'location ' if block_type == 'colour_probe' else 'colour '} trials."
                "\n\nRemember to press Q to stop practising these trials once you feel comfortable starting the real experiment.",
                settings["window"],
            )
            settings["window"].flip()
            wait_for_key(["space"], settings["keyboard"])

        else:
            show_text(
                "You decided to stop practicing the trials."
                f"\n\nPress SPACE to start the experiment.",
                settings["window"],
            )
            settings["window"].flip()
            wait_for_key(["space"], settings["keyboard"])


def practice_n_trials(block_type, n_trials, settings):
    # Show practice info
    show_text(
        f"You will practice {n_trials} "
        f"{'colour ' if block_type == 'colour_probe' else 'location '}"
        "trials.\n\nPress SPACE to start.",
        settings["window"],
    )
    settings["window"].flip()
    wait_for_key(["space"], settings["keyboard"])

    # Run set number of practice trials
    for _ in range(n_trials):
        target_bar = random.choice(["left", "right"])
        congruency = random.choice(["congruent", "incongruent"])
        cue_form = random.choice(["colour_cue", "location_cue"])

        stimulus = generate_stimuli_characteristics(target_bar, congruency, cue_form)

        report: dict = single_trial(
            **stimulus, probe_form=block_type, settings=settings, testing=True
        )

    show_text(
        "You finished the practice trials.\n\nPress SPACE to start the session.",
        settings["window"],
    )
    settings["window"].flip()
    wait_for_key(["space"], settings["keyboard"])
