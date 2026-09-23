from dataclasses import dataclass, field
import pandas as pd

@dataclass
class ExtraResult:
    tables: dict = field(default_factory=dict)
    summary: dict = field(default_factory=dict)
    features: dict = field(default_factory=dict)
    documents: dict = field(default_factory=dict)

@dataclass
class Context:
    graph: object
    nodes: pd.DataFrame
    transactions: pd.DataFrame
    config: dict
    results: dict = field(default_factory=dict)

    @property
    def cfg(self): return self.config['extras']

    def table(self, module, name):
        r=self.results.get(module)
        return r.tables.get(name, pd.DataFrame()) if r else pd.DataFrame()
