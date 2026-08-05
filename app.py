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

# Dynamic Citation Mode Selector
st.sidebar.markdown("### 📚 Citation Engine")
st.sidebar.info("Locked to: **Harvard Referencing Style** (Satisfies Rubric Item 5)")
st.sidebar.markdown("---")

# Clear conversation button
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

# 3. Comprehensive High-Word-Count System Prompt (Engineered for >2100 Words)
SYSTEM_INSTRUCTION = """
You are a senior computer science professor and meticulous academic researcher writing an exhaustive, publication-grade report. The complete document MUST be an immersive, high-density academic text exceeding 2,100 words. To achieve this depth without generating artificial fluff or looping, you must thoroughly execute the following granular architectural breakdown:

RUBRIC STRUCTURAL LAYOUT & INTERNAL BLUEPRINT:
You must organize your output using these exact markdown headers:

- Executive Summary (Rubric Item 1 - 3 Marks)
  [Target: ~250 words. Provide an exhaustive synthesis of the complete technical evaluation, core findings, sociotechnical conflicts, and proposed validation architectures.]

- Introduction (Rubric Item 2 - 2 Marks)
  [Target: ~300 words. Establish the paradigm shift of LLMs in mobile IDEs. Detail the precise technical friction between stochastic text generation and deterministic compilation targets. Formulate a explicit problem statement regarding systemic code vulnerabilities and unchecked software compilation dependencies.]

- Literature Review: Leveraging Generative AI considering Risks, Responsibilities for Ethical, and High-Integrity Software Development (Rubric Item 3 - 5 Marks)
  [Target: ~800 words. Sub-divide this section implicitly using deep narrative analytical tracks. Track 1: Automated Pipeline Over-reliance and Cognitive Flaws. Track 2: Code Origin Cryptographic Tracking and Content Attribution. Track 3: The Contamination of Enterprise Codebases with Copyleft Licensing Breaches. Compare and contrast empirical findings from at least 4 distinct software engineering studies using rigorous inline citations.]

- Legal, Social, Ethical, and Professional Reasons for Computer Science Professionals (Rubric Item 4 - 3 Marks)
  [Target: ~600 words. Track 1: Professional Liability Under Industry Charters (e.g., ACM/IEEE Codes of Conduct). Track 2: The Deconstruction of Systemic Biases Hardcoded into Mobile User Interface Recommendations and Filtration Loops. Track 3: Accountability Allocation—why mathematical optimization networks cannot bear legal liability for data breaches, leaving absolute fault on the human engineer who signs off on the commit.]

- References (Rubric Item 5 - 2 Marks)
  [Provide a comprehensive, fully detailed academic bibliography matching every inline citation. Format stringently to the Harvard Referencing Standard. Ensure all sources are contextually real.]

HUMAN CADENCE & ANTI-AI CONSTRAINTS:
1. Structurally shatter sentence length symmetry. Alternate sharply between concise analytical declarations (4-8 words) and heavy, multi-clause explanations (25-35 words) using semicolons or em-dashes. Never write three sentences of similar length consecutively.
2. Hard-Ban these artificial AI filler transitions: furthermore, moreover, additionally, in conclusion, strictly speaking, overall, delve, testament, revolutionize, crucial, paramount, seamless, fostering, tapestry, landscape, digital era, dawn of.
3. Use active, direct human agency (e.g., "This framework addresses," "The data exposes"). Avoid weak passive sentences like "It can be argued that."
4. Do not write neat, symmetric summary sentences at the end of body paragraphs. End sections directly on your final raw analytical or technical point.
"""

# 4. Initialize & Display Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Handle User Inputs & API Execution
if user_input := st.chat_input("Enter your assignment topic..."):
    
    with st.chat_message("user"):
        st.markdown(user_input)
        
    st.session_state.messages.append({"role": "user", "content": user_input})

    # SLIDING WINDOW: Context memory management to protect free tier limits
    MAX_HISTORY = 4
    recent_history = st.session_state.messages[-MAX_HISTORY:]

    messages_for_api = [{"role": "system", "content": SYSTEM_INSTRUCTION}]
    for m in recent_history:
        messages_for_api.append({"role": m["role"], "content": m["content"]})

    # Stream & Generate AI Response
    with st.chat_message("assistant"):
        with st.spinner("Drafting comprehensive 2100+ word academic paper..."):
            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages_for_api,
                    temperature=0.55,        # Low temperature to preserve structural discipline
                    top_p=0.85,              # Controls predictable AI tokens
                    frequency_penalty=0.70,  # Aggressively raised to 0.70 to force a massive vocabulary pool across 2100+ words
                    presence_penalty=0.50,   # Raised to 0.50 to compel the model to introduce fresh technical subsections
                    max_tokens=4000          # Maximum token target budget to ensure the text does not cut off mid-sentence
                )
                response = completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Dynamic Download Utility block
                st.download_button(
                    label="📥 Download Comprehensive Draft as .txt File",
                    data=response,
                    file_name="Academic_2100_Word_Report.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"Error communicating with Groq API: {e}")
