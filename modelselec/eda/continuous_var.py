"""
                        This script includes functions useful for Exploratory Data Analysis
                                         for continuous variables

                                            Guillaume A. Khayat
                                           guill.khayat@gmail.com
                                                2024-02-11
"""
from modelselec.modules_paths import *


def continuous_categorical_stats(db: pd.DataFrame, continuous_var: str, categorical_var: str, relative: bool = False,
                                 base_categorical_var: str = None,
                                 path_save: str = None):
    """
    This function reports the mean and median of a continuous variable when these are calculated based
    on grouped observations by the categroies of the categorical variable
    :param db: pd.DataFrame, the dataframe which contain the categorical and continuous data
    :param categorical_var: str, the name of the categorical variable
    :param continuous_var: str, the name of the continuous variable
    :param relative: boolean, optional, True if the ratio of the statistic relative to a base category
    :param base_categorical_var: str, optional, the base category to be used when calculating the relative ratios
    :param path_save:, str, optional, needed if the plot should be saved instead of shown in a pop-up window
    :return: pd.DataFrame if no path_save is provided and None if it is provided,
    """
    if (base_categorical_var is not None) and (not relative):
        raise Exception('base_categorical_var should be None if relative is different from True')

    categs = list(set(db[categorical_var]))
    categs.sort()
    dictData = {}
    list(map(lambda categ: dictData.update({categ: [np.mean(db[continuous_var][db[categorical_var] == categ]),
                                                    np.median(db[continuous_var][db[categorical_var] == categ])]}),
             categs))
    stat_df = pd.DataFrame(dictData)
    stat_df = stat_df.transpose()
    stat_df.columns = ['Mean', 'Median']
    if relative:
        if base_categorical_var is None:
            base_categorical_var = categs[0]
        stat_df = stat_df.div(stat_df.loc[base_categorical_var])
        stat_df = stat_df.drop(base_categorical_var)
        stat_df.index = [row + '/' + base_categorical_var for row in list(stat_df.index)]

    if path_save is not None:
        stat_df.to_csv(path_or_buf=path_save + continuous_var + '_' + categorical_var + '_stats.csv')

    return stat_df


def continuous_categorical_overlap_histogram(db: pd.DataFrame, continuous_var: str, categorical_var: str,
                                             path_save: str = None):
    """
    This function plots overlapping histograms of a continuous variable when considered the categorical variable has
    different values
    :param db: pd.DataFrame, the dataframe which contain the categorical and continuous data
    :param categorical_var: str, the name of the categorical variable
    :param continuous_var: str, the name of the continuous variable
    :param path_save:, str, optional, needed if the plot should be saved instead of shown in a pop-up window
    :return: None
    """

    plt.close('all')
    plt.figure(figsize=(8, 6))
    if path_save is not None:
        plt.ioff()
    categs = list(set(db[categorical_var]))
    for i in range(len(categs)):
        series = db[continuous_var][db[categorical_var] == categs[i]]
        plt.hist(series, label=categs[i], color=colorsPyPlot[i], density=True, alpha=0.5)
    plt.legend()

    if path_save is not None:
        file_name = categorical_var + '_' + continuous_var + '_overlap_hist'
        plt.savefig(path_save + file_name + '.png')
        plt.ion()
    else:
        plt.show()


def continuous_categorical_boxplot(db: pd.DataFrame, continuous_var: str, categorical_var: str, path_save: str = None):
    """
    This function plots (shows or saves) the boxplot of a categorical variable in x-axis and
    a continuous variable in y-axis
    :param db: pd.DataFrame, the dataframe which contain the categorical and continuous data
    :param categorical_var: str, the name of the categorical variable
    :param continuous_var: str, the name of the continuous variable
    :param path_save: str, optional, needed if the plot should be saved instead of shown in a pop-up window
    :return: None
    """

    plt.close('all')
    plt.figure(figsize=(8, 6))
    if path_save is not None:
        plt.ioff()
    sns.boxplot(data=db, x=categorical_var, y=continuous_var, hue=categorical_var,
                palette=colorsPyPlot[:len(list(set(db[categorical_var])))])

    if path_save is not None:
        file_name = categorical_var + '_' + continuous_var + '_boxplot'
        plt.savefig(path_save + file_name + '.png')
        plt.ion()
    else:
        plt.show()


def continuous_continuous_scatter(db: pd.DataFrame, x_var: str, y_var: str, path_save: str = None):
    """
    This function's output is a scatter plot of two continuous variables x_var and y_var
    :param db: pd.DataFrame, the dataframe which contain the two continuous variables
    :param x_var: str, the first continuous variable to be plotted on the x-axis
    :param y_var: str, the second continuous variable to be plotted on the y-axis
    :param path_save: str, optional, needed if the plot should be saved instead of shown in a pop-up window
    :return: None
    """
    plt.figure(figsize=(8, 6))
    if path_save is not None:
        plt.ioff()
    plt.scatter(x=db[x_var], y=db[y_var])
    plt.xlabel(x_var)
    plt.ylabel(y_var)
    if path_save is not None:
        file_name = x_var + '_' + y_var + '_scatter'
        plt.savefig(path_save + file_name + '.png')
        plt.ion()
    else:
        plt.show()


def continuous_continuous_heatmap(db: pd.DataFrame, var_list: list, path_save: str = None):
    """
    Produces the correlation heatmap of a list of variables in a pandas dataframe
    :param db: pd.DataFrame, the dataframe which includes the observations of the variables of interest
    :param var_list: list of strings, the list of column names representing the variables of interest in the dataframe
    :param path_save: str, optional, the path where the .png file should be saved
    :return: None
    """
    if path_save is not None:
        plt.ioff()
    plt.figure(figsize=(8, 6))
    sns.heatmap(db[var_list].corr(), annot=True, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1)
    plt.title('Correlation Heatmap')
    if path_save is not None:
        file_name = var_list[0] + '_--_' + var_list[len(var_list) - 1] + '_heatmap'
        plt.savefig(path_save + file_name + '.png')
        plt.ion()
    else:
        plt.show()
