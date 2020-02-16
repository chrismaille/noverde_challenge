"""Application Helpers."""


def only_numbers(value: str) -> str:
    """Return only numbers from string.

    :param value: string
    :return: string
    """
    return "".join([character for character in value if character.isdigit()])
