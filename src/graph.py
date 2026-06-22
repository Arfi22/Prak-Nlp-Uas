from __future__ import annotations

from typing import TypedDict, Literal

from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langsmith import traceable

from .llm import get_llm
from .market_indicators import load_ohlc_csv, summarize_market, analyze_journal, risk_check
from .rag import retrieve_context
from .prompts import SYSTEM_PROMPT, FINAL_ANSWER_TEMPLATE


class FinMentorState(TypedDict, total=False):
    question: str
    intent: str
    learning_context: str
    market_summary: dict
    journal_summary: dict
    risk_summary: dict
    answer: str


@traceable(name="classify_intent")
def classify_intent(state: FinMentorState) -> FinMentorState:
    question = state.get("question", "").lower()

    if any(word in question for word in ["rsi", "sma", "ohlc", "harga", "market", "btc", "crypto", "forex"]):
        intent = "market_analysis"
    elif any(word in question for word in ["jurnal", "journal", "winrate", "rr", "kesalahan", "evaluasi trade"]):
        intent = "journal_analysis"
    elif any(word in question for word in ["risk", "risiko", "stop loss", "lot", "modal", "position size"]):
        intent = "risk_management"
    else:
        intent = "learning_assistant"

    return {"intent": intent}


@traceable(name="retrieve_learning_context")
def retrieve_learning_context_node(state: FinMentorState) -> FinMentorState:
    question = state.get("question", "")
    return {"learning_context": retrieve_context(question)}


@traceable(name="analyze_market")
def analyze_market_node(state: FinMentorState) -> FinMentorState:
    df = load_ohlc_csv()
    return {"market_summary": summarize_market(df)}


@traceable(name="analyze_journal")
def analyze_journal_node(state: FinMentorState) -> FinMentorState:
    return {"journal_summary": analyze_journal()}


@traceable(name="risk_management_check")
def risk_management_node(state: FinMentorState) -> FinMentorState:
    # Nilai contoh untuk demo. Pada pengembangan berikutnya, nilai ini dapat diambil dari form UI.
    summary = risk_check(
        account_balance=1000,
        risk_pct=1.0,
        stop_loss_pips=50,
        pip_value=1.0,
    )
    return {"risk_summary": summary}


@traceable(name="generate_final_answer")
def generate_final_answer_node(state: FinMentorState) -> FinMentorState:
    llm = get_llm(temperature=0.2)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", FINAL_ANSWER_TEMPLATE),
        ]
    )

    chain = prompt | llm
    response = chain.invoke(
        {
            "question": state.get("question", ""),
            "intent": state.get("intent", ""),
            "learning_context": state.get("learning_context", "Tidak digunakan pada alur ini."),
            "market_summary": state.get("market_summary", "Tidak digunakan pada alur ini."),
            "journal_summary": state.get("journal_summary", "Tidak digunakan pada alur ini."),
            "risk_summary": state.get("risk_summary", "Tidak digunakan pada alur ini."),
        }
    )
    return {"answer": response.content}


def route_by_intent(state: FinMentorState) -> Literal["learning", "market", "journal", "risk"]:
    intent = state.get("intent", "learning_assistant")
    if intent == "market_analysis":
        return "market"
    if intent == "journal_analysis":
        return "journal"
    if intent == "risk_management":
        return "risk"
    return "learning"


def build_graph():
    builder = StateGraph(FinMentorState)

    builder.add_node("classify_intent", classify_intent)
    builder.add_node("retrieve_learning_context", retrieve_learning_context_node)
    builder.add_node("analyze_market", analyze_market_node)
    builder.add_node("analyze_journal", analyze_journal_node)
    builder.add_node("risk_management", risk_management_node)
    builder.add_node("generate_final_answer", generate_final_answer_node)

    builder.add_edge(START, "classify_intent")
    builder.add_conditional_edges(
        "classify_intent",
        route_by_intent,
        {
            "learning": "retrieve_learning_context",
            "market": "analyze_market",
            "journal": "analyze_journal",
            "risk": "risk_management",
        },
    )

    builder.add_edge("retrieve_learning_context", "generate_final_answer")
    builder.add_edge("analyze_market", "generate_final_answer")
    builder.add_edge("analyze_journal", "generate_final_answer")
    builder.add_edge("risk_management", "generate_final_answer")
    builder.add_edge("generate_final_answer", END)

    checkpointer = InMemorySaver()
    return builder.compile(checkpointer=checkpointer)
