"""
                            This script is necessary to ensure that all submodules are imported
                                        when model_selec is imported

                                            Guillaume A. Khayat
                                           guill.khayat@gmail.com
                                                2024-03-12
"""

__all__ = ['util_db', 'util_perf']

# Import the specified submodules
from . import util_db, util_perf
