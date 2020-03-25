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

    print(df)


if __name__ == '__main__':
    pd.set_option('display.max_columns', None)
    read_csv(
        "https://gist.githubusercontent.com/gfelot/de17feb69320fff0a3bf1d59b9d42a06/raw/af6fcd62000b92cae8b80b285380cc7b66044a12/mock_data.tsv",
        '\t')