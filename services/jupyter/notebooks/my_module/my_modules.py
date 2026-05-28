"""docstring."""

from io import StringIO

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


def parse_info(df: pd.DataFrame) -> tuple[int, int, str, list[str]]:
    """Парсим вывод df.info().

    :param df: _description_
    :type df: pd.DataFrame
    :return: _description_
    :rtype: tuple[int, str, list[str]]
    """
    buffer = StringIO()
    df.info(buf=buffer)
    info_text = buffer.getvalue()

    lines = info_text.split("\n")
    data = []
    total_rows = 0
    null_count_total = 0

    dtypes = ""
    for line in list(map(str.strip, lines)):
        if "RangeIndex" in line:
            parts = list(map(str.strip, line.split()))
            total_rows = int(parts[1])
        if "dtypes" in line:
            parts = list(map(str.strip, line.split()))
            dtypes = ", ".join(list(map(str.strip, "".join(parts[1:]).split(","))))

        if line and line[0].isdigit():
            parts = line.split()
            col_name = parts[1]
            non_null = parts[2]
            dtype = "".join(parts[4:])

            non_null_count = int(non_null.replace("non-null", ""))
            null_count_total += total_rows - non_null_count

            data.append({
                "Column": col_name,
                "Non-Null Count": non_null_count,
                "Non-Null Count %": round((non_null_count * 100) / total_rows, 2),
                "Null Count": total_rows - non_null_count,
                "Null Count %": round(
                    ((total_rows - non_null_count) * 100) / total_rows, 2
                ),
                "Total Rows": total_rows,
                "Dtype": dtype,
            })
    return total_rows, null_count_total, dtypes, data


def custom_info(df: pd.DataFrame) -> tuple[int, int, str, pd.DataFrame]:
    """Преобразование стандартного df.info().

    :param df: _description_
    :type df: pd.DataFrame
    :return: _description_
    :rtype: tuple[int, str, pd.DataFrame]
    """
    total_rows, null_count_total, dtypes, data = parse_info(df)
    df_styled = pd.DataFrame(data)
    styled_df = df_styled.style.map(highlight_values, subset=["Null Count %"])  # type: ignore
    return total_rows, null_count_total, dtypes, styled_df


if __name__ == "__main__":
    pass
