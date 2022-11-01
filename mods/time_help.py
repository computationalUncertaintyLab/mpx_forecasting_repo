#mcandrew


def from_date_to_model_day(date):
    '''
    date: A string in the form YYYY-mm-dd
    returns an int that represents the number of days from 2020-03-11 to date
    '''
    import pandas as pd

    date = pd.to_datetime(date)
    reference_date = pd.to_datetime("2020-03-11")

    return (date - reference_date).days

if __name__ == "__main__":
    pass
