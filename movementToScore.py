"""
Create a movement score object and call add val whenever a new score is recieved.

"""

class MovementScore:
    def __init__(self, min_val, max_val):
        self.min_val = min_val
        self.max_val = max_val

    def add_val(self, new_val):
        if new_val > self.max_val:
            self.max_val = new_val

    def get_score(self, num):
        """
        Maps a given number in the range onto a scale of 10.
        """
        return ((num - self.min_val) / (self.max_val - self.min_val)) * 10
