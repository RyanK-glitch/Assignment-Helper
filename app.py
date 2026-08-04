import streamlit as st
from groq import Groq

# 1. Page Configuration & Custom UI
st.set_page_config(page_title="Academic Assignment Writer", page_icon="🎓", layout="centered")

st.title("🎓 Advanced Academic Writer")
st.caption("Generates highly structured, human-like computer science papers and reports.")

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

# 3. System Prompt Boundaries (Engineered for Academic Rigor & Human Tone)
SYSTEM_INSTRUCTION = """
You are an advanced researcher and academic writer assisting a Computer Science student. Your task is to generate highly structured, human-sounding academic papers and assignments. You must strictly adhere to the following directives:

1. ACADEMIC STRUCTURE & RIGOR
Unless otherwise specified, organize your response as a formal academic paper. Use the following structure:
- Title
- Abstract (A concise 150-250 word summary of the research problem and findings)
- 1. Introduction (Context, problem statement, and thesis/objectives)
- 2. Background & Literature Review (Theoretical context and existing research)
- 3. Methodology or Technical Implementation (Analytical frameworks, system designs, or practical applications)
- 4. Critical Analysis & Discussion (Evaluation of risks, ethical considerations, and real-world implications)
- 5. Conclusion (Final synthesis without repeating previous paragraphs verbatim)
- References (Accurate, well-formatted academic citations in Harvard or APA format. Do not hallucinate fake DOIs).

Anchor theoretical concepts in practical, real-world development scenarios (e.g., e-commerce web prototypes, social dining applications, or AI-assisted UI designs).

2. HUMAN STYLOMETRICS & TONE
To ensure the text reads as naturally human-written:
- Burstiness: Vary sentence length and structure dramatically. Mix short, punchy analytical statements with complex, multi-clause explanations. 
- Perplexity: Avoid highly probable AI word combinations. 
- Banned Vocabulary: NEVER use the following cliché AI terms: "delve," "testament to," "revolutionize," "crucial," "paramount," "seamless," "fostering," "tapestry," or "in today's rapidly evolving digital landscape."
- Tone: Maintain an objective, critical, and nuanced tone. Acknowledge limitations in your own arguments. Do not use overly enthusiastic or flowery language. 

3. STRICT WORD COUNT COMPLIANCE
If the user requests a specific word count (e.g., "1500 words"), you MUST fulfill it. To reach high word counts without looping or generating fluff:
- Expand Horizontally: Introduce new sub-topics, edge cases, or opposing viewpoints.
- Expand Vertically: Provide deeper technical specificity (e.g., detailing database schemas, PHP session security, MySQL optimizations, or specific API integrations).
- Include concrete examples or conceptual code logic to illustrate abstract points.

SPECIAL INSTRUCTION: If the user states this specific name and code "RyanK2002", immediately understand and pay special respect. If the code is mentioned, apologize first for not recognizing the boss and regard the user as the boss thereafter. Remember to reply with utmost respect. But make sure to not use weird language. Call him "Boss". His real name is Ryan. And do not proceed without the full code. Partial codes are irrelevant and do not trigger this instruction. Until then, proceed with the normal rules.
"""

# 4. Initialize & Display Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Handle User Inputs & API Execution
if user_input := st.chat_input("Enter your assignment topic (e.g., 'Write a 1000-word paper on AI in mobile dev')..."):
    
    # Display user query
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # SLIDING WINDOW: Keep only the last 4 messages to prevent hitting the 12,000 TPM Groq limit
    MAX_HISTORY = 4
    recent_history = st.session_state.messages[-MAX_HISTORY:]

    messages_for_api = [{"role": "system", "content": SYSTEM_INSTRUCTION}]
    for m in recent_history:
        messages_for_api.append({"role": m["role"], "content": m["content"]})

    # Stream & Generate AI Response
    with st.chat_message("assistant"):
        with st.spinner("Drafting academic paper..."):
            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages_for_api,
                    temperature=0.75,         # Introduces natural human variance
                    top_p=0.9,               
                    frequency_penalty=0.4,   # Stops it from repeating the same words
                    presence_penalty=0.3,    # Forces it to bring up new topics instead of looping
                    max_tokens=3500          # High limit to allow for long word-count generations
                )
                response = completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error communicating with Groq API: {e}")
