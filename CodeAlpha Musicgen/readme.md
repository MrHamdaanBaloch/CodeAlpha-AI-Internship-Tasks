# CodeAlpha AI Internship - Task 3: Music Generation (Markov Chain with Beeps)

## Task Description
Create an AI-powered music generation system capable of composing original music using techniques like Recurrent Neural Networks (RNNs) or Generative Adversarial Networks (GANs) to generate music sequences.

## Implemented Approach (Markov Chain Simulation)
This project provides a simplified approach to music sequence generation using a **RNNs based Markov Chain**. While not a deep learning model like an RNN or GAN, a Markov Chain is a probabilistic model where the next state (note) depends only on the current state. This demonstrates a basic form of sequential, rule-based generation that is a conceptual precursor to more complex AI models.

The script generates musical "phrases" and attempts to play them as **basic beeps using the `winsound` module on Windows**. On other operating systems, it will print the note information and simulate durations with pauses.

**Note:** The "music" produced is very rudimentary (sequences of beeps with some rhythmic variation). This is intended as a simple, runnable demonstration of sequence generation with audible feedback.

## Features
-   Generates sequences of (Note, Duration) tuples.
-   Uses a Markov Chain (with a predefined transition matrix) to determine the sequence of notes within a scale.
-   Plays basic beep sounds for each note on Windows using `winsound`.
-   Simulates note durations using `time.sleep()` on other OS or if `winsound` fails.
-   Allows user to specify the number of phrases and notes per phrase.
-   Prints the generated sequence and playback information to the console.

## Technologies Used
-   Python 3.x
-   `random` module
-   `time` module
-   `platform` module
-   `winsound` module (built-in on Windows)

## Setup and Installation
1.  **Prerequisites:** Python 3.6 or higher.
2.  **Clone/Download:** Get `markov_music_generator.py`.
3.  **No external libraries need `pip install`** for basic functionality. `winsound` is standard on Windows.

## How to Run
1.  Navigate to the project directory:
    ```bash
    cd CodeAlpha_MusicGenerationMarkov
    ```
2.  Execute the Python script:
    ```bash
    python markov_music_generator.py
    ```
3.  The script will prompt for the number of phrases and notes per phrase.
4.  It will then print the note information and attempt to play beeps (on Windows).

## Limitations
-   **Not True AI:** This uses a predefined Markov Chain, not a learned model.
-   **Very Basic Sound:** `winsound.Beep` creates simple tones.
-   **Windows-Specific Sound:** Audible beeps are primarily for Windows.
-   **Limited Musicality:** The transition rules are simple and do not capture complex music theory.

## Screenshot/Output Example
