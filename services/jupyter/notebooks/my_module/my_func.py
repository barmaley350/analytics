"""docstring."""

import pandas as pd


def highlight_values(
    value: pd.Series, *, threshold_null: int = 30, threshold_uniq: int = 10
) -> list:
    """Выделение значений цветом.

    :param va: _description_
    :type va: int
    :return: _description_
    :rtype: str
    """
    rez = ["background-color: transparent"] * len(value.index.to_list())
    for idx, ind in enumerate(value.index.to_list()):
        if (
            ind == "Uniq Count %"
            and value["Uniq Count %"] <= threshold_uniq
            and "String" in value["type"]
        ):
            rez[idx] = "color: black; background-color: green"

        if ind == "Null Count %":
            if value["Null Count %"] > 0 and value["Null Count %"] < threshold_null:
                rez[idx] = "color: black; background-color: yellow"
            elif value["Null Count %"] >= threshold_null:
                rez[idx] = "color: black; background-color: #ffcccc"
    return rez


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


def get_uniq_estimation(row: pd.Series, threshold: int = 30) -> str:
    """Get Description.

    :param row: _description_
    :type row: pd.Series
    :param threshold: _description_, defaults to 30
    :type threshold: int, optional
    :return: _description_
    :rtype: str
    """
    null_percent = row["Uniq Count %"]
    field_type = row["type"]

    return (
        "LowCardinality" if null_percent <= threshold and "String" in field_type else ""
    )
