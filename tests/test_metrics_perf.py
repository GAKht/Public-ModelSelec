"""
                        This script includes unit tests for performance metrics

                                            Guillaume A. Khayat
                                           guill.khayat@gmail.com
                                                2024-02-10
"""
import numpy as np
import pandas as pd
import pytest

from modelselec.util.util_perf import (perf_metrics, accuracy_score, precision_score, recall_score, f1_score,
                                       confusion_matrix)

dataObs = {'A': [2, 1, 5, 7]}
dfObs = pd.DataFrame(dataObs)
dataPred = {'A': [4, 2, 2, 1]}
dfPred = pd.DataFrame(dataPred)
dataCategObs = {'A': ['a', 'b', 'c']}
dfCategObs = pd.DataFrame(dataCategObs)
dataCategPred = {'A': ['a', 'c', 'b']}
dfCategPred = pd.DataFrame(dataCategPred)

rmse = np.sqrt(((4-2)**2 + (2-1)**2 + (2-5)**2 + (1-7)**2)/4)
nrmse = rmse/((2+1+5+7)/4)
mape = ( (2/2) + 1/1 + 3/5 + 6/7 )/4
lvlCorr = dfObs['A'].corr(dfPred['A'])
diffCorr = dfObs['A'].diff().corr(dfPred['A'].diff())
diffLnCorr = np.log(dfObs['A']).diff().corr(np.log(dfPred['A']).diff())

accuracy = accuracy_score(dfCategObs, dfCategPred)
precision = precision_score(dfCategObs, dfCategPred, average=None)
recall = recall_score(dfCategObs, dfCategPred, average=None)
f1 = f1_score(dfCategObs, dfCategPred, average=None)
conf_matrix = confusion_matrix(dfCategObs, dfCategPred)

def round_dict_values(d, decimals=6):
    return {k: round(v, decimals) if isinstance(v, float) else v for k, v in d.items()}


expectedLvl = {'lvlCorr': lvlCorr, 'RMSE': rmse, 'NRMSE': nrmse, 'MAPE': mape}
expectedDiff = {'lvlCorr': lvlCorr, 'diffCorr': diffCorr, 'RMSE': rmse, 'NRMSE': nrmse, 'MAPE': mape}
expectedDiffLn = {'lvlCorr': lvlCorr, 'diffLnCorr': diffLnCorr, 'RMSE': rmse, 'NRMSE': nrmse, 'MAPE': mape}
expectedCateg = {'accuracy': accuracy, 'precision': precision, 'recall': recall, 'f1': f1, 'conf_matrix': conf_matrix}



@pytest.mark.parametrize("in_obs, in_pred, in_y_type, in_transf, expected", [
    (dfObs, dfPred, 'num', 'lvl', expectedLvl),
    (dfObs, dfPred, 'num', 'diff', expectedDiff),
    (dfObs, dfPred, 'num', 'diffLn', expectedDiffLn),
    (dfCategObs, dfCategPred, 'categ', None, expectedCateg)
])
def test_perf_metrics(in_obs: pd.DataFrame, in_pred: pd.DataFrame, in_y_type: str, in_transf, expected: dict):
    if in_y_type == 'num':
        assert (round_dict_values(perf_metrics(obs=in_obs, pred=in_pred, y_type=in_y_type, transf=in_transf)) ==
                round_dict_values(expected))
    elif in_y_type == 'categ':
        assert (round(perf_metrics(obs=in_obs, pred=in_pred, y_type=in_y_type, transf=in_transf)['accuracy'], 6) ==
                round(expected['accuracy'], 6))
        assert list(map(lambda metric: np.array_equal(perf_metrics(obs=in_obs, pred=in_pred, y_type=in_y_type,
                                                                   transf=in_transf)[metric].tolist(),
                                                      expected[metric].tolist()),
                        ['precision', 'recall', 'f1', 'conf_matrix']))