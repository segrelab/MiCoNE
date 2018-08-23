"""
    Module that provides custom encoding for the JSON network object
"""

import json
import numpy as np


class JsonEncoder(json.JSONEncoder):
    """
        Class that extends the default `JSONEncoder` class
        Converts `numpy` datatypes to native Python datatypes
    """

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, set):
            return list(obj)
        return super().default(obj)
