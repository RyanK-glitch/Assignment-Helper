import streamlit as st
from groq import Groq

# 1. Page Configuration & Custom UI
st.set_page_config(page_title="Rubric-Aligned Academic Portal", page_icon="🎓", layout="centered")

st.title("🎓 Rubric-Aligned Academic Workspace")
st.caption("Generates targeted, high-density academic segments to satisfy 100% of your coursework metrics.")

# Sidebar controls & Branding
st.sidebar.markdown("### ⚙️ Workspace Panel")
st.sidebar.markdown("👨‍💻 **Developed by: RyanK**")
st.sidebar.markdown("---")

# STEP-BY-STEP CONTROL: This solves the 3000-token cutoff error entirely
st.sidebar.markdown("### 🎯 Modular Target Selector")
selected_section = st.sidebar.selectbox(
    "Choose Target Section to Draft:",
    [
        "1. Executive Summary (Rubric Item 1 - 3 Marks)",
        "2. Introduction (Rubric Item 2 - 2 Marks)",
        "3. Literature Review: Part 1 - Pipeline Flaws & Cognitive Bias (Rubric Item 3 - 5 Marks)",
        "4. Literature Review: Part 2 - Code Provenance & Licensing Risks (Rubric Item 3 - 5 Marks)",
        "5. Legal, Social, Ethical, and Professional Accountability (Rubric Item 4 - 3 Marks)",
        "6. Final Consolidated Harvard References Bibliography (Rubric Item 5 - 2 Marks)"
    ],
    help="Drafting section-by-section guarantees maximum word count density and eliminates text truncation."
)
st.sidebar.markdown("---")

# Clear conversation button
if st.sidebar.button("🧹 Clear Active Workspace", use_container_width=True):
    st.session_state.messages = []
    st.rerun()

# 2. Secure Groq API Connection
if "GROQ_API_KEY" in st.secrets:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
else:
    GROQ_API_KEY = st.sidebar.text_input("Enter Groq API Key:", type="password")

if not GROQ_API_KEY:
    st.info("Please insert your Groq API token to initialize the academic canvas.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# 3. System Prompt Boundaries (Re-engineered for Section-Specific Human Execution)
SYSTEM_INSTRUCTION = f"""
You are a senior computer science professor and senior software reviewer. Your goal is to draft a massive, deeply detailed academic text focused exclusively on the user's selected section blueprint.

TARGET EXECUTION FOCUS:
You are currently writing ONLY the following segment: "{selected_section}".
You must expand this section with profound technical specificity, detailing explicit architectural flows, code validation frameworks, static analysis mechanisms, or professional ethics codes relevant to mobile engineering.

CRITICAL LINGUISTIC & ANTI-AI CONSTRAINTS:
1. HARVARD CITATION MANDATE: Every reference must use explicit Harvard text tags like (Kim et al., 2020) or (Singh and Kumar, 2019). NEVER use bracketed numbers like [1] or.
2. ZERO LOOPING & HIGH LEXICAL DENSITY: Do not repeat concepts, definitions, or introductory phrases. Never start sentences with repetitive crutches like "The data exposes" or "It is important to note."
3. STRUCTURAL ASYMMETRIC BURSTINESS: Alter sentence patterns continuously. Write a brief 5-word statement. Follow it immediately with a complex, 35-word analytical observation using semicolons or em-dashes. 
4. HARD-BANNED FILLER WORDS: Completely omit: furthermore, moreover, additionally, in conclusion, strictly speaking, overall, delve, testament, revolutionize, crucial, paramount, seamless, fostering, tapestry, landscape, digital era, dawn of.
5. End paragraphs cleanly on the final logical deduction without summary loops.
"""

# 4. Display Workspace History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Handle Target Triggers & Running API State
st.info(f"👉 **Active Mode:** The engine is configured to draft **{selected_section}** with a 600-800 word local expansion focus.")

if st.button("🚀 Execute High-Density Section Generation", type="primary", use_container_width=True):
    
    execution_prompt = f"""
    Draft the target assignment portion: "{selected_section}".
    
    Topic Requirements: Focus explicitly on explaining how generative AI tools can be effectively leveraged in mobile development pipelines while ensuring ethical responsibility, minimizing risks, and maintaining integrity throughout.
    
    Ensure all in-text markers strictly follow the (Author, Year) Harvard format. Do not summarize or use banned AI filler words.
    """
    
    with st.chat_message("user"):
        st.markdown(f"Generate focus draft for: {selected_section}")
        
    st.session_state.messages.append({"role": "user", "content": f"Generate focus draft for: {selected_section}"})

    # Stream & Generate AI Response
    with st.chat_message("assistant"):
        with st.spinner("Compiling focused academic layer..."):
            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": SYSTEM_INSTRUCTION},
                        {"role": "user", "content": execution_prompt}
                    ],
                    temperature=0.58,        
                    top_p=0.82,              
                    frequency_penalty=0.75,  # Aggressively raised to 0.75 to completely destroy repetitive text loops
                    presence_penalty=0.55,   # Raised to 0.55 to force completely new vocabulary terms
                    max_tokens=2500          
                )
                response = completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Dynamic Download Utility block
                st.download_button(
                    label=f"📥 Download {selected_section.split(' ')[1]} Draft Segment",
                    data=response,
                    file_name=f"Segment_{selected_section.split(' ')[1]}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"Error communicating with Groq API: {e}")
