"""
This file contains the functions necessary for
creating the interactive response dial at the end of a trial.
To run the 'location-by-colour null-cue' experiment, see main.py.

made by Anna van Harmelen, 2024
"""

from psychopy import core, visual, event
from psychopy.hardware.keyboard import Keyboard
from math import cos, sin, degrees
from stimuli import create_fixation_dot
from time import time
from eyetracker import get_trigger

RESPONSE_DIAL_SIZE = 2  # radius of circle
RESPONSE_DIAL_ECCENTRICITY = 6


def turn_handle(pos, origin, dial_step_size):
    x0, y0 = origin
    x, y = pos

    pos = (
        x0 + (x - x0) * cos(dial_step_size) + (y - y0) * sin(dial_step_size),
        y0 - (x - x0) * sin(dial_step_size) + (y - y0) * cos(dial_step_size),
    )

    return pos


def get_report_orientation(key, turns, dial_step_size):
    report_orientation = degrees(turns * dial_step_size)

    if key == "z":
        report_orientation *= -1

    return report_orientation


def evaluate_response(report_orientation, target_orientation, key):
    report_orientation = round(report_orientation)

    signed_difference = target_orientation - report_orientation
    abs_difference = abs(target_orientation - report_orientation)

    if abs_difference > 90:
        abs_difference -= 180
        abs_difference *= -1

    performance = round(100 - abs_difference / 90 * 100)

    correct_key = (target_orientation > 0 and key == "m") or (
        target_orientation < 0 and key == "z"
    )

    return {
        "report_orientation": report_orientation,
        "performance": performance,
        "absolute_difference": abs_difference,
        "correct_key": correct_key,
        "signed_difference": signed_difference,
    }


def make_circle(rad, settings, pos=(0, 0), handle=False, colour=None):
    circle = visual.Circle(
        win=settings["window"],
        radius=settings["deg2pix"](rad),
        edges=settings["deg2pix"](1),
        lineWidth=settings["deg2pix"](0.1),
        pos=(settings["deg2pix"](pos[0]), settings["deg2pix"](pos[1])),
    )

    if handle:
        circle.lineColor = "#eaeaea"
        circle.fillColor = settings["window"].color
    else:
        circle.lineColor = colour if colour else "#d4d4d4"
        circle.fillColor = None

    return circle


def make_dial(settings, position=[], colour=None):
    if position == "left":
        pos = (-RESPONSE_DIAL_ECCENTRICITY, 0)
    elif position == "right":
        pos = (RESPONSE_DIAL_ECCENTRICITY, 0)
    else:
        pos = (0, 0)

    dial_circle = make_circle(RESPONSE_DIAL_SIZE, settings, pos, colour=colour)
    top_dial = make_circle(
        RESPONSE_DIAL_SIZE / 15,
        settings,
        pos=(pos[0], pos[1] + RESPONSE_DIAL_SIZE),
        handle=True,
    )
    bottom_dial = make_circle(
        RESPONSE_DIAL_SIZE / 15,
        settings,
        pos=(pos[0], pos[1] - RESPONSE_DIAL_SIZE),
        handle=True,
    )

    return dial_circle, top_dial, bottom_dial


def get_response(
    probe_form,
    cue_form,
    target_orientation,
    target_colour,
    trial_condition,
    target_bar,
    settings,
    testing,
    eyetracker,
    additional_objects=[],
):
    keyboard: Keyboard = settings["keyboard"]
    window = settings["window"]

    keyboard.clearEvents()
    turns = 0

    for item in additional_objects:
        item.draw()
        window.flip()

    idle_reaction_time_start = time()

    # Wait indefinitely until the participant starts giving an answer
    keyboard.clearEvents()  # do it again to be sure
    pressed = event.waitKeys(keyList=["z", "m", "q"])

    response_started = time()
    idle_reaction_time = response_started - idle_reaction_time_start

    if "m" in pressed:
        key = "m"
        rad = settings["dial_step_size"]
    elif "z" in pressed:
        key = "z"
        rad = -settings["dial_step_size"]
    if "q" in pressed:
        raise KeyboardInterrupt()

    # Stop rotating the moment either of the following happens:
    # - the participant released the rotation key
    # - a second passed

    dial_circle, top_dial, bottom_dial = make_dial(
        settings,
        target_bar if probe_form == "location_probe" else None,
        target_colour if probe_form == "colour_probe" else None,
    )

    if not testing and eyetracker:
        trigger = get_trigger(
            "response_onset", probe_form, cue_form, trial_condition, target_bar
        )
        eyetracker.tracker.send_message(f"trig{trigger}")

    while not keyboard.getKeys(keyList=[key]) and turns < settings["monitor"]["Hz"]:
        top_dial.pos = turn_handle(top_dial.pos, dial_circle.pos, rad)
        bottom_dial.pos = turn_handle(bottom_dial.pos, dial_circle.pos, rad)

        turns += 1

        for item in additional_objects:
            item.draw()

        dial_circle.draw()
        top_dial.draw()
        bottom_dial.draw()

        if not additional_objects:
            create_fixation_dot(settings)

        window.flip()

    response_time = time() - response_started

    return {
        "idle_reaction_time_in_ms": round(idle_reaction_time * 1000, 2),
        "response_time_in_ms": round(response_time * 1000, 2),
        "key_pressed": key,
        "turns_made": turns,
        **evaluate_response(
            get_report_orientation(key, turns, settings["dial_step_size"]),
            target_orientation,
            key,
        ),
    }


def wait_for_key(key_list, keyboard):
    keyboard: Keyboard = keyboard
    keyboard.clearEvents()
    keys = event.waitKeys(keyList=key_list)

    return keys
