from classes.country import Country

class Question(Country):
    def __init__(self, id, name, capital, continent, options=None):
        super().__init__(id, name, capital, continent)
        self.__options = options if options else []
        self.__user_answer = None
        self.__correct_answer = None

    @property
    def options(self):
        return self.__options

    @options.setter
    def options(self, options):
        if isinstance(options, list):
            self.__options = options
        else:
            raise ValueError("Options must be a list")

    @property
    def user_answer(self):
        return self.__user_answer

    @user_answer.setter
    def user_answer(self, answer):
        if isinstance(answer, str):
            self.__user_answer = answer
        else:
            raise ValueError("answer must be a string")
            
    @property
    def correct_answer(self):
        return self.__correct_answer

    @correct_answer.setter
    def correct_answer(self, answer):
        if isinstance(answer, str):
            self.__correct_answer = answer
        else:
            raise ValueError("answer must be a string")

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
            'options': self.__options
        }