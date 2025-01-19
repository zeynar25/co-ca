from classes.country import Country

class Question(Country):
    def __init__(self, id, name, capital, continent, question, answer_key):
        super().__init__(id, name, capital, continent)
        self.__question = question
        self.__answer_key = answer_key
        self.__answer = None
            
    @property
    def question(self):
        return self.__question

    @question.setter
    def question(self, question):
        if isinstance(question, str):
            self.__question = question
        else:
            raise ValueError("question must be a string")
        
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
            self.__answer = answer.strip()
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
    
    
    def to_dict(self):
        return {
            "id": self.id,
            'name': self.name,
            'capital': self.capital,
            'continent': self.continent,
            'question': self.__question,
            'answer_key': self.__answer_key
        }