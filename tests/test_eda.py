"""
                            This script includes unit tests for eda functions

                                            Guillaume A. Khayat
                                           guill.khayat@gmail.com
                                                2024-02-11
"""
import pytest, os
import pandas as pd
from modelselec.eda.categorical_var import categorical_categorical_crosstab
from modelselec.eda.continuous_var import continuous_continuous_heatmap, continuous_categorical_stats, \
    continuous_categorical_boxplot, continuous_continuous_scatter, continuous_categorical_overlap_histogram
from pandas.testing import assert_frame_equal

path_tests_in = os.path.dirname(__file__) + '/tests_in/'
path_tests_out = os.path.dirname(__file__) + '/tests_out/'
if not os.path.exists(path_tests_out):
    os.makedirs(path_tests_out)

db = pd.read_csv(filepath_or_buffer=path_tests_in + 'categ_cont_vars.csv')
class_categs = list(set(db['class']))

db_cont = pd.read_csv(filepath_or_buffer=path_tests_in + 'cont_cont_vars.csv')


def test_continuous_categorical_overlap_histogram():
    path_file = path_tests_out + 'class_txId_overlap_hist.png'
    if os.path.exists(path_file):
        os.remove(path_file)
    continuous_categorical_overlap_histogram(db=db, continuous_var='txId', categorical_var='class',
                                             path_save=path_tests_out)
    assert os.path.exists(path_file)
    if os.path.exists(path_file):
        os.remove(path_file)


def test_continuous_categorical_boxplot():
    path_file = path_tests_out + 'class_txId_boxplot.png'
    if os.path.exists(path_file):
        os.remove(path_file)
    continuous_categorical_boxplot(db=db, continuous_var='txId', categorical_var='class', path_save=path_tests_out)
    assert os.path.exists(path_file)
    if os.path.exists(path_file):
        os.remove(path_file)


@pytest.mark.parametrize("norm", [
    (None),
    ('all'),
    ('columns'),
    ('index')
])
def test_categorical_categorical_crosstab(norm):
    path_file = path_tests_out + f'crosstabular_class_random_categ.csv'
    if os.path.exists(path_file):
        os.remove(path_file)
    crosstab = categorical_categorical_crosstab(db=db, var1='class', var2='random_categ', normalize=norm,
                                                path_save=path_tests_out)
    if norm is None:
        expected = pd.read_csv(filepath_or_buffer=path_tests_in + 'crosstabular_class_random_categ_none.csv')
    else:
        match norm:
            case 'all':
                expected = pd.read_csv(filepath_or_buffer=path_tests_in + 'crosstabular_class_random_categ_all.csv')
            case 'columns':
                expected = pd.read_csv(filepath_or_buffer=path_tests_in + 'crosstabular_class_random_categ_columns.csv')
            case 'index':
                expected = pd.read_csv(filepath_or_buffer=path_tests_in + 'crosstabular_class_random_categ_index.csv')
    assert_frame_equal(crosstab, expected, check_exact=False, atol=1e-6, rtol=1e-6)
    assert os.path.exists(path_file)
    if os.path.exists(path_file):
        os.remove(path_file)


@pytest.mark.parametrize("rel, base_categ, path_save", [
    (False, None, path_tests_out),
    (True, None, path_tests_out),
    (True, class_categs[1], path_tests_out),
    (False, None, None),
    (True, None, None),
    (True, class_categs[1], None)
])
def test_continuous_categorical_stats(rel: bool, base_categ: str, path_save: str):
    path_file = path_tests_out + 'txId_class_stats.csv'
    if os.path.exists(path_file):
        os.remove(path_file)
    if path_save is None:
        assert isinstance(
            continuous_categorical_stats(db=db, continuous_var='txId', categorical_var='class', relative=rel,
                                         base_categorical_var=base_categ, path_save=path_save), pd.DataFrame)
    else:
        continuous_categorical_stats(db=db, continuous_var='txId', categorical_var='class', relative=rel,
                                     base_categorical_var=base_categ, path_save=path_save)
        assert os.path.exists(path_file)
        assert isinstance(
            continuous_categorical_stats(db=db, continuous_var='txId', categorical_var='class', relative=rel,
                                         base_categorical_var=base_categ, path_save=path_save), pd.DataFrame)
    if os.path.exists(path_file):
        os.remove(path_file)


def test_continuous_continuous_scatter():
    path_file = path_tests_out + 'ftre_10_ftre_11_scatter.png'
    if os.path.exists(path_file):
        os.remove(path_file)
    continuous_continuous_scatter(db=db_cont, x_var='ftre_10', y_var='ftre_11', path_save=path_tests_out)
    assert os.path.exists(path_file)
    if os.path.exists(path_file):
        os.remove(path_file)


def test_continuous_continuous_heatmap():
    path_file = path_tests_out + 'ftre_4_--_ftre_18_heatmap.png'
    if os.path.exists(path_file):
        os.remove(path_file)
    continuous_continuous_heatmap(db=db_cont, var_list=list(db_cont.columns)[5:20], path_save=path_tests_out)
    assert os.path.exists(path_file)
    if os.path.exists(path_file):
        os.remove(path_file)
