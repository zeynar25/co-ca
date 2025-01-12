class Country:
    def __init__(self, name, capital, continent):
        self.__name = name
        self.__capital = capital
        self.__continent = continent

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if isinstance(name, str) and name.strip():
            self.__name = name.capitalize()
        else:
            raise ValueError("Invalid country name")

    @property
    def capital(self):
        return self.__capital

    @capital.setter
    def capital(self, capital):
        if isinstance(capital, str) and capital.strip():
            self.__capital = capital.capitalize()
        else:
            raise ValueError("Invalid capital name")

    @property
    def continent(self):
        return self.__continent

    @continent.setter
    def continent(self, continent):
        if not isinstance(continent, str) or not continent.strip():
            raise ValueError("Continent name must be a non-empty string")
    
        continent = continent.capitalize()
        continents = ["Asia", "Europe", "North america", "South america", "Africa", "Australia"]

        if continent in continents:
            self.__continent = continent
        else:
            raise ValueError(f"Invalid continent name: '{continent}'. Must be one of {continents}")

    def __str__(self):
        return f"Country: {self.__name}, Capital: {self.__capital}, Continent: {self.__continent}"