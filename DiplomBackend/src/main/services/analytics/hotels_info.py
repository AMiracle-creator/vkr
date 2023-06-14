import pandas as pd


def make_age_clusters(df, min_age, max_age):
    result = df.query(f'visitors_avarage_age>={min_age} and visitors_avarage_age<{max_age}').values.tolist()

    return result


def get_hotel(df, hotel_id):
    result = df.query(f'hotel_id=={hotel_id}').values.tolist()

    return result


def get_period_info(df, first_date, second_date):
    print(first_date)
    print(second_date)
    total = df.query(f"arrivaldate>='{first_date}' and arrivaldate<'{second_date}'")
    total = len(total)
    print(total)
    # df = df.groupby('arrivaldate')['amount'].count().reset_index()
    # date = df['date'].tolist()
    # date_amount = df['amount'].tolist()

    date = ['2019-01-01', '2019-02-01']
    date_amount = [100, 200]

    return total, date, date_amount
