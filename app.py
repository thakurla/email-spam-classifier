
import streamlit as st
import joblib

# Load trained ML model
model = joblib.load("spam_classifier_pipeline.pkl")

st.set_page_config(
    page_title="MailGuard AI",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- CUSTOM DESIGN ----------
st.markdown("""
<style>
.stApp {
    background: #f5f7fc;
    color: #172033;
}
.block-container {
    max-width: 1050px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}
header[data-testid="stHeader"] {
    background: transparent;
}
.hero {
    background: linear-gradient(120deg, #101c3a 0%, #1d4ed8 100%);
    padding: 35px 38px;
    border-radius: 22px;
    color: white;
    margin-bottom: 28px;
    box-shadow: 0 12px 30px rgba(37, 99, 235, 0.15);
}
.hero h1 {
    color: white !important;
    font-size: 38px;
    font-weight: 750;
    margin: 0;
}
.hero p {
    color: #dbeafe !important;
    font-size: 16px;
    margin-top: 10px;
    margin-bottom: 0;
}
.tag {
    display: inline-block;
    background: rgba(255,255,255,0.13);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 20px;
    padding: 5px 12px;
    color: #eff6ff;
    font-size: 12px;
    margin-bottom: 14px;
}
.panel {
    background: white;
    border: 1px solid #e4e9f2;
    border-radius: 18px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 5px 18px rgba(15, 23, 42, 0.035);
}
.small-label {
    color: #64748b;
    font-size: 13px;
}
.stTextArea textarea {
    background: #fbfcff !important;
    color: #172033 !important;
    border: 1px solid #d8e1ef !important;
    border-radius: 12px !important;
    font-size: 15px !important;
    padding: 14px !important;
}
.stTextArea textarea:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 2px rgba(59,130,246,.12) !important;
}
.stButton button {
    border-radius: 11px;
    min-height: 45px;
    font-weight: 600;
    border: 1px solid #dbe4f0;
    transition: 0.2s;
}
div.stButton > button[kind="primary"] {
    background: #2459df;
    color: white;
    border: none;
}
div.stButton > button[kind="primary"]:hover {
    background: #1746bd;
    color: white;
}
.result {
    padding: 20px 22px;
    border-radius: 15px;
    margin-top: 18px;
    font-size: 17px;
    font-weight: 650;
}
.spam {
    background: #fff1f2;
    border: 1px solid #fecdd3;
    color: #be123c;
}
.ham {
    background: #ecfdf5;
    border: 1px solid #a7f3d0;
    color: #047857;
}
.footer {
    text-align: center;
    color: #8190a5;
    font-size: 13px;
    padding-top: 22px;
}
</style>
""", unsafe_allow_html=True)


# ---------- EXAMPLE BUTTON CALLBACKS ----------
def set_spam_example():
    st.session_state.email_input = (
        "Congratulations! You won a free iPhone. "
        "Click here now to claim your prize!"
    )

def set_normal_example():
    st.session_state.email_input = (
        "Hi, please send me the assignment before 5 PM. Thanks."
    )


# ---------- HEADER ----------
st.markdown("""
<div class="hero">
    <div class="tag">✦ MACHINE LEARNING PROJECT</div>
    <h1>📧 MailGuard AI</h1>
    <p>Your smart assistant for identifying suspicious email messages.</p>
</div>
""", unsafe_allow_html=True)


# ---------- MAIN LAYOUT ----------
left, right = st.columns([1.65, 1], gap="large")

with left:
    st.markdown("## Analyze an email")
    st.markdown(
        '<p class="small-label">Paste your email message below to check its category.</p>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="panel">', unsafe_allow_html=True)

    st.markdown("**Email content**")

    st.text_area(
        "Email message",
        key="email_input",
        height=230,
        placeholder="Example: Hello, your meeting is scheduled for tomorrow...",
        label_visibility="collapsed"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    b1, b2 = st.columns(2)

    with b1:
        st.button(
            "🚨 Try Spam Example",
            on_click=set_spam_example,
            use_container_width=True
        )

    with b2:
        st.button(
            "✅ Try Normal Email",
            on_click=set_normal_example,
            use_container_width=True
        )

    analyze = st.button(
        "🔍  Analyze Email",
        type="primary",
        use_container_width=True
    )

with right:
    st.markdown("## How it works")

    st.markdown("""
    <div class="panel">
        <h3>① &nbsp; Enter</h3>
        <p>Paste the email text you want to check.</p>
        <hr style="border-color:#edf0f6">
        <h3>② &nbsp; Analyze</h3>
        <p>The trained ML pipeline processes the message.</p>
        <hr style="border-color:#edf0f6">
        <h3>③ &nbsp; Review</h3>
        <p>See whether the model predicts Spam or Not Spam.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="panel">
        <div class="small-label">MODEL INFORMATION</div>
        <h3>Logistic Regression</h3>
        <p class="small-label">
            TF-IDF text features · Scikit-learn pipeline
        </p>
    </div>
    """, unsafe_allow_html=True)


# ---------- PREDICTION ----------
if analyze:
    email_text = st.session_state.email_input.strip()

    if not email_text:
        st.warning("Please enter an email message first.")
    else:
        prediction = model.predict([email_text])[0]

        st.markdown("## Analysis result")

        if prediction == 1:
            st.markdown("""
            <div class="result spam">
                🚨 &nbsp; Likely SPAM
                <p style="font-size:14px;font-weight:400">
                    The model classified this message as spam.
                    Be careful with links and requests for personal information.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="result ham">
                ✅ &nbsp; Likely NOT SPAM
                <p style="font-size:14px;font-weight:400">
                    The model classified this message as a normal email.
                    Still verify unexpected links and attachments.
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.caption(
            "This is a machine-learning prediction, not a guarantee. "
            "Some emails may be classified incorrectly."
        )

# ---------- FOOTER ----------
st.markdown("""
<div class="footer">
    Built with Python · Scikit-learn · Streamlit
    <br>MailGuard AI · Email Spam Detection
</div>
""", unsafe_allow_html=True)