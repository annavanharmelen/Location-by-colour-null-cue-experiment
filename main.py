"""
Main script for running the 'location-by-colour null-cue' experiment
made by Anna van Harmelen, 2024

see README.md for instructions if needed
"""

# Import necessary stuff
from psychopy import core
import pandas as pd
from participantinfo import get_participant_details
from set_up import get_monitor_and_dir, get_settings
from eyetracker import Eyelinker
from trial import single_trial, generate_stimuli_characteristics
from time import time
from practice import practice
import datetime as dt
from block import (
    create_blocks,
    show_session_type,
    create_trial_list,
    show_block_type,
    block_break,
    long_break,
    finish,
    quick_finish,
)

N_BLOCKS = 16
TRIALS_PER_BLOCK = 48


def main():
    """
    Data formats / storage:
     - eyetracking data saved in one .edf file per session
     - all trial data saved in one .csv per session
     - subject data in one .csv (for all sessions combined)
    """

    # Set whether this is a test run or not
    testing = False

    # Get monitor and directory information
    monitor, directory = get_monitor_and_dir(testing)

    # Get participant details and save in same file as before
    old_participants = pd.read_csv(
        rf"{directory}\participantinfo.csv",
        dtype={
            "participant_number": int,
            "session_number": int,
            "age": int,
            "block_order": str,
            "trials_completed": str,
        },
    )
    new_participants, block_order = get_participant_details(old_participants, testing)

    # Initialise set-up
    settings = get_settings(monitor, directory)

    # Connect to eyetracker and calibrate it
    if not testing:
        eyelinker = Eyelinker(
            new_participants.participant_number.iloc[-1],
            new_participants.session_number.iloc[-1],
            settings["window"],
            settings["directory"],
        )
        eyelinker.calibrate()

    # Start recording eyetracker
    if not testing:
        eyelinker.start()

    # Practice until participant wants to stop
    practice("start", settings)

    # Initialise some stuff
    start_of_experiment = time()
    data = []
    current_trial = 0
    finished_early = True

    # Start experiment
    try:
        # Generate pseudo-random order of blocks
        blocks = create_blocks(N_BLOCKS, block_order)

        for block_nr, block_type in blocks:
            # Show session info if beginning of session
            if block_nr % 4 == 1:

                # Show participant session type
                calibrated = True
                while calibrated:
                    calibrated = show_session_type(
                        block_type,
                        settings,
                        eyetracker=None if testing else eyelinker,
                    )

                # Run practice trials
                practice(block_type, settings)

            # Pseudo-randomly create conditions and target locations (so they're weighted)
            trials_in_block = create_trial_list(8 if testing else TRIALS_PER_BLOCK)

            # Remind participant of block type
            calibrated = True
            while calibrated:
                calibrated = show_block_type(
                    block_type,
                    settings,
                    eyetracker=None if testing else eyelinker,
                )

            # Run trials per pseudo-randomly created info
            for target_bar, congruency, cue_form in trials_in_block:
                current_trial += 1
                start_time = time()

                stimuli_characteristics: dict = generate_stimuli_characteristics(
                    target_bar, congruency, cue_form
                )

                # Generate trial
                report: dict = single_trial(
                    **stimuli_characteristics,
                    probe_form=block_type,
                    settings=settings,
                    testing=testing,
                    eyetracker=None if testing else eyelinker,
                )
                end_time = time()

                # Save trial data
                data.append(
                    {
                        "trial_number": current_trial,
                        "block_type": block_type,
                        "block": block_nr,
                        "start_time": str(
                            dt.timedelta(seconds=(start_time - start_of_experiment))
                        ),
                        "end_time": str(
                            dt.timedelta(seconds=(end_time - start_of_experiment))
                        ),
                        **stimuli_characteristics,
                        **report,
                    }
                )

            # Break after end of block, unless it's the last block.
            # Experimenter can re-calibrate the eyetracker by pressing 'c' here.
            calibrated = True
            if block_nr == N_BLOCKS // 2:
                while calibrated:
                    calibrated = long_break(
                        N_BLOCKS, settings, eyetracker=None if testing else eyelinker
                    )
                if not testing:
                    eyelinker.start()
            elif block_nr < N_BLOCKS:
                while calibrated:
                    calibrated = block_break(
                        block_nr,
                        N_BLOCKS,
                        settings,
                        eyetracker=None if testing else eyelinker,
                    )

        finished_early = False

    finally:
        # Stop eyetracker (this should also save the data)
        if not testing:
            eyelinker.stop()

        # Save all collected trial data to a new .csv
        pd.DataFrame(data).to_csv(
            rf"{settings['directory']}\data_session_{new_participants.session_number.iloc[-1]}{'_test' if testing else ''}.csv",
            index=False,
        )

        # Register how many trials this participant has completed
        new_participants.loc[new_participants.index[-1], "trials_completed"] = str(
            len(data)
        )

        # Save participant data to existing .csv file
        new_participants.to_csv(
            rf"{settings['directory']}\participantinfo.csv", index=False
        )

        # Done!
        if finished_early:
            quick_finish(settings)
        else:
            finish(N_BLOCKS, settings)

        core.quit()

    # Thanks for meedoen


if __name__ == "__main__":
    main()
