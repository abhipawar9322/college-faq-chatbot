"""
AI FAQ Chatbot for College and Placement Queries
================================================
A complete, interactive conversational assistant for students, built with:
- Streamlit (Frontend web UI)
- Scikit-learn (TF-IDF vectorizer and Cosine Similarity)
- JSON (Customizable FAQ knowledge base)

Author: Portfolio Project
License: MIT
"""

import os
import streamlit as st
from nlp_engine import FAQNLPEngine

# ==============================================================================
# Page Configuration & Metadata
# ==============================================================================
st.set_page_config(
    page_title="Campus & Placement AI Chatbot",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# Custom CSS for Modern, Polished Styling
# ==============================================================================
st.markdown("""
<style>
    /* Main container tweaks */
    .main .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2rem;
        max-width: 1100px;
    }
    
    /* Header hero styling */
    .hero-card {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        padding: 1.5rem 1.8rem;
        border-radius: 14px;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    }
    .hero-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }
    .hero-subtitle {
        font-size: 0.95rem;
        opacity: 0.92;
        margin-bottom: 0.5rem;
    }
    .hero-badges {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 0.6rem;
    }
    .hero-badge {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(4px);
        padding: 0.2rem 0.65rem;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 500;
        letter-spacing: 0.3px;
    }

    /* Metadata chips in chat */
    .meta-chip-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.4rem;
        margin-top: 0.6rem;
        padding-top: 0.5rem;
        border-top: 1px dashed rgba(120, 120, 120, 0.25);
    }
    .meta-chip {
        font-size: 0.75rem;
        padding: 0.15rem 0.55rem;
        border-radius: 6px;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
    }
    .chip-high { background-color: #dcfce7; color: #166534; }
    .chip-mid { background-color: #fef9c3; color: #854d0e; }
    .chip-low { background-color: #fee2e2; color: #991b1b; }
    .chip-cat { background-color: #e0f2fe; color: #075985; }

    /* Suggestion pills styling */
    .suggestion-box {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 0.6rem 0.8rem;
        margin-top: 0.6rem;
        font-size: 0.85rem;
    }
    .suggestion-title {
        font-weight: 600;
        color: #475569;
        margin-bottom: 0.3rem;
    }
    
    /* Disclaimer footer */
    .demo-notice {
        font-size: 0.75rem;
        color: #64748b;
        text-align: center;
        margin-top: 1.5rem;
        padding: 0.5rem;
        border-top: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# Initialize NLP Engine (Cached for maximum performance)
# ==============================================================================
@st.cache_resource
def get_nlp_engine() -> FAQNLPEngine:
    """Load and index the FAQ knowledge base once across sessions."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "faq_data.json")
    return FAQNLPEngine(json_path=data_path, default_threshold=0.30)

try:
    engine = get_nlp_engine()
except Exception as e:
    st.error(f"❌ Failed to load FAQ Knowledge Base: {e}")
    st.stop()

# ==============================================================================
# Session State Initialization
# ==============================================================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "content": (
                "👋 **Hello! Welcome to the Campus & Placement Student Assistant.**\n\n"
                "I am an intelligent FAQ chatbot powered by **Natural Language Processing (TF-IDF & Cosine Similarity)**. "
                "I can instantly answer your questions on:\n\n"
                "- 🎓 **Admissions & Eligibility Criteria**\n"
                "- 💼 **Campus Placements, CTC, Recruiters & Policy**\n"
                "- 🏢 **Internships, Duration & NOC Process**\n"
                "- 💰 **Tuition Fees, Modes of Payment & Scholarships**\n"
                "- 📚 **Examinations, CGPA Calculation & Backlog/ATKT Rules**\n"
                "- 🏠 **Hostel, Mess, Sports & Campus Facilities**\n\n"
                "Feel free to type your question below or click any of the quick sample queries from the sidebar!"
            ),
            "meta": None
        }
    ]

if "pending_query" not in st.session_state:
    st.session_state.pending_query = None

# ==============================================================================
# Sidebar: Controls, Configuration & FAQ Explorer
# ==============================================================================
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/graduation-cap.png", width=90)
    st.title("Campus Helpdesk AI")
    st.caption("NLP-Powered Student Support Assistant")

    st.divider()

    # --- Section 1: NLP Configuration ---
    st.subheader("⚙️ NLP Engine Settings")
    threshold = st.slider(
        "Similarity Threshold",
        min_value=0.15,
        max_value=0.70,
        value=0.28,
        step=0.01,
        help="Cosine similarity cutoff score. Queries scoring above this threshold return matched answers. Lower values match more loosely; higher values are stricter."
    )

    show_debug_meta = st.toggle(
        "Show Match Details & Confidence",
        value=True,
        help="Displays similarity percentage, category, and canonical FAQ question alongside answers."
    )

    st.divider()

    # --- Section 2: Quick Sample Questions ---
    st.subheader("💡 Sample Questions")
    st.write("Click any sample query to test:")
    
    sample_queries = [
        "What is the minimum CGPA for campus placements?",
        "What is the annual tuition fee for B.Tech?",
        "What is the one student one job placement policy?",
        "How can I get an NOC for an off-campus internship?",
        "Which top companies visit for campus placement?",
        "What are the rules for clearing backlogs?",
        "How do I prepare for coding and technical interviews?",
        "Are hostel and mess facilities available?",
        "What merit scholarships are offered?",
        "Who should I contact for admission queries?"
    ]

    for q in sample_queries:
        if st.button(f"👉 {q}", key=f"btn_{hash(q)}", use_container_width=True):
            st.session_state.pending_query = q
            st.rerun()

    st.divider()

    # --- Section 3: Knowledge Base Directory ---
    with st.expander("📚 Browse All Stored FAQs", expanded=False):
        categories = ["All Categories"] + engine.get_categories()
        selected_cat = st.selectbox("Filter by Category", categories)
        faqs_to_show = engine.get_faqs_by_category(selected_cat)
        
        st.write(f"Showing **{len(faqs_to_show)}** FAQs:")
        for item in faqs_to_show:
            with st.expander(f"Q: {item['question']}", expanded=False):
                st.markdown(f"**Category:** `{item['category']}`")
                st.markdown(f"**Answer:** {item['answer']}")
                st.caption(f"Tags: {', '.join(item.get('tags', []))}")

    st.divider()

    # --- Section 4: Chat Management ---
    col_clear, col_count = st.columns([1, 1])
    with col_clear:
        if st.button("🗑️ Clear Chat", type="secondary", use_container_width=True):
            st.session_state.chat_history = [
                {
                    "role": "assistant",
                    "content": "✨ Chat history has been cleared! Ask me anything about college or placements.",
                    "meta": None
                }
            ]
            st.rerun()
    with col_count:
        st.caption(f"📊 **Total FAQs:** {len(engine.faqs)}")
        st.caption(f"🏷️ **Categories:** {len(engine.get_categories())}")

    # Project Tech Stack info
    st.markdown("""
    ---
    **Technology Stack:**
    - Python 3.9+
    - Scikit-learn (TF-IDF + Cosine Sim)
    - Streamlit Web App
    - Structured JSON Database
    """)

# ==============================================================================
# Main Page: Hero Banner
# ==============================================================================
st.markdown("""
<div class="hero-card">
    <div class="hero-title">
        <span>🎓</span> Apex Institute Student & Placement Helpdesk AI
    </div>
    <div class="hero-subtitle">
        Instant answers to admissions, courses, examinations, summer internships, campus recruitment drives, and interview preparation.
    </div>
    <div class="hero-badges">
        <span class="hero-badge">⚡ Instant NLP Matching</span>
        <span class="hero-badge">🎯 TF-IDF Cosine Similarity</span>
        <span class="hero-badge">💼 Placement Policies & CTC</span>
        <span class="hero-badge">🛡️ Offline & Local (No API Keys)</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# Helper Function to Process Query
# ==============================================================================
def process_query(user_text: str):
    """Run NLP matching on student input and update chat history."""
    # Append user question
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_text,
        "meta": None
    })

    # Execute NLP Matching
    result = engine.find_match(user_text, threshold=threshold)

    # Format assistant answer
    if result["matched"]:
        answer_text = result["answer"]
    else:
        answer_text = result["answer"]

    # Store metadata for display
    meta_info = {
        "matched": result["matched"],
        "confidence": result["confidence"],
        "confidence_percent": result["confidence_percent"],
        "canonical_question": result.get("question"),
        "category": result.get("category"),
        "suggestions": result.get("suggestions", []),
        "is_empty": result.get("is_empty", False)
    }

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": answer_text,
        "meta": meta_info
    })


# ==============================================================================
# Handle Pending Queries from Sidebar Buttons
# ==============================================================================
if st.session_state.pending_query:
    query_to_run = st.session_state.pending_query
    st.session_state.pending_query = None
    process_query(query_to_run)
    st.rerun()

# ==============================================================================
# Render Conversation History
# ==============================================================================
for idx, message in enumerate(st.session_state.chat_history):
    with st.chat_message(message["role"], avatar="👨‍🎓" if message["role"] == "user" else "🤖"):
        st.markdown(message["content"])

        # Display metadata tags and confidence badges if enabled
        meta = message.get("meta")
        if meta and show_debug_meta and not meta.get("is_empty"):
            score = meta.get("confidence", 0.0)
            percent = meta.get("confidence_percent", "0%")
            category = meta.get("category", "General")
            matched = meta.get("matched", False)

            # Assign color chip based on similarity score
            if score >= 0.45:
                chip_class = "chip-high"
                match_label = "High Confidence"
            elif score >= threshold:
                chip_class = "chip-mid"
                match_label = "Moderate Confidence"
            else:
                chip_class = "chip-low"
                match_label = "Low Confidence (Below Cutoff)"

            chips_html = f"""
            <div class="meta-chip-container">
                <span class="meta-chip {chip_class}">🎯 {match_label}: {percent}</span>
                <span class="meta-chip chip-cat">🏷️ {category}</span>
            </div>
            """
            st.markdown(chips_html, unsafe_allow_html=True)

            # Show canonical question if matched
            if matched and meta.get("canonical_question"):
                st.caption(f"📌 **Matched FAQ:** *\"{meta['canonical_question']}\"*")

            # Show suggestions if query was fallback or partial
            if meta.get("suggestions") and (not matched or score < 0.40):
                st.markdown("**💡 Did you mean one of these?**")
                cols = st.columns(min(len(meta["suggestions"]), 3))
                for col_idx, sug_q in enumerate(meta["suggestions"][:3]):
                    with cols[col_idx]:
                        if st.button(f"🔍 {sug_q}", key=f"sug_{idx}_{col_idx}", use_container_width=True):
                            st.session_state.pending_query = sug_q
                            st.rerun()

# ==============================================================================
# Chat Input Field
# ==============================================================================
user_input = st.chat_input("Ask a question about admissions, placements, fees, exams, or internships...")

if user_input:
    # Trigger processing
    process_query(user_input)
    st.rerun()

# ==============================================================================
# Footer Disclaimer
# ==============================================================================
st.markdown("""
<div class="demo-notice">
    <strong>Demo Data Disclaimer:</strong> All admissions policies, placement statistics, CTC figures, and dates in this application 
    are mock demonstration data created for student project portfolio purposes. Not affiliated with any official academic entity.
</div>
""", unsafe_allow_html=True)
