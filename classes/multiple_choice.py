from classes.question import Question

class MultipleChoice(Question):
    def __init__(self, id, name, capital, continent, desc, answer_key, options=None):
        super().__init__(id, name, capital, continent, desc, answer_key)
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

    def add_option(self, option):
        """Add an option to the question."""
        if isinstance(option, str) and option.strip():
            self.__options.append(option)
        else:
            raise ValueError("Option must be a non-empty string")

    def __str__(self):
        base_info = super().__str__()
        return f"{base_info}, Options: {', '.join(self.__options)}"

    def to_dict(self):
        return {
            "id": self.id,
            'name': self.name,
            'capital': self.capital,
            'continent': self.continent,
            'desc': self.desc,
            'answer_key': self.answer_key,
            'options': self.__options
        }