# analytics/insights.py
import pandas as pd


def generate_insights(df: pd.DataFrame, sov_global: pd.DataFrame, sov_kw: pd.DataFrame) -> str:
    if df.empty or sov_global.empty:
        return "Not enough brand mentions yet to generate insights. Try increasing TOP_N or adding more keywords."

    lines = []

    # Global leaders
    top_vol = sov_global.sort_values("sov_volume", ascending=False).head(1)
    top_pos = sov_global.sort_values("sov_positive", ascending=False).head(1)

    if not top_vol.empty:
        b = top_vol.iloc[0]
        lines.append(
            f"- **Volume leader:** `{b['brand']}` with ~{b['sov_volume']*100:.1f}% of total mentions across all keywords."
        )
    if not top_pos.empty:
        b = top_pos.iloc[0]
        lines.append(
            f"- **Positive voice leader:** `{b['brand']}` with ~{b['sov_positive']*100:.1f}% of positive sentiment share."
        )

    # Sentiment overview
    brand_sent = df[df["brand"].notna()].groupby("brand")["sentiment"].mean().reset_index()
    brand_sent["sentiment_label"] = brand_sent["sentiment"].apply(
        lambda s: "positive" if s > 0.2 else ("negative" if s < -0.2 else "mixed")
    )
    lines.append("\n**Brand sentiment overview:**")
    for _, row in brand_sent.iterrows():
        lines.append(f"- `{row['brand']}` → avg sentiment **{row['sentiment']:.2f}** ({row['sentiment_label']}).")

    # Atomberg keyword strengths
    if not sov_kw.empty and "Atomberg" in sov_kw["brand"].unique():
        atom_kw = sov_kw[sov_kw["brand"] == "Atomberg"]
        best = atom_kw.sort_values("sov_positive", ascending=False).head(1)
        worst = atom_kw.sort_values("sov_positive", ascending=True).head(1)

        if not best.empty:
            b = best.iloc[0]
            lines.append(
                f"\n- Atomberg is strongest for **\"{b['keyword']}\"**, "
                f"with ~{b['sov_positive']*100:.1f}% share of positive voice."
            )
        if not worst.empty:
            w = worst.iloc[0]
            lines.append(
                f"- Atomberg is relatively weaker for **\"{w['keyword']}\"**, "
                f"with only ~{w['sov_positive']*100:.1f}% positive voice share."
            )

    # Recommendations
    lines.append("\n**Actionable recommendations:**")
    lines.append("- Double down on keywords where Atomberg already has strong positive share (SEO blogs, landing pages, FAQs).")
    lines.append("- For weaker keywords, create comparison and explainer content addressing common pain points visible in search snippets.")
    lines.append("- Track SOV over time (weekly) to see if campaigns actually shift visibility and positive voice.")

    return "\n".join(lines)
