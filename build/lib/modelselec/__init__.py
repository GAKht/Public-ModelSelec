"""
                            This script is necessary to ensure that all submodules are imported
                                        when model_selec is imported

                                            Guillaume A. Khayat
                                           guill.khayat@gmail.com
                                                2024-03-12
"""

__all__ = ['db', 'eda', 'util']

# Import the specified submodules
from . import db
from . import eda
from . import util