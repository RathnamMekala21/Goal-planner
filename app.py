import streamlit as st
import asyncio
from main import run_pipeline

st.set_page_config(page_title="Hackathon AI", layout="wide")

st.title("🚀 Hackathon Automation Dashboard")

goal = st.text_input("Enter your goal", placeholder="e.g Build a crypto trading bot")

if st.button("Run AI"):
    if not goal:
        st.warning("Please enter a goal")
    else:
        with st.spinner("🤖 Running AI agents..."):
            result = asyncio.run(run_pipeline(goal))

        st.success("✅ Done!")

        # -------- UI SECTIONS --------
        st.subheader("🔍 Analysis")
        st.code(result["analysis"])

        st.subheader("🌐 Research")
        st.code(result["research"])

        st.subheader("🛠 Plan")
        st.code(result["plan"])

        st.subheader("✅ Validation")
        st.code(result["validation"])
