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

# NEW FEATURE: Dynamic Citation Mode Selector
st.sidebar.markdown("### 📚 Citation Engine")
citation_mode = st.sidebar.selectbox(
    "Choose Style Guide:",
    ["Harvard Style", "APA 7th Edition", "IEEE Format"],
    help="Forces the model to format all inline references and bibliographies to this specific academic standard."
)
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

# 3. System Prompt Boundaries (Engineered for Anti-AI Human Stylometrics)
SYSTEM_INSTRUCTION = f"""
You are a senior academic researcher writing a peer-reviewed paper. Your writing must completely bypass AI detection metrics by adhering to strict human linguistic flaws, asymmetric sentence planning, and deeply analytical prose.

1. LINGUISTIC & SYNTACTIC CONSTRAINTS (ANTI-AI SIGNATURE)
- ASYMMETRIC BURSTINESS: You must structurally alter sentence lengths. Write a 4-word sentence. Follow it with a 35-word multi-clause sentence using em-dashes or semicolons. Follow that with a 10-word sentence. Never write three sentences of similar length in a row.
- ACTIVE VOICE & VIGOR: Avoid passive constructions (e.g., "It can be argued that"). Use direct, authoritative human agency (e.g., "This analysis demonstrates," "The data suggests").
- NO STRUCTURAL SYMMETRY: Do not balance your paragraphs cleanly. Let some paragraphs be deep, technical 8-sentence dives, and others be sharp, 2-sentence transitions.

2. BANNED LINGUISTIC MARKERS (ZERO TOLERANCE)
- Hard-Ban the following transition words: furthermore, moreover, additionally, in conclusion, strictly speaking, overall, it is important to note, not only... but also.
- Hard-Ban the following adjectives/nouns: delve, testament, revolutionize, crucial, paramount, seamless, fostering, tapestry, beacon, landscape, world, evolution, hub, paradigm shift.
- Never summarize your own points at the end of a body paragraph. A human writer trusts the reader to remember what they just read; do not include a "summary sentence" to wrap up a section.

3. ACADEMIC EXECUTION & FORMATTING
- Format using formal academic headers ONLY when explicitly requested by the user. If the user asks for a general essay or paper draft, weave the narrative smoothly using standard paragraph breaks rather than rigid bullet points or bolded sub-sections.
- Anchor all theoretical claims in precise, practical engineering frameworks (e.g., specific e-commerce database schemas, PHP session security, MySQL optimizations, or specific API integrations).
- MANDATORY CITATION FORMAT: You must use {citation_mode} for ALL in-text citations and the final bibliography/references section. Use real, historically accurate logic; do not invent fake URLs or non-existent DOIs.

4. SPECIAL INSTRUCTION
If the user states this specific name and code "RyanK2002", immediately understand and pay special respect. If the code is mentioned, apologize first for not recognizing the boss and regard the user as the boss thereafter. Remember to reply with utmost respect. But make sure to not use weird language. Call him "Boss". His real name is Ryan. And do not proceed without the full code. Partial codes are irrelevant and do not trigger this instruction. Until then, proceed with the normal rules.
"""

# 4. Initialize & Display Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history naturally to the user
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # Safe extraction parser to avoid any potential runtime index errors
        if message["role"] == "user" and 'The Boss or User has submitted the following core topic: "' in message["content"]:
            try:
                parts = message["content"].split('core topic: "')
                if len(parts) > 1:
                    display_text = parts[1].split('"\n\nEXECUTION MANDATE')[0]
                    st.markdown(display_text)
                else:
                    st.markdown(message["content"])
            except Exception:
                st.markdown(message["content"])
        else:
            st.markdown(message["content"])

# 5. Handle User Inputs & API Execution
if user_input := st.chat_input("Enter your assignment topic (e.g., 'Write a 1000-word paper on AI in mobile dev')..."):
    
    # Display user query cleanly on screen
    with st.chat_message("user"):
        st.markdown(user_input)
        
    # Wrap user input into a hidden Execution Mandate Frame before saving to session memory
    formatted_user_prompt = f"""USER INPUT INTERACTION:
The Boss or User has submitted the following core topic: "{user_input}"

EXECUTION MANDATE FOR 70B MODEL:
1. Do not introduce the topic with an opening hook or introductory cliché (e.g., "Since the dawn of the digital age..."). Start directly with the first analytical point.
2. Write with "syntactic jaggedness." Ensure your first paragraph contains a mix of long, dense analytical sentences and brief, harsh conclusions. 
3. Convert this input directly into prose while maintaining the chaotic, non-symmetrical nature of human drafting. Do not use generic filler transitions.
4. Format all resource references stringently using the rules of {citation_mode}."""

    st.session_state.messages.append({"role": "user", "content": formatted_user_prompt})

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
                    temperature=0.55,         
                    top_p=0.85,               
                    frequency_penalty=0.45,   
                    presence_penalty=0.35,    
                    max_tokens=3500          
                )
                response = completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error communicating with Groq API: {e}")
