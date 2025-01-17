from classes.country import Country

class Question(Country):
    def __init__(self, id, name, capital, continent, desc, answer_key):
        super().__init__(id, name, capital, continent)
        self.__desc = desc
        self.__answer_key = answer_key
        self.__answer = None
            
    @property
    def desc(self):
        return self.__desc

    @desc.setter
    def desc(self, desc):
        if isinstance(desc, str):
            self.__desc = desc
        else:
            raise ValueError("description must be a string")
        
    @property
    def answer_key(self):
        return self.__answer_key

    @answer_key.setter
    def correct_answer(self, answer):
        if isinstance(answer, str):
            self.__answer_key = answer
        else:
            raise ValueError("answer must be a string")

    @property
    def answer(self):
        return self.__answer

    @answer.setter
    def answer(self, answer):
        if isinstance(answer, str):
            self.__answer = answer
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
        return f"{base_info}, Question: {self.__desc}, Answer Key: {self.__answer_key}"