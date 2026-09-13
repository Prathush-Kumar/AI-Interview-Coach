import streamlit as st


def load_css():
    st.html("""
    <style>

    /* ==============================
       GLOBAL
       ============================== */

    .stApp {
        background:
            radial-gradient(
                circle at 15% 10%,
                rgba(99, 102, 241, 0.15),
                transparent 30%
            ),
            radial-gradient(
                circle at 85% 20%,
                rgba(168, 85, 247, 0.12),
                transparent 30%
            ),
            #080b14;

        color: #f8fafc;
    }

    .main .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* ==============================
       HIDE STREAMLIT UI
       ============================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }


    /* ==============================
       HERO
       ============================== */

    .hero {
        text-align: center;
        padding: 45px 20px 30px 20px;
    }

    .hero-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 30px;
        background: rgba(99, 102, 241, 0.12);
        border: 1px solid rgba(129, 140, 248, 0.25);
        color: #a5b4fc;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 20px;
        animation: fadeUp 0.7s ease;
    }

    .hero h1 {
        font-size: 54px;
        line-height: 1.1;
        margin: 0;
        font-weight: 800;
        letter-spacing: -2px;

        background: linear-gradient(
            90deg,
            #ffffff,
            #c4b5fd,
            #93c5fd
        );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;

        animation: fadeUp 0.8s ease;
    }

    .hero p {
        max-width: 680px;
        margin: 20px auto 0 auto;
        color: #94a3b8;
        font-size: 18px;
        line-height: 1.7;
        animation: fadeUp 1s ease;
    }


    /* ==============================
       SECTION
       ============================== */

    .section-title {
        color: #f8fafc;
        font-size: 24px;
        font-weight: 700;
        margin-top: 30px;
        margin-bottom: 8px;
    }

    .section-subtitle {
        color: #94a3b8;
        font-size: 14px;
        margin-bottom: 20px;
    }


    /* ==============================
       CARDS
       ============================== */

    .feature-card {
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 18px;
        padding: 26px;
        height: 100%;

        transition:
            transform 0.25s ease,
            border-color 0.25s ease,
            box-shadow 0.25s ease;

        animation: fadeUp 0.7s ease;
    }

    .feature-card:hover {
        transform: translateY(-5px);

        border-color: rgba(129, 140, 248, 0.35);

        box-shadow:
            0 15px 45px rgba(0, 0, 0, 0.25);
    }

    .feature-icon {
        font-size: 30px;
        margin-bottom: 15px;
    }

    .feature-card h3 {
        margin: 0 0 10px 0;
        color: #f8fafc;
        font-size: 20px;
    }

    .feature-card p {
        color: #94a3b8;
        line-height: 1.6;
        font-size: 14px;
    }


    /* ==============================
       JOB DESCRIPTION TEXTAREA
       ============================== */

    div[data-testid="stTextArea"] textarea {
        background: #252a3a !important;

        border: 1px solid rgba(148, 163, 184, 0.30) !important;

        border-radius: 14px !important;

        color: #ffffff !important;

        caret-color: #ffffff !important;

        font-size: 15px !important;
    }

    /* Placeholder text */
    div[data-testid="stTextArea"] textarea::placeholder {
        color: #d1d5db !important;
        opacity: 1 !important;
    }

    /* Text while typing */
    div[data-testid="stTextArea"] textarea:focus {
        color: #ffffff !important;

        background: #252a3a !important;

        border-color: #818cf8 !important;

        box-shadow:
            0 0 0 1px #818cf8 !important;
    }


    /* ==============================
       FILE UPLOADER
       ============================== */

    div[data-testid="stFileUploader"] {
        background: rgba(15, 23, 42, 0.55) !important;

        border: 1px dashed rgba(129, 140, 248, 0.35) !important;

        border-radius: 16px !important;

        padding: 8px !important;

        color: #ffffff !important;
    }

    div[data-testid="stFileUploader"]:hover {
        border-color: #818cf8 !important;
    }


    /* Upload button */

    div[data-testid="stFileUploader"] button {
        background: linear-gradient(
            135deg,
            #6366f1,
            #8b5cf6
        ) !important;

        color: #ffffff !important;

        border: none !important;

        border-radius: 10px !important;

        font-weight: 700 !important;
    }

    div[data-testid="stFileUploader"] button:hover {
        background: linear-gradient(
            135deg,
            #4f46e5,
            #7c3aed
        ) !important;
    }

    /* Upload button text */

    div[data-testid="stFileUploader"] button span {
        color: #ffffff !important;
    }

    div[data-testid="stFileUploader"] button svg {
        color: #ffffff !important;
        fill: #ffffff !important;
    }

    /* Upload area text */

    div[data-testid="stFileUploader"] label {
        color: #e5e7eb !important;
    }

    div[data-testid="stFileUploader"] small {
        color: #cbd5e1 !important;
    }


    /* ==============================
       NORMAL BUTTONS
       ============================== */

    .stButton > button {
        width: 100%;

        border-radius: 12px;

        border: 1px solid rgba(129, 140, 248, 0.35);

        background: linear-gradient(
            135deg,
            #6366f1,
            #8b5cf6
        );

        color: #ffffff !important;

        font-weight: 700;

        font-size: 15px;

        padding: 13px 20px;

        transition: all 0.25s ease;
    }

    .stButton > button span {
        color: #ffffff !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px);

        box-shadow:
            0 10px 30px rgba(99, 102, 241, 0.25);

        border-color: #a5b4fc;
    }


    /* ==============================
       SCORE CARD
       ============================== */

    .score-card {
        background: rgba(15, 23, 42, 0.8);

        border: 1px solid rgba(129, 140, 248, 0.18);

        border-radius: 20px;

        padding: 28px;

        text-align: center;

        animation: fadeUp 0.6s ease;
    }

    .score-number {
        font-size: 52px;

        font-weight: 800;

        color: #a5b4fc;
    }

    .score-label {
        color: #94a3b8;

        font-size: 14px;
    }


    /* ==============================
       LOADING BOX
       ============================== */

    .loading-box {
        background: rgba(15, 23, 42, 0.8);

        border: 1px solid rgba(129, 140, 248, 0.2);

        border-radius: 18px;

        padding: 30px;

        text-align: center;

        animation: pulse 2s infinite;
    }

    .loading-spinner {
        width: 42px;

        height: 42px;

        border: 4px solid rgba(129, 140, 248, 0.2);

        border-top: 4px solid #818cf8;

        border-radius: 50%;

        margin: 0 auto 18px auto;

        animation: spin 1s linear infinite;
    }

    .loading-text {
        color: #cbd5e1;

        font-size: 16px;

        font-weight: 600;
    }


    /* ==============================
       ANIMATIONS
       ============================== */

    @keyframes spin {

        from {
            transform: rotate(0deg);
        }

        to {
            transform: rotate(360deg);
        }

    }

    @keyframes pulse {

        0%, 100% {
            opacity: 1;
        }

        50% {
            opacity: 0.75;
        }

    }

    @keyframes fadeUp {

        from {
            opacity: 0;

            transform: translateY(15px);
        }

        to {
            opacity: 1;

            transform: translateY(0);
        }

    }


    /* ==============================
       RESPONSIVE
       ============================== */

    @media (max-width: 768px) {

        .hero h1 {
            font-size: 38px;
        }

        .hero p {
            font-size: 16px;
        }

        .main .block-container {
            padding-left: 1rem;

            padding-right: 1rem;
        }

    }

    </style>
    """)