"""
                        This script includes unit tests for data transformations

                                            Guillaume A. Khayat
                                           guill.khayat@gmail.com
                                                2024-02-10
"""
import numpy as np
import pandas as pd
import pytest

# Import the functions to test
from modelselec.util.util_db import diff, diff_inv, ln_diff, ln_diff_inv

# DataFrames for testing
data1 = {'A': [1, 2, 3, 4],
        'B': [4, 6, 8, 10]}
df1 = pd.DataFrame(data1)
data2 = {'A': [1, 2, 3, 4]}
df2 = pd.DataFrame(data2)

data1_1_diff = {'A': [np.nan, 1, 1, 1],
             'B': [np.nan, 2, 2, 2]}
df1_1_diff = pd.DataFrame(data1_1_diff)
data2_1_diff = {'A': [np.nan, 1, 1, 1]}
df2_1_diff = pd.DataFrame(data2_1_diff)

data1_3_diff = {'A': [np.nan, np.nan, np.nan, 3],
             'B': [np.nan, np.nan, np.nan, 6]}
df1_3_diff = pd.DataFrame(data1_3_diff)
data2_3_diff = {'A': [np.nan, np.nan, np.nan, 3]}
df2_3_diff = pd.DataFrame(data2_3_diff)

data1_1_ln_diff = {'A': [np.nan, np.log(2)-np.log(1), np.log(3)-np.log(2), np.log(4)-np.log(3)],
             'B': [np.nan, np.log(6)-np.log(4), np.log(8)-np.log(6), np.log(10)-np.log(8)]}
df1_1_ln_diff = pd.DataFrame(data1_1_ln_diff)
data2_1_ln_diff = {'A': [np.nan, np.log(2)-np.log(1), np.log(3)-np.log(2), np.log(4) - np.log(3)]}
df2_1_ln_diff = pd.DataFrame(data2_1_ln_diff)

data1_3_ln_diff = {'A': [np.nan, np.nan, np.nan, np.log(4) - np.log(1)],
             'B': [np.nan, np.nan, np.nan, np.log(10) - np.log(4)]}
df1_3_ln_diff = pd.DataFrame(data1_3_ln_diff)
data2_3_ln_diff = {'A': [np.nan, np.nan, np.nan, np.log(4) - np.log(1)]}
df2_3_ln_diff = pd.DataFrame(data2_3_ln_diff)


@pytest.mark.parametrize("in_db, in_n, expected", [
    (df1, 1, df1_1_diff),
    (df2, 1, df2_1_diff),
    (df1, 3, df1_3_diff),
    (df2, 3, df2_3_diff)
])
def test_diff(in_db: pd.DataFrame, in_n: int, expected: pd.DataFrame):
    assert ( (diff(db=in_db, nTransf=in_n) == expected) |
             (diff(db=in_db, nTransf=in_n).isna() & expected.isna()) ).all().all()

@pytest.mark.parametrize("in_db, in_n, expected", [
    (df1, 1, df1_1_ln_diff),
    (df2, 1, df2_1_ln_diff),
    (df1, 3, df1_3_ln_diff),
    (df2, 3, df2_3_ln_diff)
])
def test_ln_diff(in_db: pd.DataFrame, in_n: int, expected: pd.DataFrame):
    assert ((ln_diff(db=in_db, nTransf=in_n) - expected < 10**(-10)) |
            (ln_diff(db=in_db, nTransf=in_n).isna() & expected.isna())).all().all()

@pytest.mark.parametrize("in_db, in_n, in_t0, expected", [
    (df1_1_diff, 1, df1.loc[[0]], df1),
    (df1_1_diff.dropna(), 1, df1.loc[[0]], df1),
    (df2_1_diff, 1, df2.loc[[0]], df2),
    (df2_1_diff.dropna(), 1, df2.loc[[0]], df2),
    (df1_3_diff, 3, df1.loc[:2], df1),
    (df1_3_diff.dropna(), 3, df1.loc[:2], df1),
    (df2_3_diff, 3, df2.loc[:2], df2),
    (df2_3_diff.dropna(), 3, df2.loc[:2], df2),
])
def test_diff_inv(in_db: pd.DataFrame, in_n: int, in_t0: pd.DataFrame, expected: pd.DataFrame):
    assert ((diff_inv(db=in_db, nTransf=in_n, t0=in_t0) - expected < 10**(-12)) |
            (diff_inv(db=in_db, nTransf=in_n, t0=in_t0).isna() & expected.isna())).all().all()

@pytest.mark.parametrize("in_db, in_n, in_t0, expected", [
    (df1_1_ln_diff, 1, df1.loc[[0]], df1),
    (df1_1_ln_diff.dropna(), 1, df1.loc[[0]], df1),
    (df2_1_ln_diff, 1, df2.loc[[0]], df2),
    (df2_1_ln_diff.dropna(), 1, df2.loc[[0]], df2),
    (df1_3_ln_diff, 3, df1.loc[:2], df1),
    (df1_3_ln_diff.dropna(), 3, df1.loc[:2], df1),
    (df2_3_ln_diff, 3, df2.loc[:2], df2),
    (df2_3_ln_diff.dropna(), 3, df2.loc[:2], df2),
])
def test_ln_diff_inv(in_db: pd.DataFrame, in_n: int, in_t0: pd.DataFrame, expected: pd.DataFrame):
    assert ((ln_diff_inv(db=in_db, nTransf=in_n, t0=in_t0) - expected < 10**(-12)) |
            (ln_diff_inv(db=in_db, nTransf=in_n, t0=in_t0).isna() & expected.isna())).all().all()