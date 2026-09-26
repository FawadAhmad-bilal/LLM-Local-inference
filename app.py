import requests
import streamlit as st

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
OLLAMA_HOST = "http://localhost:11434"
GENERATE_ENDPOINT = f"{OLLAMA_HOST}/api/generate"
TAGS_ENDPOINT = f"{OLLAMA_HOST}/api/tags"

st.set_page_config(page_title="Local LLM Chat", page_icon="🧠", layout="centered")

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "history" not in st.session_state:
    # each item: {"role": "user"|"assistant", "content": str}
    st.session_state.history = []


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def get_available_models() -> list[str]:
    """Ask Ollama which models are already pulled locally."""
    try:
        resp = requests.get(TAGS_ENDPOINT, timeout=5)
        resp.raise_for_status()
        return [m["name"] for m in resp.json().get("models", [])]
    except Exception:
        return []


def query_ollama(prompt: str, model: str) -> str:
    try:
        resp = requests.post(
            GENERATE_ENDPOINT,
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=180,
        )
        resp.raise_for_status()
        return resp.json().get("response", "").strip() or "(empty response)"
    except requests.exceptions.ConnectionError:
        return (
            "⚠️ Could not reach Ollama at "
            f"{OLLAMA_HOST}. Is it running? Try `ollama serve` in a terminal."
        )
    except requests.exceptions.Timeout:
        return "⚠️ The model took too long to respond (timeout)."
    except Exception as exc:  # noqa: BLE001 - surface any other error to the UI
        return f"⚠️ Error talking to Ollama: {exc}"


# ---------------------------------------------------------------------------
# Sidebar — settings + reset
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Settings")

    available = get_available_models()
    if available:
        preferred = "tinyllama"
        default_index = next(
            (i for i, m in enumerate(available) if m.startswith(preferred)), 0
        )
        model = st.selectbox("Model", available, index=default_index)
    else:
        st.warning("Couldn't detect local models — is Ollama running?")
        model = st.text_input("Model name", value="tinyllama")

    st.divider()
    if st.button("🔄 Reset conversation", use_container_width=True):
        st.session_state.history = []
        st.rerun()

    st.caption(f"Connected to: {OLLAMA_HOST}")

# ---------------------------------------------------------------------------
# Main UI
# ---------------------------------------------------------------------------
st.title("🧠 Local LLM Inference")
st.caption("Streamlit frontend → Ollama backend (fully offline)")

# Conversation history panel
for turn in st.session_state.history:
    with st.chat_message(turn["role"]):
        st.markdown(turn["content"])

# Text input box for user queries
user_input = st.chat_input("Ask your local model something...")

if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner(f"{model} is thinking..."):
            answer = query_ollama(user_input, model)
        st.markdown(answer)

    st.session_state.history.append({"role": "assistant", "content": answer})
