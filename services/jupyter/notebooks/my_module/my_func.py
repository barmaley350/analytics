"""docstring."""


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
