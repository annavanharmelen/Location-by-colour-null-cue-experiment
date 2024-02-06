"""
This file contains the functions necessary for
creating the fixation cross and the bar stimuli.
To run the 'null-cue gaze bias' experiment, see main.py.

made by Anna van Harmelen, 2023
"""

from psychopy import visual

ECCENTRICITY = 6
DOT_SIZE = 0.1  # diameter of circle
BAR_SIZE = [0.6, 4]  # width, height
CAPTURE_CUE_SIZE = 0.7  # diameter of circle


def create_fixation_dot(settings, colour="#eaeaea"):
    # Determine size of fixation dot
    fixation_size = settings["deg2pix"](DOT_SIZE)

    # Make fixation dot
    fixation_dot = visual.Circle(
        win=settings["window"],
        units="pix",
        radius=fixation_size,
        pos=(0, 0),
        fillColor=colour,
    )

    fixation_dot.draw()


def make_one_bar(orientation, colour, position, settings):
    # Check input
    if position == "left":
        pos = (-settings["deg2pix"](ECCENTRICITY), 0)
    elif position == "right":
        pos = (settings["deg2pix"](ECCENTRICITY), 0)
    elif position == "middle":
        pos = (0, 0)
    else:
        raise Exception(f"Expected 'left' or 'right', but received {position!r}. :(")

    # Create bar stimulus
    bar_stimulus = visual.Rect(
        win=settings["window"],
        units="pix",
        width=settings["deg2pix"](BAR_SIZE[0]),
        height=settings["deg2pix"](BAR_SIZE[1]),
        pos=pos,
        ori=orientation,
        fillColor=colour,
    )

    return bar_stimulus


def create_stimuli_frame(left_orientation, right_orientation, colours, settings):
    create_fixation_dot(settings)
    make_one_bar(left_orientation, colours[0], "left", settings).draw()
    make_one_bar(right_orientation, colours[1], "right", settings).draw()


def create_colour_cue(colour, settings):
    colour_cue = visual.Circle(
        win=settings["window"],
        units="pix",
        radius=settings["deg2pix"](CAPTURE_CUE_SIZE / 2),
        pos=(0, 0),
        fillColor=colour,
    )

    colour_cue.draw()


def create_location_cue(position, settings, colour="#eaeaea"):
    # Check input
    if position == "left":
        pos = (-settings["deg2pix"](ECCENTRICITY), 0)
    elif position == "right":
        pos = (settings["deg2pix"](ECCENTRICITY), 0)
    else:
        raise Exception(f"Expected 'left' or 'right', but received {position!r}. :(")

    location_cue = visual.Circle(
        win=settings["window"],
        units="pix",
        radius=settings["deg2pix"]((BAR_SIZE[1]) / 2),
        pos=pos,
        fillColor=colour,
    )

    location_cue.draw()


def create_capture_cue_frame(cue_form, settings, colour=None, position=None):
    if cue_form == "colour_cue":
        create_colour_cue(colour, settings)
    elif cue_form == "location_cue":
        create_location_cue(position, settings)
    else:
        raise Exception(
            f"Expected 'colour_cue' or 'location_cue', but received {cue_form!r}. :("
        )

    create_fixation_dot(settings)


def create_probe_cue_frame(probe_form, settings, colour=None, position=None):
    if probe_form == "colour_probe":
        create_fixation_dot(settings, colour)
    elif probe_form == "location_probe":
        create_location_cue(position, settings)
        create_fixation_dot(settings)
    else:
        raise Exception(
            f"Expected 'colour_probe' or 'location_probe', but received {probe_form!r}. :("
        )
