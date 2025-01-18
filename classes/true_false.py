
from classes.multiple_choice import MultipleChoice

class TrueFalse(MultipleChoice):
    def __init__(self, id, name, capital, continent, question, answer_key):
        super().__init__(id, name, capital, continent, question, answer_key, ["True", "False"])