import music21
import time
import winsound
import _thread


class Player:
    def __init__(self, midi_name, bpm):
        song = music21.converter.parse(midi_name)
        # song.show()
        self.bpm = bpm
        self.mpqn = int(float(6e4) / bpm)
        self.s = music21.instrument.partitionByInstrument(song)

    def play(self):
        total_note_num = 0
        if self.s is not None:
            for i in self.s.recurse().parts:
                if i.partName == "Piano":
                    notes = i.notesAndRests.stream()
                    total_note_num = len(notes)
                    played_note_num = 0
                    for note in notes:
                        # print(note)
                        played_note_num += 1
                        note_time = note.duration.quarterLength * self.mpqn
                        if note.isRest:
                            print("Sleep %d" % note_time)
                            time.sleep(int(note_time / 1000))
                        elif note.isNote:
                            frequency = note.pitch.frequency
                            print(note.octave, note.name, note_time)
                            winsound.Beep(int(frequency), int(note_time))
                        print("Note %d/%d" % (played_note_num, total_note_num))


player = Player("lemon.mid", 90)
_thread.start_new_thread(player.play())
