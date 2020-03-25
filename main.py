import pandas as pd
import numpy as np


def convert_big_number2(nb):
    """
        Convert string in a form $XX.YYM or $XX.YYB into a numeric type to make possible future calculation
        :param nb: str representing a number in a df row
        :return: return the str converted into an int
    """
    if nb != 'n/a':
        nb = nb.replace('$', '')
        multiplicator = 1
        if 'M' in nb:
            multiplicator = 1000 * 1000
            nb = nb.replace('M', '')
        elif 'B' in nb:
            multiplicator = 1000 * 1000 * 1000
            nb = nb.replace('B', '')
        return int(float(nb) * multiplicator)
    else:
        return 0


def calc_ratio(nb_list):
    """
    Calculate a ration between nb[1] / nb[0] in %
    :param nb_list: list of the two number to evaluate
    :return: float rounded at 2 decimals
    """
    if nb_list[0] == 0:
        return 100
    elif nb_list[1] == 0:
        return 0
    else:
        return round(nb_list[1] / nb_list[0] * 100, 2)


def columns_list(csv_uri, sep):
    """
        Create a list of columns name from a csv.
        :param: csv_uri: uri of the csv
        :param: sep: separator
        :return: return list of csv
    """
    return list(pd.read_csv(
        csv_uri,
        sep=sep,
        nrows=1))


def compare_df_gain(csv_uri, sep, df_optimized):
    """
    Compare the original size of a df without optimization and the same source but with optimization
    :param csv_uri: original uri to request without optimization
    :param sep: separator to use on the original data
    :param df_optimized: pandas dataframe optimized
    """
    df_original = pd.read_csv(
        csv_uri,
        sep=sep)
    original_size = df_original.memory_usage(deep=True).sum()
    optimized_size = df_optimized.memory_usage(deep=True).sum()
    print(original_size)
    print(optimized_size)
    print('Gain : ' + str((1 - optimized_size / original_size) * 100))


def read_csv(csv_uri, sep):
    """
        Read a csv and optimize it's import into a DataFrame.
        :param: csv_uri: uri of the csv
        :param: sep: separator
        :return: Pandas DataFrame
    """
    cols = columns_list(csv_uri, sep)

    df = pd.read_csv(
        csv_uri,
        sep=sep,
        index_col='id',
        dtype={
            'id': 'int32',
            'latitude': 'float32',
            'longitude': 'float32'
        },
        usecols=[i for i in cols if i != 'very_important'],
        converters={
            '2018': convert_big_number2,
            '2019': convert_big_number2,
            'genre': lambda x: np.where(x == "F", True, False)
        }
    )

    # Drop useless rows if `latitude` or `longitude` is NaN
    df = df.dropna(subset=['latitude', 'longitude'])
    # reformat all headers columns name
    df.rename(columns=lambda x: x.lower(), inplace=True)
    # build a `start_dat` column based on `day`, `month`, `year`, then drop the least
    df['start_date'] = pd.to_datetime(df[['day', 'month', 'year']], dayfirst=True)
    df = df.drop(columns=['day', 'month', 'year'])
    # convert genre from str to bool with F = True
    df['genre'] = df['genre'].astype('bool')
    # apply calc_ration to recalculation the values in this column
    df['ratio'] = df[['2018', '2019']].apply(calc_ratio, axis=1)
    # compare the gain with the original df w/o optimization
    compare_df_gain(csv_uri, sep, df)


if __name__ == '__main__':
    pd.set_option('display.max_columns', None)
    read_csv(
        "https://gist.githubusercontent.com/gfelot/de17feb69320fff0a3bf1d59b9d42a06/raw/af6fcd62000b92cae8b80b285380cc7b66044a12/mock_data.tsv",
        '\t')