"""
This file contains the functions necessary for
collecting participant data.
To run the 'null-cue gaze bias' experiment, see main.py.

made by Anna van Harmelen, 2023
"""

import random
import pandas as pd


def get_participant_details(existing_participants: pd.DataFrame, testing):
    # Generate random & unique participant number
    participant = random.randint(10, 99)
    while participant in existing_participants.participant_number.tolist():
        participant = random.randint(10, 99)

    print(f"Participant number: {participant}")

    if not testing:
        # Get participant age
        age = int(input("Participant age: "))
    else:
        age = 00

    # Insert session number
    session = max(existing_participants.session_number) + 1

    # Determine block order
    total_orders = 6 * ["CLCL"] + 6 * ["CLLC"] + 6 * ["LCLC"] + 6 * ["LCCL"]

    for item in existing_participants.block_order.tolist():
        if item in total_orders:
            total_orders.remove(item)

    random.shuffle(total_orders)
    current_block_order = total_orders[0]

    # Add newly made participant
    new_participant = pd.DataFrame(
        {
            "age": [age],
            "participant_number": [participant],
            "session_number": [session],
            "block_order": [current_block_order],
        }
    )
    all_participants = pd.concat(
        [existing_participants, new_participant], ignore_index=True
    )

    return all_participants, current_block_order
