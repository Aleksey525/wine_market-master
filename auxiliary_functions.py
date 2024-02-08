import datetime


def get_word_chape(delta_years):
    no_third = delta_years % 100
    if no_third in range(11, 20):
        return "лет"
    last = no_third % 10
    if last == 1:
        return "год"
    if last in range(2, 5):
        return "года"
    else:
        return "лет"


def get_delta_years(foundation_year=1920):
    this_year = datetime.datetime.now().year
    return this_year - foundation_year