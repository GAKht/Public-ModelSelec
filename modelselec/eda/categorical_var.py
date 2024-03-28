"""
                        This script includes functions useful for Exploratory Data Analysis
                                         for categorical variables

                                            Guillaume A. Khayat
                                           guill.khayat@gmail.com
                                                2024-02-11
"""
from modelselec.modules_paths import *


def categorical_categorical_crosstab(db: pd.DataFrame, var1: str, var2: str, normalize: str = None,
                                     path_save: str = None):
    """
    This function creates the cross tabulation table between two categorical variables var1 and var2
    :param db: pd.DataFrame, the dataframe which contain the two categorical variables
    :param var1: str, the name of the first categorical variable
    :param var2: str, the name of the second categorical variable
    :param normalize: str, optional, the input should be provided if the desired crosstab should be normalizd.
                        Only 'all', 'index' or 'columns' are allowed
    :param path_save: str, optional, needed if the plot should be saved instead of shown in a pop-up window
    :return: pd.DataFrame or None if path_save is provided
    """
    if normalize is not None and normalize.lower() not in ['all', 'columns', 'index']:
        raise Exception(f"Invalid value for 'normalize': {normalize}. Only 'all', 'columns' or 'index' are allowed.")

    normalize_str = str(normalize).lower()

    cross_tabular = pd.crosstab(db[var1], db[var2], normalize=normalize_str if normalize_str != 'none' else False)

    if normalize_str == 'columns':
        cross_tabular_first_sum = pd.concat(objs=[cross_tabular,
                                                  pd.DataFrame(data=[cross_tabular.sum()], index=['Total'],
                                                               columns=cross_tabular.columns)], axis='index')
    else:
        cross_tabular_first_sum = pd.concat(objs=[cross_tabular, pd.DataFrame(cross_tabular.sum(axis='columns'),
                                                                              columns=['Total'])], axis='columns')

    if normalize_str in ['none', 'all']:
        cross_tabular_final = pd.concat(objs=[cross_tabular_first_sum,
                                              pd.DataFrame(data=[cross_tabular.sum()], index=['Total'],
                                                           columns=cross_tabular_first_sum.columns)], axis='index')
    else:
        cross_tabular_final = cross_tabular_first_sum

    cross_tabular_final.insert(loc=0, column=var1, value=cross_tabular_final.index)
    cross_tabular_final.reset_index(drop=True, inplace=True)
    cross_tabular_final.index.name = None
    cross_tabular_final.columns.name = None


    if path_save is not None:
        cross_tabular_final.to_csv(path_or_buf=f'{path_save}crosstabular_{var1}_{var2}.csv', index=False)

    return cross_tabular_final

