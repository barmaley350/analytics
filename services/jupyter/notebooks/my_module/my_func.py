"""docstring."""

import pandas as pd


def highlight_values(value: float, threshold: int = 30) -> str:
    """Выделение значений цветом.

    :param va: _description_
    :type va: int
    :return: _description_
    :rtype: str
    """
    try:
        float_val = float(value)
    except TypeError:
        return "background-color: red"
    else:
        if float_val > 0 and float_val < threshold:
            return "color: black; background-color: yellow"
        if float_val >= threshold:
            return "color: black; background-color: #ffcccc"

        return "background-color: transparent"


def get_null_exists_estimation(row: pd.Series, threshold: int = 30) -> str:
    """Get Description.

    :param row: _description_
    :type row: pd.Series
    :param threshold: _description_, defaults to 30
    :type threshold: int, optional
    :return: _description_
    :rtype: str
    """
    null_percent = row["Null Count %"]
    null_count = row["Null Count"]
    rez = ""
    if null_count > 0 and null_percent >= threshold:
        rez = "Много"
    elif null_count > 0 and null_percent < threshold:
        rez = "Мало"
    return rez
