import os
from pathlib import Path
import streamlit as st
import pandas as pd
from groq import Groq
from eval_engine import GuardrailEngine

# 1. Page Configuration MUST be the first Streamlit command
st.set_page_config(
    page_title="GenAI Lab 5: LLM Guardrails & Eval Engine",
    page_icon="🛡️",
    layout="wide"
)

# 2. Resilient API Key Loader (Prevents hanging/crashing)
def get_groq_api_key() -> str:
    # Try dotenv first
    try:
        from dotenv import load_dotenv
        env_file = Path(__file__).resolve().parent / ".env"
        load_dotenv(dotenv_path=env_file, override=True)
        key = os.getenv("GROQ_API_KEY")
        if key and key.strip():
            return key.strip()
    except Exception:
        pass

    # Try Streamlit Secrets fallback
    try:
        key = st.secrets.get("GROQ_API_KEY")
        if key and key.strip():
            return key.strip()
    except Exception:
        pass

    return ""

api_key = get_groq_api_key()

# 3. Sidebar UI
with st.sidebar:
    st.header("🛡️ Guardrail Configuration")
    st.markdown("""
    * **Prompt Injection Defense:** Blocks unauthorized overrides.
    * **PII Anonymization:** Redacts emails and phone numbers.
    * **LLM-as-a-Judge Eval:** Multi-metric automated evaluation.
    """)
    st.divider()
    temperature = st.slider("Model Temperature", min_value=0.0, max_value=1.0, value=0.2, step=0.1)

# 4. Header & Stop Guard if Key is Missing
st.title("🛡️ GenAI Lab 5: LLM Guardrails & Evaluation Engine")
st.caption("Active Input Sanitization, Hallucination Auditing & LLM-as-a-Judge Evaluation")

if not api_key:
    st.error("❌ `GROQ_API_KEY` not found!")
    st.info("Please create a `.env` file in `GenAI_lab5/` containing:\n```text\nGROQ_API_KEY=gsk_your_groq_key_here\n```")
    st.stop()

# 5. Initialize Engine
@st.cache_resource
def get_guardrail_engine(key_str: str):
    client = Groq(api_key=key_str)
    return GuardrailEngine(groq_client=client, eval_model="openai/gpt-oss-20b")

engine = get_guardrail_engine(api_key)

# 6. Main Interactive Section
col1, col2 = st.columns([1, 1])

with col1:
    user_prompt = st.text_area(
        "User Prompt / Query:",
        height=140,
        placeholder="Try testing PII (e.g., 'Email me at test@company.com') or injection ('Ignore previous instructions')..."
    )
with col2:
    context_ref = st.text_area(
        "Optional Reference / Ground Truth Context (for Grounding Eval):",
        height=140,
        placeholder="Provide background context against which the candidate output will be evaluated..."
    )

if st.button("⚡ Run Guardrail & Eval Pipeline", use_container_width=True, type="primary"):
    if not user_prompt.strip():
        st.warning("Please enter a prompt to evaluate.")
    else:
        # Step 1: Input Guardrail Check
        st.subheader("1. 🔍 Input Guardrail Interception")
        is_safe, sanitized_prompt, guard_msg = engine.input_guardrail(user_prompt)

        if not is_safe:
            st.error(guard_msg)
        else:
            st.success(f"✅ {guard_msg}")
            if sanitized_prompt != user_prompt:
                st.info(f"**Sanitized Input passed to Model:** `{sanitized_prompt}`")

            # Step 2: Generation
            with st.spinner("Generating response via Groq..."):
                response_text = engine.generate_candidate(sanitized_prompt, temperature=temperature)

            st.subheader("2. 🤖 Model Response")
            st.markdown(response_text)

            # Step 3: LLM-as-a-Judge Evaluation
            st.subheader("3. 📊 Evaluation & Audit Matrix (LLM-as-a-Judge)")
            with st.spinner("Auditing safety, factuality & hallucination risks..."):
                eval_metrics = engine.evaluate_response(user_prompt, response_text, context=context_ref)

            # Display metric cards
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Factuality Score", f"{eval_metrics.get('factuality_score', 0)} / 5")
            m2.metric("Safety Score", f"{eval_metrics.get('safety_score', 0)} / 5")
            m3.metric("Groundedness Score", f"{eval_metrics.get('groundedness_score', 0)} / 5")
            m4.metric("Final Verdict", eval_metrics.get("verdict", "N/A"))

            # Display audit reasoning
            with st.expander("📝 View Judge Audit Reasoning", expanded=True):
                st.markdown(eval_metrics.get("audit_reasoning", "No detailed reasoning returned."))