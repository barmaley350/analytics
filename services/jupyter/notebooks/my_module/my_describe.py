"""docstring."""

import pandas as pd


def highlight_values(val: int) -> str:
    """Выделение значений цветом.

    :param va: _description_
    :type va: int
    :return: _description_
    :rtype: str
    """
    try:
        float_val = float(val)
    except TypeError:
        return "background-color: white"
    else:
        color = "yellow" if float_val > 0 else "white"
        return f"background-color: {color}"


def parse_describe(
    totals: dict, df: dict, sample_count: int, fields: list[str]
) -> dict:
    """Парсим вывод df.info().

    :param df: _description_
    :type df: pd.DataFrame
    :return: _description_
    :rtype: tuple[int, str, list[str]]
    """
    # print(df)
    data = {}
    for field in fields:
        data[f"avg_{field}"] = {}
        for i in range(sample_count):
            for key in df[f"df{i + 1}_{field}"]:
                data[f"avg_{field}"].setdefault(key, 0)
                data[f"avg_{field}"][key] += df[f"df{i + 1}_{field}"][key]

    for key in data:
        for field in data[key]:
            data[key][field] /= sample_count

    # print({**df, **data})
    return {**df, **data, **totals}


def custom_describe(
    totals: pd.DataFrame, df: pd.DataFrame, sample_count: int, fields: list[str]
) -> pd.DataFrame:
    """Преобразование стандартного df.info().

    :param df: _description_
    :type df: pd.DataFrame
    :return: _description_
    :rtype: tuple[int, str, pd.DataFrame]
    """
    data = parse_describe(totals.to_dict(), df.to_dict(), sample_count, fields)
    # df_styled = pd.DataFrame(data)
    # styled_df = df_styled.style.map(highlight_values, subset=["Null Count %"])  # type: ignore
    return pd.DataFrame(data)


if __name__ == "__main__":
    pass
