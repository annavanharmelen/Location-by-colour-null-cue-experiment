"""
This file contains the functions necessary for
creating and running a full block of trials start-to-finish.
To run the 'null-cue gaze bias' experiment, see main.py.

made by Anna van Harmelen, 2023
"""

import random
from trial import show_text
from response import wait_for_key


def create_blocks(n_blocks):
    if n_blocks % 2 != 0:
        raise Exception("Expected number of trials to be divisible by 2.")

    # Generate equal distribution of probe forms over the blocks, but randomly order them
    block_types = n_blocks // 2 * ["colour_probe"] + n_blocks // 2 * ["location_probe"]
    random.shuffle(block_types)

    # Save list of sets of block numbers (in order) + block types (shuffled)
    blocks = list(zip(range(1, n_blocks + 1), block_types))

    return blocks


def create_trial_list(n_trials):
    if n_trials % 8 != 0:
        raise Exception("Expected number of trials to be divisible by 8.")

    # Generate equal distribution of target locations
    locations = n_trials // 2 * ["left"] + n_trials // 2 * ["right"]

    # Generate equal distribution of congruencies,
    # that co-occur equally with the target locations
    congruencies = 2 * (n_trials // 4 * ["congruent"] + n_trials // 4 * ["incongruent"])

    # Generate equal distribution of cue forms,
    # that co-occur equally with both target locations and directions
    cue_forms = 4 * (n_trials // 8 * ["colour_cue"] + n_trials // 8 * ["location_cue"])

    # Create trial parameters for all trials
    trials = list(zip(locations, congruencies, cue_forms))
    random.shuffle(trials)

    return trials

def show_block_type(block_type, settings, eyetracker):
    show_text(
        "The next block is a "
        f"{'colour ' if block_type == 'colour_probe' else 'location '}"
        "block.",
        settings["window"],
    )
    settings["window"].flip()

    if eyetracker:
        keys = wait_for_key(["space", "c"], settings["keyboard"])
        if "c" in keys:
            eyetracker.calibrate()
            eyetracker.start()
            return True
    else:
        wait_for_key(["space"], settings["keyboard"])

    return False

def block_break(current_block, n_blocks, settings, eyetracker):
    blocks_left = n_blocks - current_block

    show_text(
        f"You just finished block {current_block}, you {'only ' if blocks_left == 1 else ''}"
        f"have {blocks_left} block{'s' if blocks_left != 1 else ''} left. "
        "Take a break if you want to, but try not to move your head during this break."
        "\nPress SPACE when you're ready to continue.",
        settings["window"],
    )
    settings["window"].flip()

    if eyetracker:
        keys = wait_for_key(["space", "c"], settings["keyboard"])
        if "c" in keys:
            eyetracker.calibrate()
            eyetracker.start()
            return True
    else:
        wait_for_key(["space"], settings["keyboard"])

    return False


def long_break(n_blocks, settings, eyetracker):
    show_text(
        f"You're halfway through! You have {n_blocks // 2} blocks left. "
        "Now is the time to take a longer break. Maybe get up, stretch, walk around."
        "\nPress SPACE whenever you're ready to continue again.",
        settings["window"],
    )
    settings["window"].flip()

    if eyetracker:
        keys = wait_for_key(["space", "c"], settings["keyboard"])
        if "c" in keys:
            eyetracker.calibrate()
            return True
    else:
        wait_for_key(["space"], settings["keyboard"])

    return False


def finish(n_blocks, settings):
    show_text(
        f"Congratulations! You successfully finished all {n_blocks} blocks!"
        "You're completely done now. Press SPACE to exit the experiment.",
        settings["window"],
    )
    settings["window"].flip()

    wait_for_key(["space"], settings["keyboard"])


def quick_finish(settings):
    show_text(
        f"You've exited the experiment. Press SPACE to close this window.",
        settings["window"],
    )
    settings["window"].flip()

    wait_for_key(["space"], settings["keyboard"])
