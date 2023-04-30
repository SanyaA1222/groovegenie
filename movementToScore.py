"""
Create a movement score object and call add val whenever a new score is recieved.

"""


class MovementScore:
    def __init__(self):
        self.min_val = 0
        self.max_val = 2

    def add_val(self, new_val):
        if new_val > self.max_val:
            self.max_val = new_val

    def get_score(self, num):
        """
        Maps a given number in the range onto a scale of 10.
        """
        print(((num - self.min_val) / (self.max_val - self.min_val)) * 20)
        return ((num - self.min_val) / (self.max_val - self.min_val)) * 20

