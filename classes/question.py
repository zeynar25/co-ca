from classes.country import Country

class Question(Country):
    def __init__(self, country, capital, continent):
        super().__init__(country, capital, continent)
        self.__options = []

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