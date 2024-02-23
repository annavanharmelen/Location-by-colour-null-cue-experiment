"""
This file contains the functions necessary for
creating the fixation cross and the bar stimuli.
To run the 'null-cue gaze bias' experiment, see main.py.

made by Anna van Harmelen, 2023
"""

from psychopy import visual

ECCENTRICITY = 6
DOT_SIZE = 0.1  # radius of inner circle
TOTAL_DOT_SIZE = 0.35  # radius of outer circle
BAR_SIZE = [0.7, 4]  # width, height
PROBE_CUE_SIZE = 2  # radius of circle


def create_fixation_dot(settings, colour="#eaeaea"):

    # Make fixation dot
    decentral_dot = visual.Circle(
        win=settings["window"],
        units="pix",
        radius=settings["deg2pix"](TOTAL_DOT_SIZE),
        pos=(0, 0),
        fillColor=colour,
    )

    fixation_dot = visual.Circle(
        win=settings["window"],
        units="pix",
        radius=settings["deg2pix"](DOT_SIZE),
        pos=(0, 0),
        fillColor="#000000",
    )

    decentral_dot.draw()
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


def create_location_cue(position, settings):
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
        radius=settings["deg2pix"](TOTAL_DOT_SIZE),
        pos=pos,
        fillColor="#eaeaea",
    )

    location_cue.draw()


def create_capture_cue_frame(cue_form, settings, colour=None, position=None):
    if cue_form == "colour_cue":
        create_fixation_dot(settings, colour)
    elif cue_form == "location_cue":
        create_location_cue(position, settings)
        create_fixation_dot(settings)
    else:
        raise Exception(
            f"Expected 'colour_cue' or 'location_cue', but received {cue_form!r}. :("
        )


def create_probe_cue(probe_form, settings, colour, position=None):
    # Check input
    if probe_form == "location_probe":
        if position == "left":
            pos = (-settings["deg2pix"](ECCENTRICITY), 0)
        elif position == "right":
            pos = (settings["deg2pix"](ECCENTRICITY), 0)
        else:
            raise Exception(
                f"Expected 'left' or 'right', but received {position!r}. :("
            )
    elif probe_form == "colour_probe":
        pos = (0, 0)
    else:
        raise Exception(
            f"Expected 'location_probe' or 'colour_probe', but received {probe_form!r}."
        )

    probe = visual.Circle(
        win=settings["window"],
        radius=settings["deg2pix"](PROBE_CUE_SIZE),
        edges=settings["deg2pix"](1),
        pos=(pos[0], pos[1]),
        lineWidth=settings["deg2pix"](0.1),
        fillColor=None,
        lineColor=colour,
    )

    probe.draw()


def create_probe_cue_frame(probe_form, settings, colour, position=None):
    create_probe_cue(probe_form, settings, colour, position)
    create_fixation_dot(settings)
