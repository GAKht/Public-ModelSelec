"""
                        This script includes useful data transformation to be used
                                    before and/or after model estimation

                                            Guillaume A. Khayat
                                           guill.khayat@gmail.com
                                                2024-02-06
"""
from modelselec.modules_paths import *


def check_file_exists(instance, attribute, value) -> None:
    """
    This validator checks if a file exists in a given path and raises a ValueError if it does not
    :param instance: DBhist, the class instance to be check during creation
    :return: None
    """
    if not os.path.isfile(f'{instance.path_db}{instance.file_name}.{instance.file_type}'):
        raise ValueError(f"The file {instance.file_name}.{instance.file_type} does not exist.")

def diff(db: pd.DataFrame, nTransf: int) -> pd.DataFrame:
    """
    This function calculates the x(t)-x(t-n) value for each column in a dataframe
    :param db: pd.DataFrame, each of its columns are in level and their difference need to be calculated
    :param nTransf: int, how many periods should we look back to calculate the difference
    :return: pd.DataFrame, the same number of columns and rows as db. Each column is the difference based on nTransf
                observations backwards
    """
    dbDiff = db.astype(float).diff(periods=nTransf)
    return dbDiff

def ln_diff(db: pd.DataFrame, nTransf: int) -> pd.DataFrame:
    """
    This function calculates the ln(x(t))-ln(x(t-n)) value for each column in a dataframe
    :param db: pd.DataFrame, each of its columns are in level and their difference need to be calculated
    :param nTransf: int, how many periods should we look back to calculate the difference
    :return: pd.DataFrame, the same number of columns and rows as db. Each column is the difference ln based on nTransf
                observations backwards
    """
    dbLogDiff = np.log(db.astype(float)).diff(periods=nTransf)
    return dbLogDiff

def diff_inv(db: pd.DataFrame, nTransf: int, t0: pd.DataFrame) -> pd.DataFrame:
    """
    This function receives as input a databased based on differences and the initial level values and returns
    the level values
    :param db: pd.DataFrame, the difference datarame
    :param nTransf: int, the number of periods we looked back to calculate the difference
    :param t0: pd.DataFrame, the initial level values
    :return: pd.DataFrame of the same columns with the level values
    """
    if len(t0) < nTransf:
        raise Exception('The number of provided historical observations should be at least as large as the number '
                        'of the backward observations from which the difference was calculated')
    dbInt = db.copy()
    if db.isna().any().any():
        dbInt = dbInt.dropna()
    dbInt.reset_index(inplace=True, drop=True)
    if len(dbInt) > 1:
        t0.reset_index(inplace=True, drop=True)
        t0Loop = t0.tail(nTransf)
        t0Loop.reset_index(drop=True, inplace=True)
        t0Loop = pd.concat(objs=[t0, dbInt.head(1) + t0Loop.iloc[[0, ]]], axis='index')
        diffDB = dbInt.iloc[1:, ]
        return diff_inv(db=diffDB, nTransf=nTransf, t0=t0Loop)
    else:
        t0.reset_index(inplace=True, drop=True)
        t0Loop = t0.tail(nTransf)
        t0Loop.reset_index(drop=True, inplace=True)
        t0Loop = pd.concat(objs=[t0, dbInt.head(1) + t0Loop.iloc[[0, ]]], axis='index', ignore_index=True)
        return t0Loop


def ln_diff_inv(db: pd.DataFrame, nTransf: int, t0: pd.DataFrame) -> pd.DataFrame:
    """
    This function receives as input a databased based on differences of ln() and the initial level values and returns
    the level values
    :param db: pd.DataFrame, the difference of ln() datarame
    :param nTransf: int, the number of periods we looked back to calculate the difference
    :param t0: pd.DataFrame, the initial level values
    :return: pd.DataFrame of the same columns with the level values
    """
    if len(t0) < nTransf:
        raise Exception('The number of provided historical observations should be at least as large as the number '
                        'of the backward observations from which the difference was calculated')

    lvl_log = diff_inv(db=db, nTransf=nTransf, t0=np.log(t0))
    return np.exp(lvl_log)
