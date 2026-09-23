from dataclasses import dataclass
import pandas as pd

ROLES = ('consolidator', 'distributor', 'transit', 'terminal', 'coordinator', 'peripheral')


class DataValidationError(ValueError):
    def __init__(self, message, details=None):
        super().__init__(message)
        self.details = details or {}


@dataclass
class AnalysisResult:
    nodes: pd.DataFrame
    edges: pd.DataFrame
    clusters: pd.DataFrame
    top: pd.DataFrame
    run_meta: dict
    quality: dict
