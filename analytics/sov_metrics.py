# analytics/sov_metrics.py
import numpy as np
import pandas as pd


def _prep(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["rank_score"] = df["rank"].apply(
        lambda r: 1 / np.log(r + 1.5) if pd.notna(r) and r and r > 0 else 0
    )
    df["positive_score"] = df["sentiment"].clip(lower=0)
    return df


def compute_sov(df: pd.DataFrame) -> pd.DataFrame:
    df = df[df["brand"].notna()].copy()
    if df.empty:
        return pd.DataFrame(columns=[
            "brand", "volume", "visibility_score",
            "positive_voice", "sov_volume", "sov_visibility", "sov_positive"
        ])

    df = _prep(df)

    vol = df.groupby("brand")["text"].count().rename("volume")
    vis = df.groupby("brand")["rank_score"].sum().rename("visibility_score")
    pos = df.groupby("brand")["positive_score"].sum().rename("positive_voice")

    res = pd.concat([vol, vis, pos], axis=1).fillna(0)

    res["sov_volume"] = res["volume"] / res["volume"].sum() if res["volume"].sum() else 0
    res["sov_visibility"] = res["visibility_score"] / res["visibility_score"].sum() if res["visibility_score"].sum() else 0
    res["sov_positive"] = res["positive_voice"] / res["positive_voice"].sum() if res["positive_voice"].sum() else 0

    return res.reset_index()


def compute_sov_by_keyword(df: pd.DataFrame) -> pd.DataFrame:
    df = df[df["brand"].notna()].copy()
    if df.empty:
        return pd.DataFrame()

    df = _prep(df)

    grouped = df.groupby(["keyword", "brand"]).agg(
        volume=("text", "count"),
        visibility_score=("rank_score", "sum"),
        positive_voice=("positive_score", "sum"),
    ).reset_index()

    def normalize(group: pd.DataFrame) -> pd.DataFrame:
        group = group.copy()
        group["sov_volume"] = group["volume"] / group["volume"].sum() if group["volume"].sum() else 0
        group["sov_visibility"] = group["visibility_score"] / group["visibility_score"].sum() if group["visibility_score"].sum() else 0
        group["sov_positive"] = group["positive_voice"] / group["positive_voice"].sum() if group["positive_voice"].sum() else 0
        return group

    return grouped.groupby("keyword", group_keys=False).apply(normalize)
