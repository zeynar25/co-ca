import random

from classes.question import Question

class MultipleChoice(Question):
    def __init__(self, id, name, capital, continent, question, answer_key, options=None):
        super().__init__(id, name, capital, continent, question, answer_key)
        self.__options = options if options else []

    @property
    def options(self):
        return self.__options

    @options.setter
    def options(self, options):
        if isinstance(options, list):
            self.__options = options
        else:
            raise ValueError("Options must be a list")

    def add_options(self, countries, attribute):
        options = set()
        options.add(getattr(self, attribute))

        while len(options) < 4:
            random_country = random.choice(countries)
            options.add(getattr(random_country, attribute))
        
        self.__options = list(options)
        random.shuffle(self.__options)

    def __str__(self):
        base_info = super().__str__()
        return f"{base_info}, Options: {', '.join(self.__options)}"

    def to_dict(self):
        return {
            "id": self.id,
            'name': self.name,
            'capital': self.capital,
            'continent': self.continent,
            'question': self.question,
            'answer_key': self.answer_key,
            'options': self.__options
        }