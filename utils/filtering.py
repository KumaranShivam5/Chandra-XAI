"""Filtering utilities for the classification dataframe.

Implements the logic described in the specification:
* CMP threshold
* Positional cross‑match using Astropy (great‑circle distance)
* Class selection
"""
import pandas as pd
import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u


def apply_filters(
    df: pd.DataFrame,
    cmp_thresh: float,
    ra: float or None,
    dec: float or None,
    radius: float,
    classes: list[str],
    with_shap: bool,
) -> pd.DataFrame:
    # CMP filter
    mask = df["CMP1"] > cmp_thresh

    # Class filter
    mask &= df["class 1"].isin(classes)
    if(with_shap) : mask &= df['SHAP']

    # Positional filter (if radius > 0)
    if ra is not None and dec is not None and radius > 0:
        source_coord = SkyCoord(ra=ra * u.deg, dec=dec * u.deg)
        target_coord = SkyCoord(ra=df["ra"].values * u.deg,
                                dec=df["dec"].values * u.deg)
        sep = source_coord.separation(target_coord).arcminute
        mask &= sep <= radius

    return df[mask]