
import random
import time
import platform

_WINSOUND_AVAILABLE = False
if platform.system() == "Windows":
    try:
        import winsound
        _WINSOUND_AVAILABLE = True
        print("Windows OS: `winsound` available for beeps.")
    except ImportError:
        print("Windows OS: `winsound` module not found. Will only print notes.")
else:
    print(f"{platform.system()} OS: `winsound` not available. Will only print notes.")

# --- Musical Elements ---
SCALE_NOTES = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
OCTAVES = [4] # Keep it simple with one octave for beeps, e.g., Octave 4
NOTE_FREQUENCIES = { # Frequencies for octave 4 (approximate Hz)
    'C4': 262, 'D4': 294, 'E4': 330, 'F4': 349, 'G4': 392, 'A4': 440, 'B4': 494,
    'Rest': 0 # For silence
}
DURATIONS_MS = { # Rhythmic values in milliseconds
    "QUARTER": 500, 
    "HALF": 1000,
    "DOTTED_QUARTER": 750,
    "EIGHTH": 250
}
BEATS_PER_MEASURE = 4 # For structuring phrases

# --- Markov Chain Transition Matrix (Simplified) ---
# Defines probability of moving from one note in SCALE_NOTES to another.
# Rows are 'from_note_idx', Columns are 'to_note_idx'. Values are weights.
# This is a very simple example, a real one would be learned from data.
# For simplicity, let's make it more likely to move to nearby notes or repeat.
num_scale_notes = len(SCALE_NOTES)
transition_matrix = {} # {current_note_idx: [(next_note_idx, weight), ...]}

for i in range(num_scale_notes):
    transitions = []
    # Higher weight to stay or move +/-1 step
    transitions.append(((i - 1 + num_scale_notes) % num_scale_notes, 3)) # Previous note
    transitions.append((i, 5))                                         # Same note
    transitions.append(((i + 1) % num_scale_notes, 4))                 # Next note
    # Lower weight to move +/-2 steps
    transitions.append(((i - 2 + num_scale_notes) % num_scale_notes, 1)) 
    transitions.append(((i + 2) % num_scale_notes, 1))
    # Occasionally jump further
    if num_scale_notes > 4:
        transitions.append(((i + 3) % num_scale_notes, 0.5))
        transitions.append(((i - 3 + num_scale_notes) % num_scale_notes, 0.5))
    transition_matrix[i] = transitions


def get_next_note_markov(current_note_idx):
    """Selects the next note based on the Markov transition matrix."""
    if current_note_idx not in transition_matrix: # Should not happen if matrix is complete
        return random.randint(0, num_scale_notes - 1) 

    options = transition_matrix[current_note_idx]
    next_note_indices, weights = zip(*options)
    chosen_next_note_idx = random.choices(next_note_indices, weights=weights, k=1)[0]
    return chosen_next_note_idx

def generate_music_phrase_markov(num_notes=8, start_note_idx=None):
    """Generates a phrase of music using the Markov chain."""
    phrase = []
    if start_note_idx is None:
        current_note_idx = random.randint(0, num_scale_notes - 1)
    else:
        current_note_idx = start_note_idx
    
    octave_val = random.choice(OCTAVES) # Octave can be fixed or varied per phrase/note

    for _ in range(num_notes):
        note_name = SCALE_NOTES[current_note_idx]
        full_note_id = f"{note_name}{octave_val}" # e.g., C4
        
        # Simple rhythm: random duration, occasional rests
        if random.random() < 0.15: # 15% chance of a rest
            note_to_play = "Rest"
            duration_ms = random.choice(list(DURATIONS_MS.values())) // 2 # Shorter rests
        else:
            note_to_play = full_note_id
            duration_ms = random.choice(list(DURATIONS_MS.values()))
            current_note_idx = get_next_note_markov(current_note_idx) # Get next note for melody
            
        phrase.append((note_to_play, duration_ms))
        
    return phrase

def play_phrase_with_sound(phrase):
    """Plays the generated phrase with beeps (Windows) or prints (others)."""
    print("\nPlaying phrase:")
    for i, (note_id, duration_ms) in enumerate(phrase):
        freq = NOTE_FREQUENCIES.get(note_id, 0) # Get frequency, 0 for Rest or unknown
        
        print(f"  {i+1}. Note: {note_id:<4} Duration: {duration_ms}ms Freq: {freq if freq else '---'}Hz")

        if _WINSOUND_AVAILABLE and freq > 0: # winsound freq must be 37-32767
            safe_freq = max(37, min(32767, freq)) # Clamp frequency
            try:
                winsound.Beep(int(safe_freq), int(duration_ms))
            except Exception as e: # Catch potential winsound errors
                print(f"      Error playing beep: {e}")
                time.sleep(duration_ms / 1000.0) # Fallback to sleep
        else: # Rest or not on Windows or winsound unavailable
            time.sleep(duration_ms / 1000.0) # Simulate duration
    print("-" * 20)

if __name__ == "__main__":
    print("=== RNNS/GANNs Music Note Sequence Generator (with Basic Sound on Windows) ===")
    print("This script uses a simple RNNs base Markovchain to generate note sequences.")
    print("It's a conceptual step towards RNNs/GANs.\n")

    try:
        num_phrases = int(input("Enter number of musical phrases to generate (e.g., 2-4): ") or "2")
        notes_per_phrase = int(input(f"Enter notes per phrase (e.g., 4-8, default: {BEATS_PER_MEASURE*2}): ") or str(BEATS_PER_MEASURE * 2))
        if num_phrases <= 0: num_phrases = 2
        if notes_per_phrase <= 0: notes_per_phrase = BEATS_PER_MEASURE * 2
    except ValueError:
        print("Invalid input, using defaults.")
        num_phrases = 2
        notes_per_phrase = BEATS_PER_MEASURE * 2

    current_phrase_start_note_idx = random.randint(0, num_scale_notes - 1)
    for i in range(num_phrases):
        print(f"\n--- Generating Phrase {i+1} ---")
        music_phrase = generate_music_phrase_markov(num_notes=notes_per_phrase, start_note_idx=current_phrase_start_note_idx)
        play_phrase_with_sound(music_phrase)
        
        # For next phrase, start near where the last one ended (simple continuity)
        if music_phrase:
            last_note_played_id = music_phrase[-1][0]
            if last_note_played_id != "Rest":
                last_note_name = last_note_played_id[:-1] # Remove octave
                if last_note_name in SCALE_NOTES:
                    current_phrase_start_note_idx = SCALE_NOTES.index(last_note_name)


    if not _WINSOUND_AVAILABLE:
        print("\nNote: Audible beeps via 'winsound' are only available on Windows.")
        print("On other systems, note durations were simulated by pausing.")