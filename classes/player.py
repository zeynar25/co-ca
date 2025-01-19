class Player():
    def __init__(self, id, user, score, mode, category, option, duration, record_date):
        self.__id = id
        self.__user = user
        self.__score = score
        self.__mode = mode
        self.__category = category
        self.__option = option
        self.__duration = duration
        self.__record_date = record_date

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, value):
        self.__user = value

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, value):
        self.__score = value

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, value):
        self.__mode = value

    @property
    def category(self):
        return self.__category

    @category.setter
    def category(self, value):
        self.__category = value

    @property
    def option(self):
        return self.__option

    @option.setter
    def option(self, value):
        self.__option = value

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, value):
        self.__duration = value

    @property
    def record_date(self):
        return self.__record_date

    @record_date.setter
    def record_date(self, value):
        self.__record_date = value