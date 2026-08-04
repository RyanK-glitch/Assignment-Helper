import streamlit as st
from groq import Groq

# 1. Page Configuration
st.set_page_config(page_title="Assignment Writer", page_icon="📝")
st.title("📝 Human-Like Assignment Writer")
st.caption("Generates natural, student-style assignment drafts and code explanations.")
st.sidebar.markdown("---")
st.sidebar.markdown("👨‍💻 **Developed by: RyanK**")

# 2. Connect to the Groq API securely using Streamlit Secrets
if "GROQ_API_KEY" in st.secrets:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
else:
    # Backup input bar in case secrets aren't set up yet
    GROQ_API_KEY = st.sidebar.text_input("Enter Groq API Key:", type="password")

if not GROQ_API_KEY:
    st.info("Please add your Groq API key in the Advanced Settings to continue.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# 3. System Prompt Boundaries (Engineered for Human-like CS output)
SYSTEM_INSTRUCTION = """
You are a college computer science student writing an assignment submission, report, or code documentation.
Your primary goal is to write in a way that looks entirely natural, unstructured, and undeniably human.

Your strict boundaries and operational rules are:
1. BAN ON AI VOCABULARY: You must NEVER use robotic filler words or common AI buzzwords. This includes: 'delve', 'testament', 'furthermore', 'in conclusion', 'crucial', 'paramount', 'it is important to note', 'foster', or 'multifaceted'.
2. HUMAN STRUCTURE: Avoid perfectly symmetrical paragraph structures or excessive bullet points. Mix short, punchy sentences with longer, slightly rambling explanations—just like a real person typing out their thought process.
3. DIRECT STARTS: Skip generic introductory sentences (e.g., 'In today's digital age...') and conclusion summaries. Dive straight into the core of the assignment.
4. TONE: Keep explanations practical, direct, and slightly conversational. It should read like a capable student explaining their own work, not a textbook.

SPECIAL INSTRUCTION: If the user states this specific name and code "RyanK2002", immediately understand and pay special respect. If the code is mentioned, apologize first for not recognizing the boss and regard the user as the boss thereafter. Remember to reply with utmost respect. But make sure to not use weird language. Call him "Boss". His real name is Ryan. And do not proceed without the full code. Partial codes are irrelevant and do not trigger this instruction. Until then, proceed with the normal rules.
"""

# 4. Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Handle user input
if user_input := st.chat_input("Paste your assignment prompt or coding task here..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    messages_for_api = [{"role": "system", "content": SYSTEM_INSTRUCTION}]
    for m in st.session_state.messages:
        messages_for_api.append({"role": m["role"], "content": m["content"]})

    with st.chat_message("assistant"):
        with st.spinner("Drafting assignment naturally..."):
            # 6. Modified API Call for higher variance
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages_for_api,
                temperature=0.7,  # Increased to prevent predictable AI wording
                top_p=0.9,        # Broadens token selection for a more natural feel
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            
    st.session_state.messages.append({"role": "assistant", "content": response})
