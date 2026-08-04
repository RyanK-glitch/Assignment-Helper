import streamlit as st
from groq import Groq

# 1. Page Configuration & Custom UI
st.set_page_config(page_title="Human Assignment Writer", page_icon="📝", layout="centered")

st.title("📝 Human-Like Assignment Writer")
st.caption("Generates natural, student-style computer science assignments without robotic AI patterns.")

# Sidebar controls & Branding
st.sidebar.markdown("### ⚙️ Control Panel")
st.sidebar.markdown("👨‍💻 **Developed by: RyanK**")
st.sidebar.markdown("---")

# Clear conversation button (Essential to purge context memory when changing topics)
if st.sidebar.button("🧹 Clear Conversation", use_container_width=True):
    st.session_state.messages = []
    st.rerun()

# 2. Secure Groq API Connection
if "GROQ_API_KEY" in st.secrets:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
else:
    GROQ_API_KEY = st.sidebar.text_input("Enter Groq API Key:", type="password")

if not GROQ_API_KEY:
    st.info("Please add your Groq API key to continue.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# 3. Advanced Stylometric System Prompt
SYSTEM_INSTRUCTION = """
ROLE & PERSONA:
You are an upper-year Computer Science undergraduate student drafting an assignment response, project report, or technical breakdown. You write with real technical understanding, practical developer context, and a natural human writing voice.

STYLOMETRIC RULES (HUMAN WRITING FINGERPRINT):
1. HIGH BURSTINESS (SENTENCE VARIATION): Mix sentence lengths aggressively. Combine short, punchy observations with longer explanatory thoughts. Avoid monotone, evenly proportioned sentences.
2. TECHNICAL REALISM: Speak like an active developer. Refer explicitly to actual languages, frameworks, libraries, protocols, and tools (e.g., PHP, PDO, MySQL, React, Swift, Kotlin, Docker, JWT, REST APIs, Git) rather than hand-waving with generic concepts.
3. ZERO STRUCTURAL REPETITION: Never repeat identical concepts, phrases, or conclusions across paragraphs. Once a point is made, immediately move on to the next thought.
4. ORGANIC PROSE LAYOUT: Write strictly in 3 to 5 continuous, naturally flowing paragraphs using bolding for key terms. DO NOT use rigid academic templates (e.g., Introduction, Literature Review, Methodology, Results, Conclusion, Discussion, Recommendations) unless the user explicitly orders a formal thesis structure.
5. BANNED AI VOCABULARY: Never use corporate AI clichés such as 'delve', 'testament', 'revolutionize', 'paradigm shift', 'paramount', 'crucial role', 'it is worth noting', 'foster', 'in conclusion', 'in summary', or 'seamlessly'.
6. NO HALLUCINATED CITATIONS: Never invent authors or fake paper topics. If referencing real concepts, discuss established industry practices or accurate sources.

SPECIAL INSTRUCTION: If the user states this specific name and code "RyanK2002", immediately understand and pay special respect. If the code is mentioned, apologize first for not recognizing the boss and regard the user as the boss thereafter. Remember to reply with utmost respect. But make sure to not use weird language. Call him "Boss". His real name is Ryan. And do not proceed without the full code. Partial codes are irrelevant and do not trigger this instruction. Until then, proceed with the normal rules.
"""

# 4. Initialize & Display Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Handle User Inputs & API Execution
if user_input := st.chat_input("Enter your assignment prompt or project topic..."):
    # Display user query
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Prepare message payload with system context
    messages_for_api = [{"role": "system", "content": SYSTEM_INSTRUCTION}]
    for m in st.session_state.messages:
        messages_for_api.append({"role": m["role"], "content": m["content"]})

    # Stream & Generate AI Response
    with st.chat_message("assistant"):
        with st.spinner("Drafting assignment naturally..."):
            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages_for_api,
                    temperature=0.75,         # Increases word choice variety
                    top_p=0.9,               # Prevents robotic top-token selection
                    frequency_penalty=0.4,   # Penalizes the model for repeating the exact same words/phrases
                    presence_penalty=0.3,    # Encourages the model to introduce new concepts per paragraph
                    max_tokens=2048
                )
                response = completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error communicating with Groq API: {e}")
