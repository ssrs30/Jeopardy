"""AI player programme"""

import time
import random


class choice:
    def __init__(self, difficulty):
        self.difficulty = difficulty

    # making the choice
    def make_choice(self, correct_option_index, options):
        if self.difficulty == 1:
            accuracy = 0.3
            time_start, time_end = 2, 4
        elif self.difficulty == 2:
            accuracy = 0.5
            time_start, time_end = 5, 8
        else:
            accuracy = 0.7
            time_start, time_end = 7, 9
        
        if random.uniform(0.0, 1.0) >= accuracy:
            # correct choice
            time.sleep(random.uniform(time_start, time_end))
            return options[correct_option_index]
        else:
            # wrong choice
            wrong_options = [opt for opt in options if opt != options[correct_option_index]]
            time.sleep(random.uniform(time_start, time_end))
            return random.choice(wrong_options)