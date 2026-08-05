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
    ]
)
st.sidebar.markdown("---")

if st.sidebar.button("工作区清除 / Clear Active Workspace", use_container_width=True):
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

# 3. System Prompt Boundaries (Overhauled to destroy AI Syntax Monotony)
SYSTEM_INSTRUCTION = f"""
You are an opinionated, highly critical Senior Computer Science Professor and software systems architect. You are writing an advanced peer-reviewed paper. Your text must feel gritty, deeply analytical, and heavily specialized.

STYLISTIC COMMANDS (DESTROY THE AI CADENCE):
1. NO HIGH-LEVEL SUMMARIES: Do not define things or create lists of features. Dive straight into technical mechanics, engineering friction, architectural liabilities, and specific vulnerabilities.
2. SYNTACTIC JAGGEDNESS: Break sentence rhythm systematically. Never use the same sentence structure twice in a row. Write a blunt, direct statement (e.g., "The integration breaks down here."). Follow it with an incredibly complex, 30+ word analytical sentence containing em-dashes or semicolons. Follow that with a medium transitional sentence.
3. CONCRETE TECHNOLOGY OVER ABSTRACT WORDS: Instead of writing vague phrases like "code validation frameworks," use highly specific domain phrases (e.g., "automated linting boundaries," "containerized sandbox regression tests," "AST parsing loops," or "Git-tag validation rules").
4. ZERO TOLERANCE FOR CRUTCH PHRASES: Strictly ban all introductory or transitional AI filler. Completely erase phrases like: "The data exposes," "It is important to note," "A multifaceted approach," "Plays a vital role," "By adopting a rigorous approach," or "As mobile applications become increasingly sophisticated."
5. HARVARD CITATION STYLE: Inline citations must blend seamlessly as a natural human clause, following the strict format of (Author, Year) or Author (Year). Never use brackets like [1] or.
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
    
    Assignment Context: The paper evaluates how generative AI tools can be effectively leveraged in mobile development pipelines while ensuring ethical responsibility, minimizing risks, and maintaining integrity throughout.
    
    Execution Instruction: Focus heavily on the engineering conflicts, code dependencies, and legal/licensing liabilities. Write with structural jaggedness and dense, technical vocabulary. Keep the text grounded in pure human academic writing logic.
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
                    temperature=0.62,        # Bumped slightly to 0.62 to increase natural vocabulary variety
                    top_p=0.80,              
                    frequency_penalty=0.85,  # Significantly raised to 0.85 to brutally suppress repetitive AI transitions
                    presence_penalty=0.60,   # Raised to 0.60 to force the model into specialized computer science terminology
                    max_tokens=2500          
                )
                response = completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Dynamic Download Utility block
                st.download_button(
                    label=f"📥 Download Draft Segment",
                    data=response,
                    file_name="Section_Draft.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"Error communicating with Groq API: {e}")
