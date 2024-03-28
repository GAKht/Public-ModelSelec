"""
                        This script includes useful metric and performance measures
                            to be used before and/or after model estimation

                                            Guillaume A. Khayat
                                           guill.khayat@gmail.com
                                                2024-02-10
"""

from modelselec.modules_paths import *
from sklearn.metrics import (root_mean_squared_error, accuracy_score, precision_score, recall_score, f1_score,
                             confusion_matrix)
from modelselec.util.util_db import diff, ln_diff

def perf_metrics(obs: pd.DataFrame, pred: pd.DataFrame, y_type: str = 'num', transf: str = None) -> dict:
    """
    This function returns useful metrics that quantify how well our model forecast the dependent variable
    :param obs: pd.DataFrame of 1 column which includes the observed historical data of the dependent variable
    :param pred: pd.DataFrame of 1 column which includes the model predicted values of the dependent variable
    :param y_type: str, 'num' if the dependent variable is numerical and 'categ' if the dependent variable
                    is categorical
    :param transf: str,
    :return: dict, a dictionary with the relevant forecasting performance metrics
                    (depending on the type of the dependent variable)
    """

    if obs.columns != pred.columns:
        raise Exception('Both observed and predicted dataframes should have the same column name')
    if len(obs.columns) != 1:
        raise Exception('Computing the performance metrics is possible only for 1 series at a time')
    if y_type not in ['num', 'categ']:
        raise Exception('"y_type" should be either "num" if the dependent variable is numerical or '
                        '"categ" if the dependant variable is categorical')
    if (y_type == 'num') and (transf is None):
        raise Exception("'transf' can't be None if the dependent variable is numerical")
    if (transf is not None):
        if (transf.lower() not in ['lvl', 'diff', 'diffln']):
            raise Exception("'transf' should be None if the dependent variable is categorical or one of the following "
                            "transformations if the dependent variable is numerical ['lvl', 'diff', 'diffln']")

    y_type = y_type.lower()

    if y_type == 'num':
        abs_prct_errors = np.abs( (obs - pred)/(obs + 10**(-10)) )
        mape = np.mean(abs_prct_errors)

        lvl_corr = pred[obs.columns[0]].astype('float64').corr(obs[obs.columns[0]].astype('float64'))

        rmse = root_mean_squared_error(y_true=obs, y_pred=pred)
        nrmse = rmse/np.mean(obs)

        if transf.lower() == 'diff':
            diff_corr = (diff(db=pred, nTransf=1).dropna()[obs.columns[0]].astype('float64').
                         corr(diff(db=obs, nTransf=1).dropna()[obs.columns[0]].astype('float64')))
            return {'lvlCorr': lvl_corr, 'diffCorr': diff_corr, 'RMSE': rmse, 'NRMSE': nrmse, 'MAPE': mape}
        elif transf.lower() == 'diffln':
            ln_diff_corr = (ln_diff(db=pred, nTransf=1).dropna()[obs.columns[0]].astype('float64').
                             corr(ln_diff(db=obs, nTransf=1).dropna()[obs.columns[0]].astype('float64')))
            return {'lvlCorr': lvl_corr, 'diffLnCorr': ln_diff_corr, 'RMSE': rmse, 'NRMSE': nrmse, 'MAPE': mape}
        elif transf.lower() == 'lvl':
            return {'lvlCorr': lvl_corr, 'RMSE': rmse, 'NRMSE': nrmse, 'MAPE': mape}
    elif y_type == 'categ':
        accuracy = accuracy_score(obs, pred)
        precision = precision_score(obs, pred, average=None)
        recall = recall_score(obs, pred, average=None)
        f1 = f1_score(obs, pred, average=None)
        conf_matrix = confusion_matrix(obs, pred)
        return {'accuracy': accuracy, 'precision': precision, 'recall': recall, 'f1': f1, 'conf_matrix': conf_matrix}