"""Get Available Rates module."""

from typing import List

import pandas


def get_rates(
    score: int, min_term: int, valid_terms: List[int], csv: str
) -> pandas.Series:
    """Get Available Rates for current Model and Borrower.

    This method can be used in PyCharm Scientific Mode.
    To do this, please uncomment test values inside each Cell.

    :param score: Borrower current score
    :param min_term: Borrower selected term
    :param valid_terms: Current Policy valid terms
    :param csv: CSV filename
    :return: pandas.Series
    """
    # %%
    import os
    from pathlib import Path
    import pandas

    # Uncomment in scientific mode for tests
    # csv = "noverde_rate_model"

    current_dir = os.getcwd()
    data_frame_path = Path().joinpath(
        current_dir, "noverde_challenge", "policies", "data", f"{csv}.csv",
    )
    df = pandas.read_csv(data_frame_path)
    df.set_index("score", inplace=True)
    # %%
    # Uncomment in scientific mode for tests
    # valid_terms = [6, 9, 12]
    # score = 600
    # min_term = 9

    available_terms = [str(term) for term in valid_terms if term >= min_term]
    # %%
    index = int(score / 100) * 100
    if index < df.index.min():
        return pandas.Series()
    if index > df.index.max():
        index = df.index.max()
    filtered_rates = df.filter(items=available_terms)
    available_rates = filtered_rates.loc[index]
    # %%
    return available_rates
