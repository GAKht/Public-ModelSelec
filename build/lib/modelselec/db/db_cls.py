"""
                        This script includes classes which handle historical databases

                                            Guillaume A. Khayat
                                           guill.khayat@gmail.com
                                                2023-12-15
"""
import attr
from typing import Tuple, Union
from modelselec.modules_paths import *
from modelselec.util.util_db import check_file_exists


@attr.define(slots=True)
class DBhist:
    """
    This class stores historical databases and provides attributes and methods to be applied to them
    """

    path_db: str = attr.field(validator=attr.validators.instance_of(str))
    file_name: str = attr.field(validator=attr.validators.and_(attr.validators.instance_of(str),
                                                               check_file_exists))
    file_type: str = attr.field(default='parquet', validator=attr.validators.instance_of(str))
    desc_continuous: Union[pd.DataFrame, None] = attr.field(default=None)
    desc_categorical: Union[pd.DataFrame, None] = attr.field(default=None)
    dtype: dict = attr.field(default=None, validator=attr.validators.optional(attr.validators.instance_of(dict)))
    parse_dates: list = attr.field(default=None, validator=attr.validators.optional(attr.validators.instance_of(list)))
    header: int = attr.field(default=0, validator=attr.validators.instance_of(int))

    db: pd.DataFrame = attr.field(init=False)

    def __attrs_post_init__(self):
        """
        Read the historical data file into a pandas DataFrame after the instance is created
        """
        match self.file_type:
            case 'parquet':
                self.db = pd.read_parquet(path=f'{self.path_db}{self.file_name}.parquet')
            case 'csv':
                self.db = pd.read_csv(filepath_or_buffer=f'{self.path_db}{self.file_name}.csv', dtype=self.dtype,
                                      header=self.header, parse_dates=self.parse_dates)


        desc_continuous, desc_categorical = self.get_desc()
        self.desc_continuous = desc_continuous
        self.desc_categorical = desc_categorical


    def get_desc(self, db: pd.DataFrame = None) -> Tuple[Union[pd.DataFrame, None], Union[pd.DataFrame, None]]:
        """
        A method to provide the description of the pandas dataframe
        :param db: pd.DataFrame, optional. If not provided, the object's attribute db will be used
        :return: the description of the continuous variables in the dataframe
                    and the categorical variables in the dataframe
        """

        if db is None:
            db = self.db

        continuous_cols = db.select_dtypes(include=np.number).columns
        categorical_cols = db.select_dtypes(exclude=np.number).columns

        if len(continuous_cols) > 0:
            desc_continuous = db.select_dtypes(include=np.number).describe()
        else:
            desc_continuous = None

        if len(categorical_cols) > 0:
            desc_categorical = db.select_dtypes(exclude=np.number).describe()
        else:
            desc_categorical = None

        return desc_continuous, desc_categorical

    def get_na_percent(self, db: pd.DataFrame = None) -> pd.Series:
        """
        A method to provide the percentage of NAs in each column of the dataframe
        :param db: pd.DataFrame, optional. If not provided, the object's attribute db will be used
        :return: A pandas series with the percentage of observations of NAs in each column,
                    the index of the series are the column names of the dataframe
        """

        if db is None:
            db = self.db

        prct_nas = db.isna().mean() * 100
        prct_nas.name = '% of NA obs.'
        return prct_nas

    def update_db(self, db_new: pd.DataFrame) -> None:
        """
        This method updates the object's attributes in case we would like to change the historical database
        :param db_new: pd.DataFrame, the new dataframe of the object
        :return: None
        """

        desc_continuous, desc_categorical = self.get_desc(db=db_new)

        self.db = db_new
        self.desc_continuous = desc_continuous
        self.desc_categorical = desc_categorical