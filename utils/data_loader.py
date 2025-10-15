"""Data‑loading helpers.

Creates synthetic CSVs if they do not exist and reads them into
pandas DataFrames.
"""
import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path(__file__).parents[1] / "data/main_data"

CLASS_COLS = ["class 1", "class 2"]
CMP_COLS = ["CMP1", "CMP2"]
ALL_CLASSES = ["AGN", "STAR", "YSO", "HMXB", "LMXB", "ULX", "PULSAR", "CV"]


# def _make_mock_classification() -> pd.DataFrame:
#     rng = np.random.default_rng(42)
#     n = 500
#     names = [f"Src{i:04d}" for i in range(n)]
#     ra = rng.uniform(0, 360, n)
#     dec = rng.uniform(-90, 90, n)

#     class1 = rng.choice(ALL_CLASSES, n)
#     class2 = rng.choice(ALL_CLASSES, n)

#     cmp1 = rng.uniform(0, 1, n)
#     cmp2 = rng.uniform(0, 1, n)

#     df = pd.DataFrame({
#         "name": names,
#         "ra": ra,
#         "dec": dec,
#         "class 1": class1,
#         "CMP1": cmp1,
#         "class 2": class2,
#         "CMP2": cmp2,
#     }).set_index("name")
#     df = df.sort_values(by = ['class 1', 'CMP1'])
#     return df


# def _make_mock_feature_contributions() -> pd.DataFrame:
#     rng = np.random.default_rng(123)
#     n = 500
#     names = [f"Src{i:04d}" for i in range(n)]
#     features = [f"feat_{i}" for i in range(10)]
#     data = rng.normal(0, 1, size=(n, len(features)))
#     df = pd.DataFrame(data, index=names, columns=features)
#     return df


# def load_classification() -> pd.DataFrame:
#     path = DATA_DIR / "paper-2-data-table-with-shap.pq"
#     if not path.exists():
#         df = _make_mock_classification()
#         df.to_parquet(path)
#     else:
#         df = pd.read_parquet(path)
#         df = df.sample(frac = 1)
#         df['SHAP'] = ['✓' if si else '' for si in df['SHAP']]
#     return df


# def load_feature_contributions() -> pd.DataFrame:
#     path = DATA_DIR / "shap-df-conf.pq"
#     if not path.exists():
#         df = _make_mock_feature_contributions()
#         df.to_parquet(path)
#     else:
#         df = pd.read_parquet(path)
#         # df = df.sample(frac = 1)
#     return df




def load_classification() -> pd.DataFrame:
    path = DATA_DIR / "paper-2-data-table-with-shap.gz"
    df = pd.read_parquet(path)
    df = df.sample(frac = 1)
    df['SHAP'] = ['✓' if si else '' for si in df['SHAP']]
    return df


def load_feature_contributions() -> pd.DataFrame:
    path = DATA_DIR / "All-paper-2-shap.gz"
    df = pd.read_parquet(path)
    # df = df.sample(frac = 1)
    return df


def load_feature_value() -> pd.DataFrame:
    path = DATA_DIR / "All-paper2-feat.gz"
    df = pd.read_parquet(path)
    # df = df.sample(frac = 1)
    return df