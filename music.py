from mingus.midi import fluidsynth
from mingus.containers import Note, NoteContainer
from mingus.core import intervals, progressions
import time
import platform

class Music:
    def __init__(self):
        soundFontPath = "./FluidR3_GM.sf2"
        # Fludisynth setup
        if platform.system() == "Linux":
            fluidsynth.init(soundFontPath, "pulseaudio")
        else:
            fluidsynth.init(soundFontPath)

        # Music generation parameters
        self.progression = ["iv","v7","vi","iii7", "iv", "idom7", "iv", "v"]
        self.key = "C"
        self.chords = self.generateChords()
    
    # Music generation code adapted from https://medium.com/@andrewadiletta/producing-music-with-rules-python-tutorial-8c4005f276f0
    def play(self, fast = False):
        for i in range(len(self.chords)):
            current_chord = NoteContainer(self.chords[i])
            base_note = Note(current_chord[0].name)
            base_note.octave_down()
            fluidsynth.play_Note(base_note)
            time.sleep(0.5) 
            # Play highest note in chord
            fluidsynth.play_Note(current_chord[-1])  
            # 50% chance on a bass note
            if fast:
                second_base_note = Note(current_chord[1].name)
                second_base_note.octave_down()
                fluidsynth.play_Note(second_base_note)
            time.sleep(0.5)       
            # 50% chance on a ninth
            if fast:
                ninth_note = Note(intervals.third(current_chord[0].name, self.key))
                ninth_note.octave_up()
                fluidsynth.play_Note(ninth_note)
            time.sleep(0.5)     
            # 50% chance on a last note
            if fast:
                fluidsynth.play_Note(current_chord[-2])
            time.sleep(0.5)

    def generateChords(self):
        return progressions.to_chords(self.progression, self.key)