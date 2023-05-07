class Sound_Manager():

    def __init__(self, low_notes, high_notes, notes_index, note_input, lowest_achieved_note, highest_achieved_note):
        self.low_notes = low_notes
        self.high_notes = high_notes
        self.notes_index = notes_index
        self.note_input = note_input
        self.lowest_achieved_note = lowest_achieved_note
        self.highest_achieved_note = highest_achieved_note
        self.notes_index = notes_index

    def get_notes_index(self):
        return self.notes_index

    def set_notes_index(self, new_index):
        self.notes_index = new_index

    def get_next_low_note(self):
        return self.low_notes[self.notes_index]
    
    def get_next_high_note(self):
        return self.high_notes[self.notes_index]
    
    def set_note_input(self, new_note_input):
        self.note_input = new_note_input

    def get_note_input(self):
        return self.note_input
    
    def set_lowest_achieved_note(self, new_note):
        self.lowest_achieved_note = new_note

    def set_highest_achieved_note(self, new_note):
        self.highest_achieved_note = new_note

    def get_lowest_achieved_note(self):
        return self.lowest_achieved_note
    
    def get_highest_achieved_note(self):
        return self.highest_achieved_note