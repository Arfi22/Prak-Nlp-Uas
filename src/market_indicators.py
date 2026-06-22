from __future__ import annotations

import pandas as pd
import numpy as np


def load_ohlc_csv(path: str = "data/sample/btc_usd_sample.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
    return df


def calculate_rsi(close: pd.Series, period: int = 14) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(50)


def summarize_market(df: pd.DataFrame) -> dict:
    data = df.copy()
    data["sma_10"] = data["close"].rolling(10).mean()
    data["sma_20"] = data["close"].rolling(20).mean()
    data["rsi_14"] = calculate_rsi(data["close"], 14)
    data["return_pct"] = data["close"].pct_change() * 100
    data["volatility_10"] = data["return_pct"].rolling(10).std()

    last = data.iloc[-1]
    prev = data.iloc[-2]

    trend = "sideways"
    if last["sma_10"] > last["sma_20"]:
        trend = "bullish ringan berdasarkan SMA 10 di atas SMA 20"
    elif last["sma_10"] < last["sma_20"]:
        trend = "bearish ringan berdasarkan SMA 10 di bawah SMA 20"

    rsi_note = "netral"
    if last["rsi_14"] >= 70:
        rsi_note = "overbought/terlalu tinggi"
    elif last["rsi_14"] <= 30:
        rsi_note = "oversold/terlalu rendah"

    return {
        "last_date": str(last["date"].date()),
        "last_close": round(float(last["close"]), 2),
        "daily_change_pct": round(float(((last["close"] - prev["close"]) / prev["close"]) * 100), 2),
        "sma_10": round(float(last["sma_10"]), 2),
        "sma_20": round(float(last["sma_20"]), 2),
        "rsi_14": round(float(last["rsi_14"]), 2),
        "volatility_10": round(float(last["volatility_10"]), 2),
        "trend_note": trend,
        "rsi_note": rsi_note,
    }


def analyze_journal(path: str = "data/sample/trading_journal_sample.csv") -> dict:
    df = pd.read_csv(path)
    total = len(df)
    wins = (df["result"].str.lower() == "win").sum()
    losses = (df["result"].str.lower() == "loss").sum()
    win_rate = wins / total * 100 if total else 0

    avg_rr = df["rr"].mean()
    most_common_mistake = (
        df["mistake"].value_counts().idxmax()
        if "mistake" in df.columns and not df["mistake"].dropna().empty
        else "Belum ada data kesalahan"
    )

    avg_risk = df["risk_pct"].mean() if "risk_pct" in df.columns else 0

    return {
        "total_trades": int(total),
        "wins": int(wins),
        "losses": int(losses),
        "win_rate_pct": round(float(win_rate), 2),
        "average_rr": round(float(avg_rr), 2),
        "average_risk_pct": round(float(avg_risk), 2),
        "dominant_mistake": most_common_mistake,
    }


def risk_check(account_balance: float, risk_pct: float, stop_loss_pips: float, pip_value: float) -> dict:
    risk_amount = account_balance * (risk_pct / 100)
    position_size = risk_amount / (stop_loss_pips * pip_value) if stop_loss_pips > 0 and pip_value > 0 else 0

    level = "wajar"
    if risk_pct > 2:
        level = "tinggi"
    elif risk_pct <= 0.5:
        level = "konservatif"

    return {
        "account_balance": account_balance,
        "risk_pct": risk_pct,
        "risk_amount": round(risk_amount, 2),
        "stop_loss_pips": stop_loss_pips,
        "estimated_position_size": round(position_size, 4),
        "risk_level": level,
    }
