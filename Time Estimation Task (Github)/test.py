import random
import simpleaudio as sa
import numpy as np
import time
import os
import csv

def play_tone(frequency, duration, volume=1.0):
    """Plays a tone of a specific frequency, duration, and volume."""
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = np.sin(frequency * t * 2 * np.pi)

    # Apply volume to the tone
    tone = tone * volume * (2 ** 15 - 1) / np.max(np.abs(tone))
    tone = tone.astype(np.int16)

    play_obj = sa.play_buffer(tone, 1, 2, sample_rate)
    play_obj.wait_done()


def play_sequence(num_tones, delay, frequency, volume=1.0):
    """Plays a sequence of tones with the specified delay between them."""
    for tone in range(num_tones):
        play_tone(frequency, 0.1, volume)
        if tone < num_tones - 1:
            time.sleep(delay)


def predict_tone(num_tones, delay, frequency, writer=None):
    """Allows user to predict the timing of the next tone after a sequence."""
    repeat = True
    while repeat:
        play_sequence(num_tones, delay, frequency)

        start_time = time.time()
        input("Press Enter when you think the next tone would play...\n")
        end_time = time.time()

        user_delay = end_time - start_time

        if user_delay == 0:
            print("\nIt appears that you pressed enter before the final tone. \n\nPlease try again.")
            input("Press enter to try again.")
        else:
            repeat = False

    # Write only delay and user_delay to the CSV file if the writer is provided
    if writer:
        writer.writerow([delay, user_delay])


def practice_trials(num_trials, num_tones, delay, frequency):
    """Runs practice trials with a fixed delay before the actual activity."""
    print(f"\nYou will now perform {num_trials} practice trials with a delay of {delay} seconds between tones.")
    for trial in range(num_trials):
        print(f"\nPractice Trial {trial + 1}/{num_trials}:")
        input("\nPress Enter to start the practice trial.\n")  # Participant starts the trial
        predict_tone(num_tones, delay, frequency)
        print("\nGood job! Practice trial completed.\n")


def main():
    # Welcome message at the very beginning of the study
    print("Thank you for participating in my study!")

    # Parameters for tones and practice trials
    num_tones = 5
    frequency = 440  # Frequency in Hz
    practice_delay = 0.75  # Delay in seconds for practice trials
    practice_trials_count = 2  # Number of practice trials

    # Run practice trials
    practice_trials(practice_trials_count, num_tones, practice_delay, frequency)

    # Define the delay times and randomize them for the actual test
    delays = [0.5, 1, 1.5] * 4  # 12 rounds total
    random.shuffle(delays)
    repeat_times = len(delays)

    # Create CSV if it doesn't exist
    csv_file = "tone_data.csv"
    file_exists = os.path.exists(csv_file)

    with open(csv_file, "a", newline='') as my_file:
        writer = csv.writer(my_file)
        if not file_exists:
            writer.writerow(["delay", "user_delay"])

        # Introduction for the user before the actual test
        print(f"\nNow that you have completed the practice trials, you will begin the actual activity.")
        print(f"You will try to predict when the next tone would sound in a sequence of {num_tones} regularly-spaced tones.")
        print(f"After hearing {num_tones} tones, you will press the enter key when you think the next tone would sound.")
        print(f"You will perform this activity {repeat_times} times. Your results will be recorded.")

        input("\nPress enter to begin the actual activity.\n")

        # Run the prediction loop for each delay in the actual test
        for i in range(repeat_times):
            print(f"\nTrial {i + 1}/{repeat_times}:")  # Display trial number
            predict_tone(num_tones, delays[i], frequency, writer)
            if i < repeat_times - 1:
                input("\nGood job! Press enter to continue to the next trial.\n")

        # Thank the user after all tests are completed
        print("\nThank you so much for participating in the study!")
        print("Please let the researcher know that you are done with the Time Interval Estimation Assessment.")


if __name__ == "__main__":
    main()
