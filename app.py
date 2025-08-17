import streamlit as st
from datetime import datetime
import os
import re
import math
import random
from collections import Counter, defaultdict
import pandas as pd
import pylangacq

st.set_page_config(page_title="Thryve - Language Analyzer & Questionnaire", layout="wide")

# Custom CSS for beautiful styling
# Custom CSS for beautiful styling
st.markdown("""
<style>
/* Hide Streamlit default elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}

/* Global styling */
.stApp {
    background: linear-gradient(135deg, #f8f9ff 0%, #f0f2ff 100%);
}

/* Header styling */
.main-header {
    display: flex;
    align-items: center;
    padding: 20px 0;
    margin-bottom: 40px;
}

.logo-container {
    display: flex;
    align-items: center;
    gap: 12px;
}

.logo-icon {
    width: 50px;
    height: 50px;
    background: linear-gradient(135deg, #8b5cf6, #a855f7);
    border-radius: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 24px;
    font-weight: bold;
}

.logo-text {
    font-size: 32px;
    font-weight: 700;
    color: #1f2937;
    margin: 0;
}

/* Hero section */
.hero-section {
    text-align: left;
    margin: 60px 0;
}

.hero-title {
    font-size: 64px;
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 24px;
    color: #1f2937;
}

.hero-title .highlight {
    color: #8b5cf6;
}

.hero-subtitle {
    font-size: 20px;
    color: #6b7280;
    line-height: 1.6;
    margin-bottom: 40px;
    max-width: 600px;
}

/* Features section */
.features-section {
    margin: 100px 0;
    text-align: center;
}

.section-title {
    font-size: 48px;
    font-weight: 700;
    color: #1f2937;
    margin-bottom: 16px;
}

.section-subtitle {
    font-size: 18px;
    color: #6b7280;
    margin-bottom: 60px;
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
}

.feature-card {
    background: white;
    padding: 40px;
    border-radius: 20px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    border: 1px solid #f3f4f6;
    transition: all 0.3s ease;
    text-align: left;
}

.feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12);
}

.feature-icon {
    width: 60px;
    height: 60px;
    background: linear-gradient(135deg, #8b5cf6, #a855f7);
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 24px;
    color: white;
    font-size: 28px;
}

.feature-title {
    font-size: 24px;
    font-weight: 600;
    color: #1f2937;
    margin-bottom: 16px;
}

.feature-description {
    font-size: 16px;
    color: #6b7280;
    line-height: 1.6;
    margin-bottom: 20px;
}

/* Hero illustration */
.hero-illustration {
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(168, 85, 247, 0.15));
    border-radius: 24px;
    padding: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 400px;
    position: relative;
    overflow: hidden;
}

.illustration-placeholder {
    text-align: center;
    color: #8b5cf6;
    font-size: 18px;
    font-weight: 600;
}

.progress-badge {
    position: absolute;
    bottom: 40px;
    left: 40px;
    background: white;
    padding: 12px 20px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    display: flex;
    align-items: center;
    gap: 12px;
}

.progress-icon {
    width: 32px;
    height: 32px;
    background: linear-gradient(135deg, #8b5cf6, #a855f7);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 16px;
}

.progress-text {
    color: #1f2937;
    font-weight: 600;
}

.progress-subtext {
    color: #6b7280;
    font-size: 14px;
}

/* Question container with purple gradient */
.question-box {
    background: linear-gradient(135deg, #8b5cf6, #a855f7);
    padding: 50px;
    border-radius: 20px;
    margin: 40px 0;
    box-shadow: 0 10px 40px rgba(139, 92, 246, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.2);
    text-align: center;
}

.question-text {
    color: white;
    font-size: 28px;
    font-weight: 700;
    text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
    line-height: 1.4;
    margin: 0;
    text-align: center;
}

/* Analysis Interface Styles */
.analysis-container {
    max-width: 1400px;
    margin: 0 auto;
}

.header {
    text-align: center;
    margin-bottom: 50px;
}

.header h1 {
    font-size: 48px;
    font-weight: 700;
    background: linear-gradient(135deg, #8b5cf6, #a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 16px;
}

.header p {
    font-size: 20px;
    color: #6b7280;
}

.overview-section {
    margin-bottom: 50px;
}

.overview-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 25px;
    margin-bottom: 40px;
}

.overview-card {
    background: white;
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0 4px 25px rgba(139, 92, 246, 0.08);
    border: 2px solid transparent;
    background-clip: padding-box;
    position: relative;
    transition: all 0.3s ease;
}

.overview-card::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 20px;
    padding: 2px;
    background: linear-gradient(135deg, #8b5cf6, #ec4899, #06b6d4);
    mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    mask-composite: subtract;
    pointer-events: none;
}

.overview-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 40px rgba(139, 92, 246, 0.15);
}

.card-label {
    color: #8b5cf6;
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
    margin-bottom: 12px;
}

.card-value {
    font-size: 28px;
    font-weight: 700;
    color: #1f2937;
}

.status-card {
    background: linear-gradient(135deg, #8b5cf6, #a855f7);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15px;
    font-size: 20px;
    font-weight: 600;
    grid-column: span 2;
}

.status-icon {
    font-size: 24px;
}

.metrics-section {
    margin-bottom: 50px;
}

.section-title {
    font-size: 32px;
    font-weight: 700;
    color: #1f2937;
    margin-bottom: 30px;
    display: flex;
    align-items: center;
    gap: 15px;
}

.title-icon {
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, #8b5cf6, #a855f7);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 20px;
}

.metrics-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 25px;
    margin-bottom: 40px;
}

.metric-card {
    background: white;
    border-radius: 24px;
    padding: 40px;
    box-shadow: 0 4px 25px rgba(139, 92, 246, 0.08);
    border: 1px solid #f1f5f9;
    transition: all 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 35px rgba(139, 92, 246, 0.12);
}

.metric-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 25px;
}

.metric-title {
    font-size: 24px;
    font-weight: 600;
    color: #1f2937;
    margin-bottom: 8px;
}

.metric-description {
    font-size: 16px;
    color: #6b7280;
    line-height: 1.5;
    max-width: 300px;
}

.metric-value {
    font-size: 48px;
    font-weight: 800;
    background: linear-gradient(135deg, #8b5cf6, #a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: right;
}

.metric-target {
    font-size: 14px;
    color: #9ca3af;
    text-align: right;
    margin-top: 4px;
}

.progress-section {
    margin-bottom: 20px;
}

.progress-bar {
    width: 100%;
    height: 12px;
    background: #f1f5f9;
    border-radius: 6px;
    overflow: hidden;
    margin-bottom: 15px;
    position: relative;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #8b5cf6, #a855f7, #06b6d4);
    border-radius: 6px;
    transition: width 1s ease;
}

.progress-labels {
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    color: #9ca3af;
    margin-bottom: 20px;
}

.performance-badge {
    padding: 12px 20px;
    border-radius: 25px;
    font-size: 14px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.badge-excellent {
    background: linear-gradient(135deg, #d1fae5, #a7f3d0);
    color: #065f46;
}

.badge-good {
    background: linear-gradient(135deg, #dbeafe, #93c5fd);
    color: #1e40af;
}

.badge-adequate {
    background: linear-gradient(135deg, #fef3c7, #fcd34d);
    color: #92400e;
}

.insights-section {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 30px;
    margin-bottom: 50px;
}

.insight-card {
    background: white;
    border-radius: 20px;
    padding: 35px;
    box-shadow: 0 4px 25px rgba(139, 92, 246, 0.08);
    border: 1px solid #f1f5f9;
}

.insight-header {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 25px;
}

.insight-icon {
    width: 50px;
    height: 50px;
    background: linear-gradient(135deg, #8b5cf6, #a855f7);
    border-radius: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 20px;
}

.insight-title {
    font-size: 22px;
    font-weight: 600;
    color: #1f2937;
}

.insight-content {
    color: #4b5563;
    font-size: 16px;
    line-height: 1.6;
    margin-bottom: 20px;
}

.milestone-highlight {
    background: linear-gradient(135deg, #f3f4f6, #e5e7eb);
    padding: 20px;
    border-radius: 12px;
    border-left: 4px solid #8b5cf6;
}

.milestone-label {
    font-weight: 600;
    color: #8b5cf6;
    margin-bottom: 8px;
}

.stats-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-top: 20px;
}

.stat-item {
    text-align: center;
    padding: 15px;
    background: #f8fafc;
    border-radius: 12px;
}

.stat-label {
    font-size: 12px;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 8px;
}

.stat-value {
    font-size: 20px;
    font-weight: 700;
    color: #1f2937;
}

.stat-value.success {
    color: #10b981;
}

.stat-value.primary {
    color: #8b5cf6;
}

@media (max-width: 768px) {
    .hero-title {
        font-size: 40px;
    }

    .feature-card {
        padding: 30px;
    }

    .overview-grid {
        grid-template-columns: 1fr;
    }

    .status-card {
        grid-column: span 1;
    }

    .metrics-grid {
        grid-template-columns: 1fr;
        gap: 20px;
    }

    .insights-section {
        grid-template-columns: 1fr;
    }

    .metric-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 20px;
    }

    .metric-value {
        text-align: left;
        font-size: 40px;
    }

    .metric-target {
        text-align: left;
    }
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "current_section" not in st.session_state:
    st.session_state.current_section = 0
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "responses" not in st.session_state:
    st.session_state.responses = {}
if "section_completed" not in st.session_state:
    st.session_state.section_completed = {}
if "results_df" not in st.session_state:
    st.session_state.results_df = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "landing"

# Age group norms for language analysis
norms = {
    "G1": {
        "min": 17, "max": 24,
        "mlu_morphemes": (1.0, 1.8),    # Morpheme-based MLU
        "mattr": (0.45, 0.65),          # Moving Average TTR
        "ndw": (15, 45),                # Number Different Words
        "ttr": (0.40, 0.70),            # Type-Token Ratio
        "complex_ratio": (0.0, 0.15),   # Complex sentence ratio
        "vocd": (20, 45),               # VocD estimate
        "min_utterances": 30            # Minimum for reliable analysis
    },
    "G2": {
        "min": 25, "max": 30,
        "mlu_morphemes": (1.8, 2.5),
        "mattr": (0.40, 0.60),
        "ndw": (35, 75),
        "ttr": (0.35, 0.65),
        "complex_ratio": (0.05, 0.25),
        "vocd": (35, 60),
        "min_utterances": 40
    },
    "G3": {
        "min": 31, "max": 36,
        "mlu_morphemes": (2.5, 3.5),
        "mattr": (0.50, 0.66),
        "ndw": (60, 120),
        "ttr": (0.40, 0.70),
        "complex_ratio": (0.10, 0.35),
        "vocd": (50, 75),
        "min_utterances": 50
    },
    "G4": {
        "min": 37, "max": 42,
        "mlu_morphemes": (3.5, 4.5),
        "mattr": (0.55, 0.70),
        "ndw": (80, 160),
        "ttr": (0.45, 0.72),
        "complex_ratio": (0.15, 0.45),
        "vocd": (60, 85),
        "min_utterances": 60
    },
    "G5": {
        "min": 43, "max": 48,
        "mlu_morphemes": (4.5, 5.5),
        "mattr": (0.60, 0.74),
        "ndw": (100, 200),
        "ttr": (0.50, 0.75),
        "complex_ratio": (0.20, 0.55),
        "vocd": (70, 95),
        "min_utterances": 70
    },
    "G6": {
        "min": 49, "max": 54,
        "mlu_morphemes": (5.5, 6.5),
        "mattr": (0.64, 0.78),
        "ndw": (120, 250),
        "ttr": (0.52, 0.78),
        "complex_ratio": (0.25, 0.65),
        "vocd": (80, 105),
        "min_utterances": 80
    },
    "G7": {
        "min": 55, "max": 60,
        "mlu_morphemes": (6.5, 7.5),
        "mattr": (0.66, 0.80),
        "ndw": (140, 300),
        "ttr": (0.55, 0.80),
        "complex_ratio": (0.30, 0.75),
        "vocd": (90, 115),
        "min_utterances": 90
    }
}

# SWYC Questionnaire Data
questionnaire_data = {
    2: {
        "title": "SWYC: 2 months",
        "subtitle": "1 months, 0 days to 3 months, 31 days",
        "version": "V1.08, 9/1/19",
        "sections": [
            {
                "title": "DEVELOPMENTAL MILESTONES",
                "description": "Most children at this age will be able to do some (but not all) of the developmental tasks listed below. Please tell us how much your child is doing each of these things.",
                "options": ["Not Yet", "Somewhat", "Very Much"],
                "questions": [
                    "Makes sounds that let you know he or she is happy or upset",
                    "Seems happy to see you",
                    "Follows a moving toy with his or her eyes",
                    "Turns head to find the person who is talking",
                    "Holds head steady when being picked up to a sitting position",
                    "Brings hands together",
                    "Laughs",
                    "Keeps head steady when held in a sitting position",
                    'Makes sounds like "ga," "ma," or "ba"',
                    "Looks when you call his or her name"
                ]
            },
            {
    "title": "BABY PEDIATRIC SYMPTOM CHECKLIST (BPSC)",
    "description": "These questions are about your child's behavior. Think about what you would expect of other children the same age, and tell us how much each statement applies to your child.",
    "options": ["Not at all", "Somewhat", "Very Much"],
    "subscales": {
        "Social_Adaptability": {
            "name": "Social/Adaptability Issues",
            "questions": [
                "Does your child have a hard time being with new people?",
                "Does your child have a hard time in new places?",
                "Does your child have a hard time with change?",
                "Does your child mind being held by other people?"
            ]
        },
        "Emotional_Regulation": {
            "name": "Emotional Regulation/Irritability",
            "questions": [
                "Does your child cry a lot?",
                "Does your child have a hard time calming down?",
                "Is your child fussy or irritable?",
                "Is it hard to comfort your child?"
            ]
        },
        "Sleep_Routine": {
            "name": "Sleep/Routine Issues",
            "questions": [
                "Is it hard to keep your child on a schedule or routine?",
                "Is it hard to put your child to sleep?",
                "Is it hard to get enough sleep because of your child?",
                "Does your child have trouble staying asleep?"
            ]
        }
    },
    "questions": [
        "Does your child have a hard time being with new people?",
        "Does your child have a hard time in new places?",
        "Does your child have a hard time with change?",
        "Does your child mind being held by other people?",
        "Does your child cry a lot?",
        "Does your child have a hard time calming down?",
        "Is your child fussy or irritable?",
        "Is it hard to comfort your child?",
        "Is it hard to keep your child on a schedule or routine?",
        "Is it hard to put your child to sleep?",
        "Is it hard to get enough sleep because of your child?",
        "Does your child have trouble staying asleep?"
    ]
},
            {
                "title": "PARENT'S CONCERNS",
                "description": "",
                "options": ["Not At All", "Somewhat", "Very Much"],
                "questions": [
                    "Do you have any concerns about your child's learning or development?",
                    "Do you have any concerns about your child's behavior?"
                ]
            }
        ]
    },
    4: {
        "title": "SWYC: 4 months",
        "subtitle": "4 months, 0 days to 5 months, 31 days",
        "version": "V1.08, 9/1/19",
        "sections": [
            {
                "title": "DEVELOPMENTAL MILESTONES",
                "description": "Most children at this age will be able to do some (but not all) of the developmental tasks listed below. Please tell us how much your child is doing each of these things.",
                "options": ["Not Yet", "Somewhat", "Very Much"],
                "questions": [
                    "Holds head steady when being pulled up to a sitting position",
                    "Brings hands together",
                    "Laughs",
                    "Keeps head steady when held in a sitting position",
                    'Makes sounds like "ga," "ma," or "ba"',
                    "Looks when you call his or her name",
                    "Rolls over",
                    "Passes a toy from one hand to the other",
                    "Looks for you or another caregiver when upset",
                    "Holds two objects and bangs them together"
                ]
            },
            {
    "title": "BABY PEDIATRIC SYMPTOM CHECKLIST (BPSC)",
    "description": "These questions are about your child's behavior. Think about what you would expect of other children the same age, and tell us how much each statement applies to your child.",
    "options": ["Not at all", "Somewhat", "Very Much"],
    "subscales": {
        "Social_Adaptability": {
            "name": "Social/Adaptability Issues",
            "questions": [
                "Does your child have a hard time being with new people?",
                "Does your child have a hard time in new places?",
                "Does your child have a hard time with change?",
                "Does your child mind being held by other people?"
            ]
        },
        "Emotional_Regulation": {
            "name": "Emotional Regulation/Irritability",
            "questions": [
                "Does your child cry a lot?",
                "Does your child have a hard time calming down?",
                "Is your child fussy or irritable?",
                "Is it hard to comfort your child?"
            ]
        },
        "Sleep_Routine": {
            "name": "Sleep/Routine Issues",
            "questions": [
                "Is it hard to keep your child on a schedule or routine?",
                "Is it hard to put your child to sleep?",
                "Is it hard to get enough sleep because of your child?",
                "Does your child have trouble staying asleep?"
            ]
        }
    },
    "questions": [
        "Does your child have a hard time being with new people?",
        "Does your child have a hard time in new places?",
        "Does your child have a hard time with change?",
        "Does your child mind being held by other people?",
        "Does your child cry a lot?",
        "Does your child have a hard time calming down?",
        "Is your child fussy or irritable?",
        "Is it hard to comfort your child?",
        "Is it hard to keep your child on a schedule or routine?",
        "Is it hard to put your child to sleep?",
        "Is it hard to get enough sleep because of your child?",
        "Does your child have trouble staying asleep?"
    ]
},
            {
                "title": "PARENT'S CONCERNS",
                "description": "",
                "options": ["Not at all", "Somewhat", "Very Much"],
                "questions": [
                    "Do you have any concerns about your child's learning or development?",
                    "Do you have any concerns about your child's behavior?"
                ]
            }
        ]
    },
    6: {
        "title": "SWYC: 6 months",
        "subtitle": "6 months, 0 days to 8 months, 31 days",
        "version": "V1.08, 9/1/19",
        "sections": [
            {
                "title": "DEVELOPMENTAL MILESTONES",
                "description": "Most children at this age will be able to do some (but not all) of the developmental tasks listed below. Please tell us how much your child is doing each of these things.",
                "options": ["Not Yet", "Somewhat", "Very Much"],
                "questions": [
                    'Makes sounds like "ga," "ma," or "ba"',
                    "Looks when you call his or her name",
                    "Rolls over",
                    "Passes a toy from one hand to the other",
                    "Looks for you or another caregiver when upset",
                    "Holds two objects and bangs them together",
                    "Holds up arms to be picked up",
                    "Gets into a sitting position by him or herself",
                    "Picks up food and eats it",
                    "Pulls up to standing"
                ]
            },
            {
    "title": "BABY PEDIATRIC SYMPTOM CHECKLIST (BPSC)",
    "description": "These questions are about your child's behavior. Think about what you would expect of other children the same age, and tell us how much each statement applies to your child.",
    "options": ["Not at all", "Somewhat", "Very Much"],
    "subscales": {
        "Social_Adaptability": {
            "name": "Social/Adaptability Issues",
            "questions": [
                "Does your child have a hard time being with new people?",
                "Does your child have a hard time in new places?",
                "Does your child have a hard time with change?",
                "Does your child mind being held by other people?"
            ]
        },
        "Emotional_Regulation": {
            "name": "Emotional Regulation/Irritability",
            "questions": [
                "Does your child cry a lot?",
                "Does your child have a hard time calming down?",
                "Is your child fussy or irritable?",
                "Is it hard to comfort your child?"
            ]
        },
        "Sleep_Routine": {
            "name": "Sleep/Routine Issues",
            "questions": [
                "Is it hard to keep your child on a schedule or routine?",
                "Is it hard to put your child to sleep?",
                "Is it hard to get enough sleep because of your child?",
                "Does your child have trouble staying asleep?"
            ]
        }
    },
    "questions": [
        "Does your child have a hard time being with new people?",
        "Does your child have a hard time in new places?",
        "Does your child have a hard time with change?",
        "Does your child mind being held by other people?",
        "Does your child cry a lot?",
        "Does your child have a hard time calming down?",
        "Is your child fussy or irritable?",
        "Is it hard to comfort your child?",
        "Is it hard to keep your child on a schedule or routine?",
        "Is it hard to put your child to sleep?",
        "Is it hard to get enough sleep because of your child?",
        "Does your child have trouble staying asleep?"
    ]
},
            {
                "title": "PARENT'S CONCERNS",
                "description": "",
                "options": ["Not at all", "Somewhat", "Very Much"],
                "questions": [
                    "Do you have any concerns about your child's learning or development?",
                    "Do you have any concerns about your child's behavior?"
                ]
            }
        ]
    },
    9: {
        "title": "SWYC: 9 months",
        "subtitle": "9 months, 0 days to 11 months, 31 days",
        "version": "V1.08, 9/1/19",
        "sections": [
            {
                "title": "DEVELOPMENTAL MILESTONES",
                "description": "Most children at this age will be able to do some (but not all) of the developmental tasks listed below. Please tell us how much your child is doing each of these things.",
                "options": ["Not Yet", "Somewhat", "Very Much"],
                "questions": [
                    "Holds up arms to be picked up",
                    "Gets into a sitting position by him or herself",
                    "Picks up food and eats it",
                    "Pulls up to standing",
                    'Plays games like "peek-a-boo" or "pat-a-cake"',
                    'Calls you "mama" or "dada" or similar name',
                    'Looks around when you say things like "\Where is your bottle?\" or "\Where is your blanket?\"',
                    "Copies sounds that you make",
                    "Walks across a room without help",
                    "Follows directions - like \"Come here\" or \"Give me the ball\""
                ]
            },
            {
    "title": "BABY PEDIATRIC SYMPTOM CHECKLIST (BPSC)",
    "description": "These questions are about your child's behavior. Think about what you would expect of other children the same age, and tell us how much each statement applies to your child.",
    "options": ["Not at all", "Somewhat", "Very Much"],
    "subscales": {
        "Social_Adaptability": {
            "name": "Social/Adaptability Issues",
            "questions": [
                "Does your child have a hard time being with new people?",
                "Does your child have a hard time in new places?",
                "Does your child have a hard time with change?",
                "Does your child mind being held by other people?"
            ]
        },
        "Emotional_Regulation": {
            "name": "Emotional Regulation/Irritability",
            "questions": [
                "Does your child cry a lot?",
                "Does your child have a hard time calming down?",
                "Is your child fussy or irritable?",
                "Is it hard to comfort your child?"
            ]
        },
        "Sleep_Routine": {
            "name": "Sleep/Routine Issues",
            "questions": [
                "Is it hard to keep your child on a schedule or routine?",
                "Is it hard to put your child to sleep?",
                "Is it hard to get enough sleep because of your child?",
                "Does your child have trouble staying asleep?"
            ]
        }
    },
    "questions": [
        "Does your child have a hard time being with new people?",
        "Does your child have a hard time in new places?",
        "Does your child have a hard time with change?",
        "Does your child mind being held by other people?",
        "Does your child cry a lot?",
        "Does your child have a hard time calming down?",
        "Is your child fussy or irritable?",
        "Is it hard to comfort your child?",
        "Is it hard to keep your child on a schedule or routine?",
        "Is it hard to put your child to sleep?",
        "Is it hard to get enough sleep because of your child?",
        "Does your child have trouble staying asleep?"
    ]
},
            {
                "title": "PARENT'S CONCERNS",
                "description": "",
                "options": ["Not At All", "Somewhat", "Very Much"],
                "questions": [
                    "Do you have any concerns about your child's learning or development?",
                    "Do you have any concerns about your child's behavior?"
                ]
            }
        ]
    },
    12: {
        "title": "SWYC: 12 months",
        "subtitle": "12 months, 0 days to 14 months, 31 days",
        "version": "V1.08, 9/1/19",
        "sections": [
            {
                "title": "DEVELOPMENTAL MILESTONES",
                "description": "Most children at this age will be able to do some (but not all) of the developmental tasks listed below. Please tell us how much your child is doing each of these things.",
                "options": ["Not Yet", "Somewhat", "Very Much"],
                "questions": [
                    "Picks up food and eats it",
                    "Pulls up to standing",
                    'Plays games like "peek-a-boo" or "pat-a-cake"',
                    'Calls you "mama" or "dada" or similar name',
                    'Looks around when you say things like "\Where is your bottle?\" or "\Where is your blanket?\"',
                    "Copies sounds that you make",
                    "Walks across a room without help",
                    "Follows directions - like \"Come here\" or \"Give me the ball\"",
                    "Runs",
                    "Walks up stairs with help"
                ]
            },
            {
    "title": "BABY PEDIATRIC SYMPTOM CHECKLIST (BPSC)",
    "description": "These questions are about your child's behavior. Think about what you would expect of other children the same age, and tell us how much each statement applies to your child.",
    "options": ["Not at all", "Somewhat", "Very Much"],
    "subscales": {
        "Social_Adaptability": {
            "name": "Social/Adaptability Issues",
            "questions": [
                "Does your child have a hard time being with new people?",
                "Does your child have a hard time in new places?",
                "Does your child have a hard time with change?",
                "Does your child mind being held by other people?"
            ]
        },
        "Emotional_Regulation": {
            "name": "Emotional Regulation/Irritability",
            "questions": [
                "Does your child cry a lot?",
                "Does your child have a hard time calming down?",
                "Is your child fussy or irritable?",
                "Is it hard to comfort your child?"
            ]
        },
        "Sleep_Routine": {
            "name": "Sleep/Routine Issues",
            "questions": [
                "Is it hard to keep your child on a schedule or routine?",
                "Is it hard to put your child to sleep?",
                "Is it hard to get enough sleep because of your child?",
                "Does your child have trouble staying asleep?"
            ]
        }
    },
    "questions": [
        "Does your child have a hard time being with new people?",
        "Does your child have a hard time in new places?",
        "Does your child have a hard time with change?",
        "Does your child mind being held by other people?",
        "Does your child cry a lot?",
        "Does your child have a hard time calming down?",
        "Is your child fussy or irritable?",
        "Is it hard to comfort your child?",
        "Is it hard to keep your child on a schedule or routine?",
        "Is it hard to put your child to sleep?",
        "Is it hard to get enough sleep because of your child?",
        "Does your child have trouble staying asleep?"
    ]
},
            {
                "title": "PARENT'S CONCERNS",
                "description": "",
                "options": ["Not At All", "Somewhat", "Very Much"],
                "questions": [
                    "Do you have any concerns about your child's learning or development?",
                    "Do you have any concerns about your child's behavior?"
                ]
            }
        ]
    },
    15: {
        "title": "SWYC: 15 months",
        "subtitle": "15 months, 0 days to 17 months, 31 days",
        "version": "V1.08, 9/1/19",
        "sections": [
            {
                "title": "DEVELOPMENTAL MILESTONES",
                "description": "Most children at this age will be able to do some (but not all) of the developmental tasks listed below. Please tell us how much your child is doing each of these things.",
                "options": ["Not Yet", "Somewhat", "Very Much"],
                "questions": [
                    'Calls you "mama" or "dada" or similar name',
                    'Looks around when you say things like "\Where is your bottle?\" or "\Where is your blanket?\"',
                    "Copies sounds that you make",
                    "Walks across a room without help",
                    "Follows directions - like \"Come here\" or \"Give me the ball\"",
                    "Runs",
                    "Walks up stairs with help",
                    "Kicks a ball",
                    "Names at least 5 familiar objects - like ball or milk",
                    "Names at least 5 body parts - like nose, hand, or tummy"
                ]
            },
           {
    "title": "BABY PEDIATRIC SYMPTOM CHECKLIST (BPSC)",
    "description": "These questions are about your child's behavior. Think about what you would expect of other children the same age, and tell us how much each statement applies to your child.",
    "options": ["Not at all", "Somewhat", "Very Much"],
    "subscales": {
        "Social_Adaptability": {
            "name": "Social/Adaptability Issues",
            "questions": [
                "Does your child have a hard time being with new people?",
                "Does your child have a hard time in new places?",
                "Does your child have a hard time with change?",
                "Does your child mind being held by other people?"
            ]
        },
        "Emotional_Regulation": {
            "name": "Emotional Regulation/Irritability",
            "questions": [
                "Does your child cry a lot?",
                "Does your child have a hard time calming down?",
                "Is your child fussy or irritable?",
                "Is it hard to comfort your child?"
            ]
        },
        "Sleep_Routine": {
            "name": "Sleep/Routine Issues",
            "questions": [
                "Is it hard to keep your child on a schedule or routine?",
                "Is it hard to put your child to sleep?",
                "Is it hard to get enough sleep because of your child?",
                "Does your child have trouble staying asleep?"
            ]
        }
    },
    "questions": [
        "Does your child have a hard time being with new people?",
        "Does your child have a hard time in new places?",
        "Does your child have a hard time with change?",
        "Does your child mind being held by other people?",
        "Does your child cry a lot?",
        "Does your child have a hard time calming down?",
        "Is your child fussy or irritable?",
        "Is it hard to comfort your child?",
        "Is it hard to keep your child on a schedule or routine?",
        "Is it hard to put your child to sleep?",
        "Is it hard to get enough sleep because of your child?",
        "Does your child have trouble staying asleep?"
    ]
},
            {
                "title": "PARENT'S CONCERNS",
                "description": "",
                "options": ["Not At All", "Somewhat", "Very Much"],
                "questions": [
                    "Do you have any concerns about your child's learning or development?",
                    "Do you have any concerns about your child's behavior?"
                ]
            }
        ]
    },
    18: {
        "title": "SWYC: 18 months",
        "subtitle": "18 months, 0 days to 22 months, 31 days",
        "version": "V1.08, 9/1/19",
        "sections": [
            {
                "title": "DEVELOPMENTAL MILESTONES",
                "description": "Most children at this age will be able to do some (but not all) of the developmental tasks listed below. Please tell us how much your child is doing each of these things.",
                "options": ["Not Yet", "Somewhat", "Very Much"],
                "questions": [
                    "Runs",
                    "Walks up stairs with help",
                    "Kicks a ball",
                    "Names at least 5 familiar objects - like ball or milk",
                    "Names at least 5 body parts - like nose, hand, or tummy",
                    "Climbs up a ladder at a playground",
                    'Uses words like "me" or "mine"',
                    "Jumps off the ground with two feet",
                    'Puts 2 or more words together - like "more water" or "go outside"',
                    "Uses words to ask for help"
                ]
            },
            {
                "title": "PRESCHOOL PEDIATRIC SYMPTOM CHECKLIST (PPSC)",
                "description": "These questions are about your child's behavior. Think about what you would expect of other children the same age, and tell us how much each statement applies to your child.",
                "options": ["Not at all", "Somewhat", "Very Much"],
                "questions": [
                    "Does your child seem nervous or afraid?",
                    "Does your child seem sad or unhappy?",
                    "Does your child get upset if things are not done in a certain way?",
                    "Does your child have a hard time with change?",
                    "Does your child have trouble playing with other children?",
                    "Does your child break things on purpose?",
                    "Does your child fight with other children?",
                    "Does your child have trouble paying attention?",
                    "Does your child have a hard time calming down?",
                    "Does your child have trouble staying with one activity?",
                    "Is your child aggressive?",
                    "Is your child fidgety or unable to sit still?",
                    "Is your child angry?",
                    "Is it hard to take your child out in public?",
                    "Is it hard to comfort your child?",
                    "Is it hard to know what your child needs?",
                    "Is it hard to keep your child on a schedule or routine?",
                    "Is it hard to get your child to obey you?"
                ]
            },
            {
                "title": "PARENT'S OBSERVATIONS OF SOCIAL INTERACTIONS (POSI)",
                "description": "These questions are about your child's social behavior.",
                "type": "special",
                "questions": [
                    {
                        "text": "Does your child bring things to you to show them to you?",
                        "options": ["Many times a day", "A few times a day", "A few times a week", "Less than once a week", "Never"]
                    },
                    {
                        "text": "Is your child interested in playing with other children?",
                        "options": ["Always", "Usually", "Sometimes", "Rarely", "Never"]
                    },
                    {
                        "text": "When you say a word or wave your hand, will your child try to copy you?",
                        "options": ["Always", "Usually", "Sometimes", "Rarely", "Never"]
                    },
                    {
                        "text": "Does your child look at you when you call his or her name?",
                        "options": ["Always", "Usually", "Sometimes", "Rarely", "Never"]
                    },
                    {
                        "text": "Does your child look if you point to something across the room?",
                        "options": ["Always", "Usually", "Sometimes", "Rarely", "Never"]
                    },
                    {
                        "text": "How does your child usually show you something he or she wants?",
                        "options": ["Says a word for what he or she wants", "Points to it with one finger", "Reaches for it", "Pulls me over or puts my hand on it", "Grunts, cries or screams"]
                    },
                    {
                        "text": "What are your child's favorite play activities?",
                        "type": "checkbox",
                        "options": ["Playing with dolls or stuffed animals", "Reading books with you", "Climbing, running and being active", "Lining up toys or other things", "Watching things go round and round like fans or wheels"]
                    }
                ]
            },
            {
                "title": "PARENT'S CONCERNS",
                "description": "",
                "options": ["Not At All", "Somewhat", "Very Much"],
                "questions": [
                    "Do you have any concerns about your child's learning or development?",
                    "Do you have any concerns about your child's behavior?"
                ]
            }
        ]
    },
    24: {
        "title": "SWYC: 24 months",
        "subtitle": "23 months, 0 days to 28 months, 31 days",
        "version": "V1.08, 9/1/19",
        "sections": [
            {
                "title": "DEVELOPMENTAL MILESTONES",
                "description": "Most children at this age will be able to do some (but not all) of the developmental tasks listed below. Please tell us how much your child is doing each of these things.",
                "options": ["Not Yet", "Somewhat", "Very Much"],
                "questions": [
                    "Names at least 5 body parts - like nose, hand, or tummy",
                    "Climbs up a ladder at a playground",
                    'Uses words like "me" or "mine"',
                    "Jumps off the ground with two feet",
                    'Puts 2 or more words together - like "more water" or "go outside"',
                    "Uses words to ask for help",
                    "Names at least one color",
                    'Tries to get you to watch by saying "Look at me"',
                    "Says his or her first name when asked",
                    "Draws lines"
                ]
            },
            {
                "title": "PRESCHOOL PEDIATRIC SYMPTOM CHECKLIST (PPSC)",
                "description": "These questions are about your child's behavior. Think about what you would expect of other children the same age, and tell us how much each statement applies to your child.",
                "options": ["Not at all", "Somewhat", "Very Much"],
                "questions": [
                    "Does your child seem nervous or afraid?",
                    "Does your child seem sad or unhappy?",
                    "Does your child get upset if things are not done in a certain way?",
                    "Does your child have a hard time with change?",
                    "Does your child have trouble playing with other children?",
                    "Does your child break things on purpose?",
                    "Does your child fight with other children?",
                    "Does your child have trouble paying attention?",
                    "Does your child have a hard time calming down?",
                    "Does your child have trouble staying with one activity?",
                    "Is your child aggressive?",
                    "Is your child fidgety or unable to sit still?",
                    "Is your child angry?",
                    "Is it hard to take your child out in public?",
                    "Is it hard to comfort your child?",
                    "Is it hard to know what your child needs?",
                    "Is it hard to keep your child on a schedule or routine?",
                    "Is it hard to get your child to obey you?"
                ]
            },
            {
                "title": "PARENT'S OBSERVATIONS OF SOCIAL INTERACTIONS (POSI)",
                "description": "These questions are about your child's social behavior.",
                "type": "special",
                "questions": [
                    {
                        "text": "Does your child bring things to you to show them to you?",
                        "options": ["Many times a day", "A few times a day", "A few times a week", "Less than once a week", "Never"]
                    },
                    {
                        "text": "Is your child interested in playing with other children?",
                        "options": ["Always", "Usually", "Sometimes", "Rarely", "Never"]
                    },
                    {
                        "text": "When you say a word or wave your hand, will your child try to copy you?",
                        "options": ["Always", "Usually", "Sometimes", "Rarely", "Never"]
                    },
                    {
                        "text": "Does your child look at you when you call his or her name?",
                        "options": ["Always", "Usually", "Sometimes", "Rarely", "Never"]
                    },
                    {
                        "text": "Does your child look if you point to something across the room?",
                        "options": ["Always", "Usually", "Sometimes", "Rarely", "Never"]
                    },
                    {
                        "text": "How does your child usually show you something he or she wants?",
                        "options": ["Says a word for what he or she wants", "Points to it with one finger", "Reaches for it", "Pulls me over or puts my hand on it", "Grunts, cries or screams"]
                    },
                    {
                        "text": "What are your child's favorite play activities?",
                        "type": "checkbox",
                        "options": ["Playing with dolls or stuffed animals", "Reading books with you", "Climbing, running and being active", "Lining up toys or other things", "Watching things go round and round like fans or wheels"]
                    }
                ]
            },
            {
                "title": "PARENT'S CONCERNS",
                "description": "",
                "options": ["Not At All", "Somewhat", "Very Much"],
                "questions": [
                    "Do you have any concerns about your child's learning or development?",
                    "Do you have any concerns about your child's behavior?"
                ]
            }
        ]
    },
    30: {
        "title": "SWYC: 30 months",
        "subtitle": "29 months, 0 days to 34 months, 31 days",
        "version": "V1.08, 9/1/19",
        "sections": [
            {
                "title": "DEVELOPMENTAL MILESTONES",
                "description": "Most children at this age will be able to do some (but not all) of the developmental tasks listed below. Please tell us how much your child is doing each of these things.",
                "options": ["Not Yet", "Somewhat", "Very Much"],
                "questions": [
                    "Names at least one color",
                    'Tries to get you to watch by saying "Look at me"',
                    "Says his or her first name when asked",
                    "Draws lines",
                    "Talks so other people can understand him or her most of the time",
                    "Washes and dries hands by him or herself (even if you turn on the water)",
                    'Asks questions beginning with "why" or "how" - like "Why no cookie?"',
                    "Explains the reasons for things, like needing a sweater when it's cold",
                    'Compares things - using words like "bigger" or "shorter"',
                    'Answers questions like "What do you do when you are cold?" or "...when you are sleepy?"'
                ]
            },
            {
                "title": "PRESCHOOL PEDIATRIC SYMPTOM CHECKLIST (PPSC)",
                "description": "These questions are about your child's behavior. Think about what you would expect of other children the same age, and tell us how much each statement applies to your child.",
                "options": ["Not at all", "Somewhat", "Very Much"],
                "questions": [
                    "Does your child seem nervous or afraid?",
                    "Does your child seem sad or unhappy?",
                    "Does your child get upset if things are not done in a certain way?",
                    "Does your child have a hard time with change?",
                    "Does your child have trouble playing with other children?",
                    "Does your child break things on purpose?",
                    "Does your child fight with other children?",
                    "Does your child have trouble paying attention?",
                    "Does your child have a hard time calming down?",
                    "Does your child have trouble staying with one activity?",
                    "Is your child aggressive?",
                    "Is your child fidgety or unable to sit still?",
                    "Is your child angry?",
                    "Is it hard to take your child out in public?",
                    "Is it hard to comfort your child?",
                    "Is it hard to know what your child needs?",
                    "Is it hard to keep your child on a schedule or routine?",
                    "Is it hard to get your child to obey you?"
                ]
            },
            {
                "title": "PARENT'S OBSERVATIONS OF SOCIAL INTERACTIONS (POSI)",
                "description": "These questions are about your child's social behavior.",
                "type": "special",
                "questions": [
                    {
                        "text": "Does your child bring things to you to show them to you?",
                        "options": ["Many times a day", "A few times a day", "A few times a week", "Less than once a week", "Never"]
                    },
                    {
                        "text": "Is your child interested in playing with other children?",
                        "options": ["Always", "Usually", "Sometimes", "Rarely", "Never"]
                    },
                    {
                        "text": "When you say a word or wave your hand, will your child try to copy you?",
                        "options": ["Always", "Usually", "Sometimes", "Rarely", "Never"]
                    },
                    {
                        "text": "Does your child look at you when you call his or her name?",
                        "options": ["Always", "Usually", "Sometimes", "Rarely", "Never"]
                    },
                    {
                        "text": "Does your child look if you point to something across the room?",
                        "options": ["Always", "Usually", "Sometimes", "Rarely", "Never"]
                    },
                    {
                        "text": "How does your child usually show you something he or she wants?",
                        "options": ["Says a word for what he or she wants", "Points to it with one finger", "Reaches for it", "Pulls me over or puts my hand on it", "Grunts, cries or screams"]
                    },
                    {
                        "text": "What are your child's favorite play activities?",
                        "type": "checkbox",
                        "options": ["Playing with dolls or stuffed animals", "Reading books with you", "Climbing, running and being active", "Lining up toys or other things", "Watching things go round and round like fans or wheels"]
                    }
                ]
            },
            {
                "title": "PARENT'S CONCERNS",
                "description": "",
                "options": ["Not At All", "Somewhat", "Very Much"],
                "questions": [
                    "Do you have any concerns about your child's learning or development?",
                    "Do you have any concerns about your child's behavior?"
                ]
            }
        ]
    },
    36: {
        "title": "SWYC: 36 months",
        "subtitle": "35 months, 0 days to 46 months, 31 days",
        "version": "V1.08, 9/1/19",
        "sections": [
            {
                "title": "DEVELOPMENTAL MILESTONES",
                "description": "Most children at this age will be able to do some (but not all) of the developmental tasks listed below. Please tell us how much your child is doing each of these things.",
                "options": ["Not Yet", "Somewhat", "Very Much"],
                "questions": [
                    "Talks so other people can understand him or her most of the time",
                    "Washes and dries hands by him or herself (even if you turn on the water)",
                    'Asks questions beginning with "why" or "how" - like "Why no cookie?"',
                    "Explains the reasons for things, like needing a sweater when it's cold",
                    'Compares things - using words like "bigger" or "shorter"',
                    'Answers questions like "What do you do when you are cold?" or "...when you are sleepy?"',
                    "Tells you a story from a book or tv",
                    "Draws simple shapes - like a circle or a square",
                    'Says words like "feet" for more than one foot and "men" for more than one man',
                    'Uses words like "yesterday" and "tomorrow" correctly'
                ]
            },
            {
                "title": "PRESCHOOL PEDIATRIC SYMPTOM CHECKLIST (PPSC)",
                "description": "These questions are about your child's behavior. Think about what you would expect of other children the same age, and tell us how much each statement applies to your child.",
                "options": ["Not at all", "Somewhat", "Very Much"],
                "questions": [
                    "Does your child seem nervous or afraid?",
                    "Does your child seem sad or unhappy?",
                    "Does your child get upset if things are not done in a certain way?",
                    "Does your child have a hard time with change?",
                    "Does your child have trouble playing with other children?",
                    "Does your child break things on purpose?",
                    "Does your child fight with other children?",
                    "Does your child have trouble paying attention?",
                    "Does your child have a hard time calming down?",
                    "Does your child have trouble staying with one activity?",
                    "Is your child aggressive?",
                    "Is your child fidgety or unable to sit still?",
                    "Is your child angry?",
                    "Is it hard to take your child out in public?",
                    "Is it hard to comfort your child?",
                    "Is it hard to know what your child needs?",
                    "Is it hard to keep your child on a schedule or routine?",
                    "Is it hard to get your child to obey you?"
                ]
            },
            {
                "title": "PARENT'S CONCERNS",
                "description": "",
                "options": ["Not At All", "Somewhat", "Very Much"],
                "questions": [
                    "Do you have any concerns about your child's learning or development?",
                    "Do you have any concerns about your child's behavior?"
                ]
            }
        ]
    },
    48: {
        "title": "SWYC: 48 months",
        "subtitle": "47 months, 0 days to 56 months, 31 days",
        "version": "V1.08, 9/1/19",
        "sections": [
            {
                "title": "DEVELOPMENTAL MILESTONES",
                "description": "Most children at this age will be able to do some (but not all) of the developmental tasks listed below. Please tell us how much your child is doing each of these things.",
                "options": ["Not Yet", "Somewhat", "Very Much"],
                "questions": [
                    'Compares things - using words like "bigger" or "shorter"',
                    'Answers questions like "What do you do when you are cold?" or "...when you are sleepy?"',
                    "Tells you a story from a book or tv",
                    "Draws simple shapes - like a circle or a square",
                    'Says words like "feet" for more than one foot and "men" for more than one man',
                    'Uses words like "yesterday" and "tomorrow" correctly',
                    "Stays dry all night",
                    "Follows simple rules when playing a board game or card game",
                    "Prints his or her name",
                    "Draws pictures you recognize"
                ]
            },
            {
                "title": "PRESCHOOL PEDIATRIC SYMPTOM CHECKLIST (PPSC)",
                "description": "These questions are about your child's behavior. Think about what you would expect of other children the same age, and tell us how much each statement applies to your child.",
                "options": ["Not at all", "Somewhat", "Very Much"],
                "questions": [
                    "Does your child seem nervous or afraid?",
                    "Does your child seem sad or unhappy?",
                    "Does your child get upset if things are not done in a certain way?",
                    "Does your child have a hard time with change?",
                    "Does your child have trouble playing with other children?",
                    "Does your child break things on purpose?",
                    "Does your child fight with other children?",
                    "Does your child have trouble paying attention?",
                    "Does your child have a hard time calming down?",
                    "Does your child have trouble staying with one activity?",
                    "Is your child aggressive?",
                    "Is your child fidgety or unable to sit still?",
                    "Is your child angry?",
                    "Is it hard to take your child out in public?",
                    "Is it hard to comfort your child?",
                    "Is it hard to know what your child needs?",
                    "Is it hard to keep your child on a schedule or routine?",
                    "Is it hard to get your child to obey you?"
                ]
            },
            {
                "title": "PARENT'S CONCERNS",
                "description": "",
                "options": ["Not At All", "Somewhat", "Very Much"],
                "questions": [
                    "Do you have any concerns about your child's learning or development?",
                    "Do you have any concerns about your child's behavior?"
                ]
            }
        ]
    },
    60: {
        "title": "SWYC: 60 months",
        "subtitle": "59 months, 0 days to 65 months, 31 days",
        "version": "V1.08, 9/1/19",
        "sections": [
            {
                "title": "DEVELOPMENTAL MILESTONES",
                "description": "Most children at this age will be able to do some (but not all) of the developmental tasks listed below. Please tell us how much your child is doing each of these things.",
                "options": ["Not Yet", "Somewhat", "Very Much"],
                "questions": [
                    "Tells you a story from a book or tv",
                    "Draws simple shapes - like a circle or a square",
                    'Says words like "feet" for more than one foot and "men" for more than one man',
                    'Uses words like "yesterday" and "tomorrow" correctly',
                    "Stays dry all night",
                    "Follows simple rules when playing a board game or card game",
                    "Prints his or her name",
                    "Draws pictures you recognize",
                    "Stays in the lines when coloring",
                    "Names the days of the week in the correct order"
                ]
            },
            {
                "title": "PRESCHOOL PEDIATRIC SYMPTOM CHECKLIST (PPSC)",
                "description": "These questions are about your child's behavior. Think about what you would expect of other children the same age, and tell us how much each statement applies to your child.",
                "options": ["Not at all", "Somewhat", "Very Much"],
                "questions": [
                    "Does your child seem nervous or afraid?",
                    "Does your child seem sad or unhappy?",
                    "Does your child get upset if things are not done in a certain way?",
                    "Does your child have a hard time with change?",
                    "Does your child have trouble playing with other children?",
                    "Does your child break things on purpose?",
                    "Does your child fight with other children?",
                    "Does your child have trouble paying attention?",
                    "Does your child have a hard time calming down?",
                    "Does your child have trouble staying with one activity?",
                    "Is your child aggressive?",
                    "Is your child fidgety or unable to sit still?",
                    "Is your child angry?",
                    "Is it hard to take your child out in public?",
                    "Is it hard to comfort your child?",
                    "Is it hard to know what your child needs?",
                    "Is it hard to keep your child on a schedule or routine?",
                    "Is it hard to get your child to obey you?"
                ]
            },
            {
                "title": "PARENT'S CONCERNS",
                "description": "",
                "options": ["Not At All", "Somewhat", "Very Much"],
                "questions": [
                    "Do you have any concerns about your child's learning or development?",
                    "Do you have any concerns about your child's behavior?"
                ]
            }
        ]
    }
}

# Helper functions for language analysis
def extract_age_from_id_line(file):
    try:
        for line in file.getvalue().decode("utf-8").splitlines():
            if line.startswith("@ID:") and "CHI" in line:
                age_part = line.split("|")[3].strip()
                years, rest = age_part.split(";")
                months = rest.split(".")[0]
                return int(years) * 12 + int(months)
    except Exception:
        return None

def clean_tokens(tokens):
    return [w.lower() for w in tokens if re.match("^[a-zA-Z]+$", w)]

def count_morphemes(word):
    """Enhanced morpheme counting with better linguistic rules"""
    word = word.lower().strip()
    if not word:
        return 0

    # Base count
    morphemes = 1

    # Contractions (don't, can't, I'm, etc.)
    if "'" in word:
        morphemes += 1

    # Past tense -ed
    if word.endswith('ed') and len(word) > 3:
        # Exclude words where 'ed' is part of the root (like 'red', 'bed')
        if word not in ['red', 'bed', 'fed', 'led', 'wed', 'shed', 'bred', 'fled']:
            morphemes += 1

    # Present progressive -ing
    if word.endswith('ing') and len(word) > 4:
        # Exclude words where 'ing' is part of the root (like 'ring', 'king')
        if word not in ['ring', 'king', 'sing', 'wing', 'bring', 'thing', 'string']:
            morphemes += 1

    # Plural -s
    if word.endswith('s') and len(word) > 2:
        # Exclude words where 's' is part of the root
        if not word.endswith('ss') and word not in ['gas', 'yes', 'bus', 'plus']:
            # Simple heuristic: if removing 's' gives a valid word pattern
            root = word[:-1]
            if len(root) > 1:
                morphemes += 1

    # Possessive 's (already handled in contractions)

    # Comparative -er
    if word.endswith('er') and len(word) > 3:
        if word not in ['her', 'per', 'under', 'over', 'after', 'water', 'other']:
            morphemes += 1

    # Superlative -est
    if word.endswith('est') and len(word) > 4:
        if word not in ['best', 'rest', 'test', 'west', 'nest']:
            morphemes += 1

    return morphemes

def enhanced_chat_processor(filepath):
    """Enhanced CHAT file processing with better error handling"""
    try:
        reader = pylangacq.read_chat(filepath)

        chi_utterances = []
        excluded_utterances = []

        for utt in reader.utterances():
            if utt.participant == "CHI":
                utt_text = str(utt).lower()

                # Skip unintelligible or incomplete utterances
                if any(marker in utt_text for marker in ['xxx', 'yyy', '+...', '0']):
                    excluded_utterances.append(('unintelligible', str(utt)))
                    continue

                # Get tokens
                tokens = [token.word for token in utt.tokens if token.word]

                # Skip empty utterances
                if not tokens:
                    excluded_utterances.append(('empty', str(utt)))
                    continue

                # Skip single word interjections
                if len(tokens) == 1 and tokens[0].lower() in ['oh', 'ah', 'um', 'uh', 'mm', 'hmm']:
                    excluded_utterances.append(('interjection', str(utt)))
                    continue

                chi_utterances.append(utt)

        metadata = {
            'total_chi_utterances': len(chi_utterances),
            'excluded_utterances': len(excluded_utterances),
            'transcription_quality': len(chi_utterances) / (len(chi_utterances) + len(excluded_utterances)) if (len(chi_utterances) + len(excluded_utterances)) > 0 else 0
        }

        return chi_utterances, metadata

    except Exception as e:
        raise Exception(f"Error processing CHAT file: {str(e)}")

def calculate_enhanced_mlu(utterances):
    """Calculate morpheme-based MLU"""
    total_morphemes = 0
    total_utterances = 0

    for utt in utterances:
        morpheme_count = 0

        for token in utt.tokens:
            if token.word:
                morphemes = count_morphemes(token.word)
                morpheme_count += morphemes

        if morpheme_count > 0:
            total_morphemes += morpheme_count
            total_utterances += 1

    mlu = total_morphemes / total_utterances if total_utterances > 0 else 0
    return round(mlu, 3)

def calculate_mattr(tokens, window=50):
    """Calculate Moving Average Type-Token Ratio"""
    if len(tokens) < window:
        return round(len(set(tokens)) / len(tokens), 3) if tokens else 0

    scores = []
    for i in range(len(tokens) - window + 1):
        window_tokens = tokens[i:i + window]
        unique = len(set(window_tokens))
        scores.append(unique / window)

    return round(sum(scores) / len(scores), 3)

def calculate_lexical_diversity(utterances):
    """Calculate comprehensive lexical diversity measures"""
    all_words = []

    for utt in utterances:
        for token in utt.tokens:
            if token.word and re.match(r'^[a-zA-Z]+$', token.word):
                all_words.append(token.word.lower())

    if not all_words:
        return {}

    unique_words = set(all_words)
    total_words = len(all_words)

    # Type-Token Ratio
    ttr = len(unique_words) / total_words if total_words > 0 else 0

    # Moving Average TTR
    mattr = calculate_mattr(all_words)

    # Number of Different Words
    ndw = len(unique_words)

    # VocD estimation (simplified)
    vocd = estimate_vocd(all_words)

    return {
        'ttr': round(ttr, 3),
        'mattr': mattr,
        'ndw': ndw,
        'vocd': vocd,
        'total_words': total_words
    }

def estimate_vocd(words):
    """Simplified VocD estimation"""
    if len(words) < 50:
        return None

    # Sample different sizes and calculate average TTR
    sample_sizes = [35, 50] if len(words) < 100 else [35, 50, 75, 100]
    ttrs_by_size = {}

    for size in sample_sizes:
        if len(words) >= size:
            ttrs = []
            # Take multiple random samples
            for _ in range(min(10, len(words) // size)):
                try:
                    sample = random.sample(words, size)
                    ttr = len(set(sample)) / len(sample)
                    ttrs.append(ttr)
                except:
                    continue

            if ttrs:
                ttrs_by_size[size] = sum(ttrs) / len(ttrs)

    if ttrs_by_size:
        avg_ttr = sum(ttrs_by_size.values()) / len(ttrs_by_size)
        return round(avg_ttr * 100, 1)

    return None

def calculate_syntactic_complexity(utterances):
    """Enhanced syntactic complexity calculation - BACKWARD COMPATIBLE"""
    complex_sentences = 0
    total_utterances = len(utterances)
    
    # Enhanced complexity indicators
    subordinating_conj = {
        'because', 'when', 'if', 'while', 'since', 'although', 'though', 
        'before', 'after', 'until', 'unless', 'whereas', 'whenever'
    }
    coordinating_conj = {'and', 'but', 'or', 'so', 'yet', 'nor'}
    relative_pronouns = {'who', 'which', 'that', 'where', 'whose'}
    complement_markers = {'that', 'what', 'how', 'why', 'whether'}
    
    # Store detailed results for potential future use
    complexity_details = {
        'subordination_count': 0,
        'relative_clause_count': 0,
        'complement_count': 0,
        'coordination_count': 0
    }
    
    for utt in utterances:
        words = [token.word.lower() for token in utt.tokens if token.word and token.word.isalpha()]
        
        if len(words) == 0:
            continue
            
        # Check for complexity indicators
        has_subordination = any(conj in words for conj in subordinating_conj)
        has_relative_clause = any(pron in words for pron in relative_pronouns)
        has_complement = any(marker in words for marker in complement_markers)
        has_coordination = any(conj in words for conj in coordinating_conj) and len(words) > 5
        is_long_complex = len(words) > 10  # More conservative length threshold
        
        # Count occurrences for detailed analysis
        if has_subordination:
            complexity_details['subordination_count'] += 1
        if has_relative_clause:
            complexity_details['relative_clause_count'] += 1
        if has_complement:
            complexity_details['complement_count'] += 1
        if has_coordination:
            complexity_details['coordination_count'] += 1
        
        # Consider complex if has structural complexity OR is very long
        if has_subordination or has_relative_clause or has_complement or has_coordination or is_long_complex:
            complex_sentences += 1
    
    complex_ratio = complex_sentences / total_utterances if total_utterances > 0 else 0
    
    # Store additional details in a way that won't break existing code
    if hasattr(calculate_syntactic_complexity, 'last_details'):
        calculate_syntactic_complexity.last_details = complexity_details
    
    return round(complex_ratio, 3)

def get_detailed_complexity_analysis(utterances):
    """Get detailed complexity breakdown - call after calculate_syntactic_complexity"""
    # First call the main function to populate details
    basic_ratio = calculate_syntactic_complexity(utterances)
    
    # Get the detailed breakdown
    details = getattr(calculate_syntactic_complexity, 'last_details', {})
    total_utterances = len(utterances)
    
    if total_utterances == 0:
        return {
            'complex_ratio': 0,
            'subordination_ratio': 0,
            'relative_clause_ratio': 0,
            'complement_ratio': 0,
            'coordination_ratio': 0,
            'breakdown': "No utterances to analyze"
        }
    
    return {
        'complex_ratio': basic_ratio,
        'subordination_ratio': round(details.get('subordination_count', 0) / total_utterances, 3),
        'relative_clause_ratio': round(details.get('relative_clause_count', 0) / total_utterances, 3),
        'complement_ratio': round(details.get('complement_count', 0) / total_utterances, 3),
        'coordination_ratio': round(details.get('coordination_count', 0) / total_utterances, 3),
        'breakdown': f"Subordination: {details.get('subordination_count', 0)}, "
                    f"Relative: {details.get('relative_clause_count', 0)}, "
                    f"Complement: {details.get('complement_count', 0)}, "
                    f"Coordination: {details.get('coordination_count', 0)}"
    }
def assess_parameter_status(value, norm_range, parameter_name):
    """Assess if a parameter value is normal or below expectations"""
    if value is None:
        return "❓ Unable to assess"

    min_norm, max_norm = norm_range

    if value >= min_norm:
        return "✅ Normal"
    else:
        return "⬇️ Below"

def assess_sample_adequacy(utterance_count, min_required):
    """Assess if sample size is adequate for analysis"""
    if utterance_count >= min_required:
        return "✅ Adequate"
    elif utterance_count >= min_required * 0.7:
        return "⚠️ Borderline"
    else:
        return "❌ Inadequate"

def process_uploaded_files(uploaded_files):
    """Enhanced file processing with comprehensive language analysis"""
    results = []

    for file in uploaded_files:
        try:
            if not file.name.endswith(".cha"):
                results.append({"File": file.name, "Error": "❌ Not a .cha file"})
                continue

            # Extract age
            age_months = extract_age_from_id_line(file)
            if age_months is None:
                results.append({"File": file.name, "Error": "❌ Age not found in @ID line"})
                continue

            # Find appropriate norm group
            group = next((g for g, v in norms.items() if v["min"] <= age_months <= v["max"]), None)
            if group is None:
                results.append({"File": file.name, "Error": f"⚠️ Age {age_months} not in supported range (17-60 months)"})
                continue

            # Process file
            temp_path = f"/tmp/{file.name}"
            with open(temp_path, "wb") as f:
                f.write(file.getvalue())

            # Enhanced processing
            chi_utts, metadata = enhanced_chat_processor(temp_path)

            if not chi_utts:
                results.append({"File": file.name, "Error": "⚠️ No valid CHI utterances found"})
                continue

            # Get norms for this age group
            age_norms = norms[group]

            # Calculate all language measures
            mlu_morphemes = calculate_enhanced_mlu(chi_utts)
            lexical_measures = calculate_lexical_diversity(chi_utts)
            complex_ratio = calculate_syntactic_complexity(chi_utts)
            detailed_complexity = get_detailed_complexity_analysis(chi_utts)

            # Extract individual measures
            mattr = lexical_measures.get('mattr', 0)
            ndw = lexical_measures.get('ndw', 0)
            ttr = lexical_measures.get('ttr', 0)
            vocd = lexical_measures.get('vocd', None)
            total_utterances = len(chi_utts)

            # Assess each parameter
            mlu_status = assess_parameter_status(mlu_morphemes, age_norms["mlu_morphemes"], "MLU")
            mattr_status = assess_parameter_status(mattr, age_norms["mattr"], "MATTR")
            ndw_status = assess_parameter_status(ndw, age_norms["ndw"], "NDW")
            ttr_status = assess_parameter_status(ttr, age_norms["ttr"], "TTR")
            complex_status = assess_parameter_status(complex_ratio, age_norms["complex_ratio"], "Complex Ratio")
            vocd_status = assess_parameter_status(vocd, age_norms["vocd"], "VocD") if vocd else "❓ N/A"
            sample_adequacy = assess_sample_adequacy(total_utterances, age_norms["min_utterances"])

            # Overall risk assessment
            risk_indicators = []
            if "⬇️ Below" in mlu_status:
                risk_indicators.append("MLU")
            if "⬇️ Below" in mattr_status:
                risk_indicators.append("MATTR")
            if "⬇️ Below" in ndw_status:
                risk_indicators.append("NDW")
            if "⬇️ Below" in ttr_status:
                risk_indicators.append("TTR")
            if "⬇️ Below" in complex_status:
                risk_indicators.append("Syntax")

            if len(risk_indicators) >= 2:
                overall_risk = f"⚠️ At Risk ({len(risk_indicators)} areas)"
            elif len(risk_indicators) == 1:
                overall_risk = f"⚠️ Monitor ({risk_indicators[0]})"
            else:
                overall_risk = "✅ No concerns"

            results.append({
                "File": file.name,
                "Age (months)": age_months,
                "Group": group,
                "Total Utterances": total_utterances,
                "Sample Quality": sample_adequacy,
                "MLU (Morphemes)": mlu_morphemes,
                "MLU Status": mlu_status,
                "MATTR": mattr,
                "MATTR Status": mattr_status,
                "NDW": ndw,
                "NDW Status": ndw_status,
                "TTR": ttr,
                "TTR Status": ttr_status,
                "Complex Ratio": f"{complex_ratio:.1%}",
                "Complex Status": complex_status,
                "Subordination Ratio": f"{detailed_complexity['subordination_ratio']:.1%}",
                "Relative Clauses": f"{detailed_complexity['relative_clause_ratio']:.1%}",
                "Complexity Breakdown": detailed_complexity['breakdown'],
                "VocD": vocd if vocd else "N/A",
                "VocD Status": vocd_status,
                "Overall Assessment": overall_risk,
                "Transcription Quality": f"{metadata['transcription_quality']:.1%}",
                "Error": ""
            })

        except Exception as e:
            results.append({"File": file.name, "Error": f"❌ {str(e)}"})

    return pd.DataFrame(results)

def reset_questionnaire():
    """Reset questionnaire to start over"""
    st.session_state.current_section = 0
    st.session_state.current_question = 0
    st.session_state.responses = {}
    st.session_state.section_completed = {}

def get_developmental_milestones_thresholds():
    """Get developmental milestones scoring thresholds based on age"""
    return {
        4: {4: 13, 5: 15},
        6: {6: 11, 7: 14, 8: 16},
        9: {9: 11, 10: 13, 11: 14},
        12: {12: 12, 13: 13, 14: 14},
        15: {15: 10, 16: 12, 17: 13},
        18: {18: 8, 19: 10, 20: 11, 21: 13, 22: 14},
        24: {23: 10, 24: 11, 25: 12, 26: 13, 27: 14, 28: 15},
        30: {29: 9, 30: 10, 31: 11, 32: 12, 33: 13, 34: 13},
        36: {35: 10, 36: 11, 37: 12, 38: 13, 39: 13, 40: 14, 41: 14, 42: 15, 43: 15, 44: 16, 45: 16, 46: 16},
        48: {47: 12, 48: 13, 49: 13, 50: 13, 51: 14, 52: 14, 53: 14, 54: 15, 55: 15, 56: 15, 57: 15, 58: 16}
    }

def calculate_exact_age_in_months(birth_date, assessment_date):
    """Calculate exact age in months more precisely"""
    years_diff = assessment_date.year - birth_date.year
    months_diff = assessment_date.month - birth_date.month

    # Adjust for day of month
    if assessment_date.day < birth_date.day:
        months_diff -= 1

    total_months = years_diff * 12 + months_diff
    return total_months

def get_threshold_for_age(questionnaire_age, exact_age_months):
    """Get the appropriate threshold for a specific age"""
    thresholds = get_developmental_milestones_thresholds()

    if questionnaire_age not in thresholds:
        return None

    age_thresholds = thresholds[questionnaire_age]

    # Find the exact age or closest age in the threshold table
    if exact_age_months in age_thresholds:
        return age_thresholds[exact_age_months]

    # If exact age not found, find the closest age within the questionnaire range
    available_ages = sorted(age_thresholds.keys())
    closest_age = min(available_ages, key=lambda x: abs(x - exact_age_months))
    return age_thresholds[closest_age]

def calculate_questionnaire_scores(responses, questionnaire_age=None, exact_age_months=None):
    """Calculate scores for the questionnaire responses with proper BPSC, PPSC, and POSI scoring"""
    scores = {}

    # Group responses by section
    sections_data = {}
    for key, response_data in responses.items():
        section_idx = response_data["section"]
        if section_idx not in sections_data:
            sections_data[section_idx] = []
        sections_data[section_idx].append(response_data)

    # Get the actual questionnaire data to get section titles
    if questionnaire_age and questionnaire_age in questionnaire_data:
        questionnaire = questionnaire_data[questionnaire_age]
        section_titles = [section["title"] for section in questionnaire["sections"]]
    else:
        section_titles = ["Section 0", "Section 1", "Section 2", "Section 3"]

    # Calculate scores for each section
    for section_idx, responses_list in sections_data.items():
        if section_idx < len(section_titles):
            section_name = section_titles[section_idx]
        else:
            section_name = f"Section {section_idx}"

        scores[section_name] = {"raw_score": 0, "total_questions": len(responses_list)}

        # Special handling for different section types
        if "BABY PEDIATRIC SYMPTOM CHECKLIST" in section_name or "BPSC" in section_name:
            # BPSC Scoring
            scores[section_name] = calculate_bpsc_scores(responses_list, questionnaire_age)

        elif "PRESCHOOL PEDIATRIC SYMPTOM CHECKLIST" in section_name or "PPSC" in section_name:
            # PPSC Scoring
            scores[section_name] = calculate_ppsc_scores(responses_list)

        elif "PARENT'S OBSERVATIONS OF SOCIAL INTERACTIONS" in section_name or "POSI" in section_name:
            # POSI Scoring
            scores[section_name] = calculate_posi_scores(responses_list)

        else:
            # Standard scoring for developmental milestones and other sections
            for response_data in responses_list:
                response = response_data["response"]

                # Scoring for developmental milestones (first section, index 0)
                if section_idx == 0:  # First section is developmental milestones
                    if response == "Very Much":
                        scores[section_name]["raw_score"] += 2
                    elif response == "Somewhat":
                        scores[section_name]["raw_score"] += 1
                    # "Not Yet" = 0 points
                else:
                    # Scoring for other sections
                    if response in ["Very Much", "Always"]:
                        scores[section_name]["raw_score"] += 2
                    elif response in ["Somewhat", "Usually"]:
                        scores[section_name]["raw_score"] += 1
                    elif response in ["Sometimes"]:
                        scores[section_name]["raw_score"] += 0.5

    # Add developmental milestones assessment (for the first section)
    if questionnaire_age and exact_age_months and len(section_titles) > 0:
        first_section_name = section_titles[0]
        if first_section_name in scores and "DEVELOPMENTAL MILESTONES" in first_section_name:
            dm_score = scores[first_section_name]["raw_score"]
            threshold = get_threshold_for_age(questionnaire_age, exact_age_months)

            if threshold is not None:
                if questionnaire_age == 2 or questionnaire_age == 60:
                    assessment = "No cut scores available"
                else:
                    if dm_score <= threshold:
                        assessment = "⚠️ Needs Review"
                    else:
                        assessment = "✅ Appears to meet age expectations"

                scores[first_section_name]["threshold"] = threshold
                scores[first_section_name]["assessment"] = assessment
            else:
                scores[first_section_name]["assessment"] = "Assessment not available"

    return scores

def calculate_bpsc_scores(responses_list, questionnaire_age):
    """Calculate BPSC scores with subscales"""
    # Get subscale information from questionnaire data
    if questionnaire_age and questionnaire_age in questionnaire_data:
        questionnaire = questionnaire_data[questionnaire_age]
        # Find BPSC section
        bpsc_section = None
        for section in questionnaire["sections"]:
            if "BABY PEDIATRIC SYMPTOM CHECKLIST" in section["title"]:
                bpsc_section = section
                break

        if bpsc_section and "subscales" in bpsc_section:
            subscales = bpsc_section["subscales"]

            # Initialize subscale scores
            subscale_scores = {}
            for subscale_key, subscale_info in subscales.items():
                subscale_scores[subscale_key] = {
                    "name": subscale_info["name"],
                    "score": 0,
                    "questions": subscale_info["questions"]
                }

            # Score each response
            total_score = 0
            for i, response_data in enumerate(responses_list):
                response = response_data["response"]
                question_text = response_data["question"]

                # Assign score based on response
                question_score = 0
                if response == "Very Much":
                    question_score = 2
                elif response == "Somewhat":
                    question_score = 1
                # "Not at All" = 0

                total_score += question_score

                # Find which subscale this question belongs to
                for subscale_key, subscale_info in subscales.items():
                    if question_text in subscale_info["questions"]:
                        subscale_scores[subscale_key]["score"] += question_score
                        break

            # Determine risk status for each subscale
            at_risk_subscales = []
            for subscale_key, subscale_data in subscale_scores.items():
                if subscale_data["score"] >= 3:  # BPSC threshold is 3 or more
                    at_risk_subscales.append(subscale_data["name"])

            # Overall assessment
            if at_risk_subscales:
                assessment = f"⚠️ At Risk - Subscales: {', '.join(at_risk_subscales)}"
                risk_status = "At Risk"
            else:
                assessment = "✅ Not At Risk"
                risk_status = "Not At Risk"

            return {
                "raw_score": total_score,
                "total_questions": len(responses_list),
                "subscale_scores": subscale_scores,
                "at_risk_subscales": at_risk_subscales,
                "assessment": assessment,
                "risk_status": risk_status,
                "scoring_method": "BPSC",
                "threshold": 3,
                "threshold_description": "3+ on any subscale indicates at risk"
            }

    # Fallback if subscale info not available
    total_score = 0
    for response_data in responses_list:
        response = response_data["response"]
        if response == "Very Much":
            total_score += 2
        elif response == "Somewhat":
            total_score += 1

    return {
        "raw_score": total_score,
        "total_questions": len(responses_list),
        "assessment": "BPSC scoring - subscale info not available",
        "scoring_method": "BPSC"
    }

def calculate_ppsc_scores(responses_list):
    """Calculate PPSC total score"""
    total_score = 0

    for response_data in responses_list:
        response = response_data["response"]
        if response == "Very Much":
            total_score += 2
        elif response == "Somewhat":
            total_score += 1
        # "Not at All" = 0

    # PPSC assessment
    if total_score >= 9:
        assessment = "⚠️ At Risk - Further evaluation needed"
        risk_status = "At Risk"
    else:
        assessment = "✅ Not At Risk"
        risk_status = "Not At Risk"

    return {
        "raw_score": total_score,
        "total_questions": len(responses_list),
        "assessment": assessment,
        "risk_status": risk_status,
        "scoring_method": "PPSC",
        "threshold": 9,
        "threshold_description": "Total score of 9+ indicates at risk"
    }

def calculate_posi_scores(responses_list):
    """Calculate POSI scores using binary scoring based on last three columns"""
    total_score = 0

    # Define the last three columns for each question type
    # For POSI, responses in the last 3 columns indicate concern
    last_three_columns = ["Sometimes", "Rarely", "Never"]
    concerning_responses = ["Pulls me over or puts my hand on it", "Grunts, cries or screams"]  # For question 6
    concerning_play_activities = ["Lining up toys or other things", "Watching things go round and round like fans or wheels"]  # For checkbox question

    for response_data in responses_list:
        response = response_data["response"]
        question_text = response_data["question"]

        question_score = 0

        # Check if response falls in concerning categories
        if any(concerning in response for concerning in last_three_columns):
            question_score = 1
        elif any(concerning in response for concerning in concerning_responses):
            question_score = 1
        elif any(concerning in response for concerning in concerning_play_activities):
            question_score = 1
        elif response in ["Less than once a week", "Never", "Rarely"]:
            question_score = 1

        total_score += question_score

    # POSI assessment
    if total_score >= 3:
        assessment = "⚠️ At Risk - Further evaluation needed"
        risk_status = "At Risk"
    else:
        assessment = "✅ Not At Risk"
        risk_status = "Not At Risk"

    return {
        "raw_score": total_score,
        "total_questions": len(responses_list),
        "max_score": 7,  # POSI has 7 questions maximum
        "assessment": assessment,
        "risk_status": risk_status,
        "scoring_method": "POSI",
        "threshold": 3,
        "threshold_description": "3+ points in last three columns indicates at risk"
    }

def get_available_questionnaires():
    """Get list of available questionnaire ages"""
    return sorted(questionnaire_data.keys())

def find_closest_questionnaire(age_months):
    """Find the closest available questionnaire for a given age"""
    available_ages = get_available_questionnaires()

    # Find exact match first
    if age_months in available_ages:
        return age_months

    # Find closest age
    closest_age = min(available_ages, key=lambda x: abs(x - age_months))
    return closest_age

def handle_answer_selection(response_key, question, response, current_section_idx, current_question_idx, current_section):
    """Handle answer selection and progression logic"""
    st.session_state.responses[response_key] = {
        "question": question,
        "response": response,
        "section": current_section_idx
    }

    # Move to next question
    if current_question_idx + 1 < len(current_section["questions"]):
        st.session_state.current_question += 1
    else:
        # Move to next section
        st.session_state.current_section += 1
        st.session_state.current_question = 0
        st.session_state.section_completed[current_section_idx] = True

def render_standard_question(question, options, response_key, current_section_idx, current_question_idx, current_section):
    """Render standard question with multiple options"""
    # Display question with beautiful styling
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #8b5cf6, #a855f7); padding: 50px; border-radius: 20px; margin: 40px 0; box-shadow: 0 10px 40px rgba(139, 92, 246, 0.4); border: 1px solid rgba(255, 255, 255, 0.2); text-align: center;">
        <div style="color: white; font-size: 28px; font-weight: 700; text-shadow: 2px 2px 8px rgba(0,0,0,0.3); line-height: 1.4; margin: 0; text-align: center;">
            {question}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Answer buttons
    st.markdown("### Choose your answer:")

    # Create columns based on number of options
    if len(options) == 3:
        col1, col2, col3 = st.columns(3)
        cols = [col1, col2, col3]
    elif len(options) == 5:
        col1, col2, col3, col4, col5 = st.columns(5)
        cols = [col1, col2, col3, col4, col5]
    else:
        # Handle any number of options dynamically
        cols = st.columns(len(options))

    for idx, option in enumerate(options):
        with cols[idx]:
            if st.button(f"🔘 {option}", key=f"btn{idx+1}_{response_key}", use_container_width=True):
                handle_answer_selection(response_key, question, option, current_section_idx, current_question_idx, current_section)
                st.markdown(f'<div class="success-box">✅ Selected: {option}</div>', unsafe_allow_html=True)
                st.rerun()

def render_special_question(question_data, response_key, current_section_idx, current_question_idx, current_section):
    """Render special questions like POSI with varying option counts"""
    question = question_data["text"]
    options = question_data["options"]

    # Handle checkbox type questions
    if question_data.get("type") == "checkbox":
        # Display question
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #8b5cf6, #a855f7); padding: 50px; border-radius: 20px; margin: 40px 0; box-shadow: 0 10px 40px rgba(139, 92, 246, 0.4); border: 1px solid rgba(255, 255, 255, 0.2); text-align: center;">
            <div style="color: white; font-size: 28px; font-weight: 700; text-shadow: 2px 2px 8px rgba(0,0,0,0.3); line-height: 1.4; margin: 0; text-align: center;">
                {question}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Select all that apply:")
        st.markdown('<div class="checkbox-section">', unsafe_allow_html=True)

        selected_options = []
        for option in options:
            if st.checkbox(option, key=f"checkbox_{option}_{response_key}"):
                selected_options.append(option)

        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("Continue", key=f"continue_{response_key}", use_container_width=True):
            response = ", ".join(selected_options) if selected_options else "None selected"
            handle_answer_selection(response_key, question, response, current_section_idx, current_question_idx, current_section)
            st.markdown(f'<div class="success-box">✅ Selected: {response}</div>', unsafe_allow_html=True)
            st.rerun()
    else:
        # Regular special question with multiple options - render directly here
        # Display question with beautiful styling
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #8b5cf6, #a855f7); padding: 50px; border-radius: 20px; margin: 40px 0; box-shadow: 0 10px 40px rgba(139, 92, 246, 0.4); border: 1px solid rgba(255, 255, 255, 0.2); text-align: center;">
    <div style="color: white; font-size: 28px; font-weight: 700; text-shadow: 2px 2px 8px rgba(0,0,0,0.3); line-height: 1.4; margin: 0; text-align: center;">
        {question}
    </div>
</div>
""", unsafe_allow_html=True)

        # Answer buttons
        st.markdown("### Choose your answer:")

        # Create columns based on number of options
        if len(options) == 3:
            col1, col2, col3 = st.columns(3)
            cols = [col1, col2, col3]
        elif len(options) == 5:
            col1, col2, col3, col4, col5 = st.columns(5)
            cols = [col1, col2, col3, col4, col5]
        else:
            # Handle any number of options dynamically
            cols = st.columns(len(options))

        for idx, option in enumerate(options):
            with cols[idx]:
                if st.button(f"🔘 {option}", key=f"btn{idx+1}_{response_key}", use_container_width=True):
                    handle_answer_selection(response_key, question, option, current_section_idx, current_question_idx, current_section)
                    st.markdown(f'<div class="success-box">✅ Selected: {option}</div>', unsafe_allow_html=True)
                    st.rerun()

def get_current_question_data(current_section, current_question_idx):
    """Get current question data handling both regular and special question formats"""
    question = current_section["questions"][current_question_idx]

    # Check if this is a special section with dictionary-style questions
    if current_section.get("type") == "special" and isinstance(question, dict):
        return question["text"], question.get("options", []), question
    else:
        # Regular question (string format)
        return question, current_section.get("options", []), None

def go_to_language_analysis():
    st.session_state.current_page = "language_analysis"
    st.rerun()

def go_to_questionnaire():
    st.session_state.current_page = "questionnaire"
    st.rerun()

def go_to_landing():
    st.session_state.current_page = "landing"
    st.rerun()

# Landing Page
if st.session_state.current_page == "landing":
    # Header
    st.markdown("""
<div class="main-header">
    <div class="logo-container">
    <span style="font-size: 48px;">💜</span>
        <div>
            <h1 class="logo-text" style="color: #8B5CF6; margin-bottom: 5px; font size: 48px">Thryve</h1>
            <p style="color: #A855F7; font-size: 14px; font-weight: 400; letter-spacing: 2px; margin: 0; font-family: Arial, sans-serif;">FOR BRILLIANT MINDS</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

    # Hero Section
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("""
        <div class="hero-section">
            <h1 class="hero-title">
                AI-Powered Child<br>
                <span class="highlight">Development</span>
            </h1>
            <p class="hero-subtitle">
                Track milestones, analyze speech development, and support brilliant minds with cutting-edge AI technology designed for parents and caregivers.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Start Tracking Today", key="hero_cta"):
            go_to_questionnaire()

    with col2:
        st.markdown("""
        <div class="hero-illustration">
    <img src="https://avaceod.com/images/studentTest.jpg"
         style="max-width: 100%; height: auto; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.2);"
         alt="Child Development">
    <!-- keep the progress badge if you want -->
    <div class="progress-badge">
        <div class="progress-icon">📈</div>
        <div>
            <div class="progress-text">Progress Tracking</div>
            <div class="progress-subtext">Real-time insights</div>
        </div>
    </div>
</div>
        """, unsafe_allow_html=True)

    # Features Section

        st.markdown("""
<div style="width: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 100px 0;">
<h2 style="font-size: 60px; font-weight: 700; color: #1f2937; margin-bottom: 16px; text-align: center; width: 100%; margin-left: auto; margin-right: auto;">
Comprehensive Development Support
</h2>
<p style="font-size: 28px; color: #6b7280; margin-bottom: 60px; max-width: 800px; text-align: center; width: 100%; margin-left: auto; margin-right: auto;">
Everything you need to monitor and support your child's growth with AI-powered insights
</p>
</div>
""", unsafe_allow_html=True)

    # Feature Cards
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📈</div>
            <h3 class="feature-title">Milestone Tracking</h3>
            <p class="feature-description" style="font-size: 18px; margin-bottom: 30px;">
                Monitor developmental milestones with AI-powered assessments and personalized recommendations.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Learn more →", key="milestone_btn"):
            go_to_questionnaire()

    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎤</div>
            <h3 class="feature-title">Speech Analysis</h3>
            <p class="feature-description" style="font-size: 18px; margin-bottom: 30px;">
        Advanced voice recording analysis to detect speech delays and communication patterns.
           </p>
       </div>
       """, unsafe_allow_html=True)
        
        if st.button("Learn more →", key="speech_btn"):
            go_to_language_analysis()

# Language Analysis Page - NEW DESIGN
elif st.session_state.current_page == "language_analysis":
    # Top navigation bar
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    with col1:
        if st.button("← Back to Home", key="back_lang"):
            go_to_landing()

    # Page header
    st.markdown("""
    <div style="text-align: center; margin: 60px 0 40px 0;">
        <h1 style="font-size: 60px; font-weight: 700; color: #1f2937; margin-bottom: 16px;">
            Recording Analysis
        </h1>
        <p style="font-size: 28px; color: #6b7280; max-width: 600px; margin: 0 auto;">
            Upload .cha files to analyze speech development
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Main upload section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #c1adf0, #a855f7); padding: 40px; border-radius: 20px; margin: 40px 0; color: white;">
        <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 12px;">
            <div style="font-size: 24px;">📄</div>
            <h2 style="margin: 0; font-size: 28px; font-weight: 700;">.CHA File Analysis</h2>
        </div>
        <p style="margin: 0; opacity: 0.9; font-size: 16px;">Upload transcription files for speech analysis</p>
    </div>
    """, unsafe_allow_html=True)

    # File upload area with custom styling
    st.markdown("""
    <div style="background: white; border: 2px dashed #d1d5db; border-radius: 16px; padding: 60px; text-align: center; margin: 30px 0;">
        <div style="font-size: 48px; color: #9ca3af; margin-bottom: 20px;">
            ⬆
        </div>
        <h3 style="color: #1f2937; font-size: 50px; font-weight: 600; margin-bottom: 8px;">
            Upload .CHA File
        </h3>
        <p style="color: #6b7280; margin-bottom: 40px;">
            Drag and drop your .cha transcription file here, or click to browse
        </p>
    </div>
    """, unsafe_allow_html=True)

    # File uploader (this will appear below the custom area)
    uploaded_files = st.file_uploader("", type=["cha"], accept_multiple_files=True, label_visibility="collapsed")

    # Choose File button styling
    st.markdown("""
    <div style="text-align: center; margin: -20px 0 40px 0;">
        <style>
        .stFileUploader button {
            background: linear-gradient(135deg, #c1adf0, #a855f7) !important;
            color: white !important;
            border: none !important;
            padding: 12px 24px !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
        }
        </style>
    </div>
    """, unsafe_allow_html=True)

    if uploaded_files:
        if st.button("📊 Analyze Files", type="primary", use_container_width=True):
            df = process_uploaded_files(uploaded_files)
            st.session_state.results_df = df

    # Information cards section
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="background: white; padding: 30px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); margin: 20px 0;">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 20px;">
                <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #c1adf0, #a855f7); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 20px;">
                    📄
                </div>
                <h3 style="margin: 0; color: #1f2937; font-size: 20px; font-weight: 600;">.CHA File Format</h3>
            </div>
            <div style="space-y: 12px;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                    <div style="width: 8px; height: 8px; background: #c1adf0; border-radius: 50%;"></div>
                    <span style="color: #374151;">CHAT format (Codes for the Human Analysis of Transcripts)</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                    <div style="width: 8px; height: 8px; background: #c1adf0; border-radius: 50%;"></div>
                    <span style="color: #374151;">Timestamped conversation transcripts</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                    <div style="width: 8px; height: 8px; background: #c1adf0; border-radius: 50%;"></div>
                    <span style="color: #374151;">Include both child and caregiver speech</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div style="width: 8px; height: 8px; background: #c1adf0; border-radius: 50%;"></div>
                    <span style="color: #374151;">Proper speaker identification required</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: white; padding: 30px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); margin: 20px 0;">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 20px;">
                <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #c1adf0, #a855f7); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 20px;">
                    📈
                </div>
                <h3 style="margin: 0; color: #1f2937; font-size: 20px; font-weight: 600;">What We Analyze</h3>
            </div>
            <div style="space-y: 12px;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                    <div style="width: 8px; height: 8px; background: #c1adf0; border-radius: 50%;"></div>
                    <span style="color: #374151;">Vocabulary growth and word usage</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                    <div style="width: 8px; height: 8px; background: #c1adf0; border-radius: 50%;"></div>
                    <span style="color: #374151;">Sentence structure and complexity</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                    <div style="width: 8px; height: 8px; background: #c1adf0; border-radius: 50%;"></div>
                    <span style="color: #374151;">Speech delay risk assessment</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div style="width: 8px; height: 8px; background: ##c1adf0; border-radius: 50%;"></div>
                    <span style="color: #374151;">Developmental milestone tracking</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Recent Analysis Sessions section
    st.markdown("""
    <div style="margin: 60px 0 30px 0;">
        <h2 style="color: #1f2937; font-size: 32px; font-weight: 700; margin-bottom: 8px;">Recent Analysis Sessions</h2>
        <p style="color: #6b7280; font-size: 16px;">Previous .cha file analysis results</p>
    </div>
    """, unsafe_allow_html=True)

    # Sample recent sessions (you can replace this with actual data)
    if st.session_state.results_df is not None and not st.session_state.results_df.empty:
        # Show actual results
        for index, row in st.session_state.results_df.iterrows():
            # Determine status color and text
            if row.get('Error', ''):
                status_color = "#ef4444"
                status_text = "Error"
                status_bg = "#fee2e2"
            elif "⬇️ Below" in str(row.get('MLU Status', '')) or "⬇️ Below" in str(row.get('MATTR Status', '')):
                status_color = "#f59e0b"
                status_text = "At Risk"
                status_bg = "#fef3c7"
            else:
                status_color = "#10b981"
                status_text = "Normal"
                status_bg = "#d1fae5"

            st.markdown(f"""
            <div style="background: white; padding: 24px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); margin: 16px 0; display: flex; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center; gap: 16px;">
                    <div style="width: 48px; height: 48px; background: linear-gradient(135deg, #c1adf0, #a855f7); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; font-size: 20px;">
                        📄
                    </div>
                    <div>
                        <h3 style="margin: 0; color: #1f2937; font-size: 18px; font-weight: 600;">{row['File']}</h3>
                        <p style="margin: 4px 0 0 0; color: #6b7280; font-size: 14px;">
                            Age: {row.get('Age (months)', 'N/A')} months • MLU: {row.get('MLU', 'N/A')} • MATTR: {row.get('MATTR', 'N/A')}
                        </p>
                    </div>
                </div>
                <div style="display: flex; align-items: center; gap: 16px;">
                    <span style="background: {status_bg}; color: {status_color}; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600;">
                        {status_text}
                    </span>
                    <button style="background: #f3f4f6; border: none; padding: 8px 16px; border-radius: 8px; color: #374151; font-weight: 500; cursor: pointer;">
                        View Analysis
                    </button>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        # Show sample sessions when no data
        sample_sessions = [
            {
                "filename": "session_20240115.cha",
                "time": "Yesterday, 2:30 PM • 8 min 32 sec",
                "status": "At Risk",
                "status_color": "#f59e0b",
                "status_bg": "#fef3c7"
            },
            {
                "filename": "session_20240113.cha",
                "time": "3 days ago, 10:15 AM • 12 min 45 sec",
                "status": "Normal",
                "status_color": "#10b981",
                "status_bg": "#d1fae5"
            }
        ]

        for session in sample_sessions:
            st.markdown(f"""
            <div style="background: white; padding: 24px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); margin: 16px 0; display: flex; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center; gap: 16px;">
                    <div style="width: 48px; height: 48px; background: linear-gradient(135deg, #c1adf0, #a855f7); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; font-size: 20px;">
                        📄
                    </div>
                    <div>
                        <h3 style="margin: 0; color: #1f2937; font-size: 18px; font-weight: 600;">{session['filename']}</h3>
                        <p style="margin: 4px 0 0 0; color: #6b7280; font-size: 14px;">{session['time']}</p>
                    </div>
                </div>
                <div style="display: flex; align-items: center; gap: 16px;">
                    <span style="background: {session['status_bg']}; color: {session['status_color']}; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600;">
                        {session['status']}
                    </span>
                    <button style="background: #f3f4f6; border: none; padding: 8px 16px; border-radius: 8px; color: #374151; font-weight: 500; cursor: pointer;">
                        View Analysis
                    </button>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Results display (PROPERLY INDENTED INSIDE LANGUAGE ANALYSIS PAGE)
    # Results display (DEBUGGING VERSION - SIMPLER AND MORE RELIABLE)
    # Results display (COMPLETE BEAUTIFUL VERSION - ALL METRICS)
    # Results display (FIXED VERSION - NO HTML ERRORS, NO FILE ANALYZED SECTION)
    # Results display (BEAUTIFUL METRIC CARDS DESIGN)
    # Results display (FIXED BEAUTIFUL CARDS - NO HTML ERRORS + SAMPLE QUALITY CARD)
    # Results display (FIXED - ALL CONTENT CONTAINED IN CARDS)
    # Results display (FIXED - ALL CONTENT CONTAINED IN CARDS)
    if st.session_state.results_df is not None and not st.session_state.results_df.empty:
        try:
            # Get the first row of results
            first_result = st.session_state.results_df.iloc[0]
            
            # Extract all values
            age_months = first_result.get('Age (months)', 'Unknown')
            total_utterances = first_result.get('Total Utterances', 'Unknown')
            group = str(first_result.get('Group', 'G1'))
            sample_quality = str(first_result.get('Sample Quality', 'Unknown'))
            transcription_quality = str(first_result.get('Transcription Quality', '95%'))
            overall_assessment = str(first_result.get('Overall Assessment', 'Normal'))
            
            # Language metrics
            mlu_value = first_result.get('MLU (Morphemes)', 0)
            mlu_status = str(first_result.get('MLU Status', 'Normal'))
            mattr_value = first_result.get('MATTR', 0)
            mattr_status = str(first_result.get('MATTR Status', 'Normal'))
            ndw_value = first_result.get('NDW', 0)
            ndw_status = str(first_result.get('NDW Status', 'Normal'))
            ttr_value = first_result.get('TTR', 0)
            ttr_status = str(first_result.get('TTR Status', 'Normal'))
            complex_ratio = str(first_result.get('Complex Ratio', '0%'))
            complex_status = str(first_result.get('Complex Status', 'Normal'))
            vocd_value = first_result.get('VocD', 0)
            vocd_status = str(first_result.get('VocD Status', 'Normal'))
            
            # Get norm ranges
            group_norms = norms.get(group, norms['G1'])
            min_age = group_norms['min']
            max_age = group_norms['max']
            
            # Calculate percentiles and progress
            def calculate_percentile_and_progress(value, target_range, status):
                if isinstance(value, (int, float)) and len(target_range) == 2:
                    min_val, max_val = target_range
                    if value >= max_val:
                        return 95, 100, "Excellent Performance"
                    elif value >= min_val:
                        progress = 50 + ((value - min_val) / (max_val - min_val) * 35)
                        return int(progress), int(progress), "Good Performance"
                    else:
                        progress = (value / min_val) * 40
                        return max(10, int(progress)), int(progress), "Below Average"
                return 75 if "Normal" in status else 40, 75 if "Normal" in status else 40, "Normal" if "Normal" in status else "Below Average"
          
            
            # Starting Header
            st.markdown("""
            <h2 style="font-size: 42px; font-weight: 700; color: #1f2937; margin: 60px 0 40px 0;">
                 Overview
            </h2>
            """, unsafe_allow_html=True)

            # Simple metrics WITHOUT "Overview" heading - REMOVED OVERVIEW HEADING
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("𖠋 Child Age", f"{age_months} months")
            with col2:
                st.metric("💬 Sample Size", f"{total_utterances} utterances")
            with col3:
                st.metric("☰ Norm Group", f"{group} ({min_age}-{max_age}m)")
            
            if "No concerns" in overall_assessment:
                st.success("✅ Development on Track")
            else:
                st.warning("⚠️ Needs Monitoring")
            
            st.markdown("---")
            
            # Detailed Metrics Header
            st.markdown("""
            <h2 style="font-size: 42px; font-weight: 700; color: #1f2937; margin: 60px 0 40px 0;">
                ⚙️ Detailed Metrics
            </h2>
            """, unsafe_allow_html=True)
            
            # MLU Metric Card - FIXED: ALL IN ONE HTML BLOCK (like NDW/TTR)
            mlu_percentile, mlu_progress, mlu_performance = calculate_percentile_and_progress(mlu_value, group_norms['mlu_morphemes'], mlu_status)
            performance_color = "#10b981" if mlu_percentile >= 70 else "#f59e0b" if mlu_percentile >= 40 else "#ef4444"
            performance_bg = "#d1fae5" if mlu_percentile >= 70 else "#fef3c7" if mlu_percentile >= 40 else "#fee2e2"
            
            st.markdown(f"""
            <div style="background: white; border-radius: 24px; padding: 50px; box-shadow: 0 8px 32px rgba(0,0,0,0.08); margin-bottom: 40px; border: 1px solid #f1f5f9;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 30px;">
                    <div style="flex: 1; max-width: 500px;">
                        <h3 style="font-size: 32px; font-weight: 700; color: #1f2937; margin-bottom: 20px; line-height: 1.2;">
                            Mean Length of Utterance (MLU)
                        </h3>
                        <p style="font-size: 18px; color: #6b7280; line-height: 1.6; margin: 0;">
                            Measures the average number of morphemes (meaningful units) per utterance. This is a key indicator of syntactic development and sentence complexity.
                        </p>
                    </div>
                    <div style="text-align: right; margin-left: 40px;">
                        <div style="font-size: 72px; font-weight: 900; background: linear-gradient(135deg, #6366f1, #8b5cf6, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; line-height: 1; margin-bottom: 10px;">
                            {mlu_value:.2f}
                        </div>
                        <div style="font-size: 16px; color: #9ca3af; font-weight: 500;">
                            Target: {group_norms['mlu_morphemes'][0]}-{group_norms['mlu_morphemes'][1]}
                        </div>
                    </div>
                </div>
                <div style="margin-bottom: 30px;">
                    <div style="width: 100%; height: 16px; background: #f1f5f9; border-radius: 8px; overflow: hidden; margin-bottom: 15px;">
                        <div style="height: 100%; background: linear-gradient(90deg, #6366f1, #8b5cf6, #a855f7, #06b6d4); border-radius: 8px; width: {mlu_progress}%;"></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 14px; color: #9ca3af; font-weight: 500;">
                        <span>Below Average</span>
                        <span>Average</span>
                        <span>Above Average</span>
                        <span>Excellent</span>
                    </div>
                </div>
                <div style="background: {performance_bg}; color: {performance_color}; padding: 16px 28px; border-radius: 25px; font-size: 16px; font-weight: 700; text-align: center; display: inline-block;">
                    {mlu_performance} ({mlu_percentile}th percentile)
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # MATTR Metric Card - FIXED: ALL IN ONE HTML BLOCK (like NDW/TTR)
            mattr_percentile, mattr_progress, mattr_performance = calculate_percentile_and_progress(mattr_value, group_norms['mattr'], mattr_status)
            performance_color = "#10b981" if mattr_percentile >= 70 else "#f59e0b" if mattr_percentile >= 40 else "#ef4444"
            performance_bg = "#d1fae5" if mattr_percentile >= 70 else "#fef3c7" if mattr_percentile >= 40 else "#fee2e2"
            
            st.markdown(f"""
            <div style="background: white; border-radius: 24px; padding: 50px; box-shadow: 0 8px 32px rgba(0,0,0,0.08); margin-bottom: 40px; border: 1px solid #f1f5f9;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 30px;">
                    <div style="flex: 1; max-width: 500px;">
                        <h3 style="font-size: 32px; font-weight: 700; color: #1f2937; margin-bottom: 20px; line-height: 1.2;">
                            Lexical Diversity (MATTR)
                        </h3>
                        <p style="font-size: 18px; color: #6b7280; line-height: 1.6; margin: 0;">
                            Moving Average Type-Token Ratio measures vocabulary richness and word variety. Higher values indicate more diverse vocabulary use.
                        </p>
                    </div>
                    <div style="text-align: right; margin-left: 40px;">
                        <div style="font-size: 72px; font-weight: 900; background: linear-gradient(135deg, #6366f1, #8b5cf6, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; line-height: 1; margin-bottom: 10px;">
                            {mattr_value:.3f}
                        </div>
                        <div style="font-size: 16px; color: #9ca3af; font-weight: 500;">
                            Target: {group_norms['mattr'][0]}-{group_norms['mattr'][1]}
                        </div>
                    </div>
                </div>
                <div style="margin-bottom: 30px;">
                    <div style="width: 100%; height: 16px; background: #f1f5f9; border-radius: 8px; overflow: hidden; margin-bottom: 15px;">
                        <div style="height: 100%; background: linear-gradient(90deg, #6366f1, #8b5cf6, #a855f7, #06b6d4); border-radius: 8px; width: {mattr_progress}%;"></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 14px; color: #9ca3af; font-weight: 500;">
                        <span>Below Average</span>
                        <span>Average</span>
                        <span>Above Average</span>
                        <span>Excellent</span>
                    </div>
                </div>
                <div style="background: {performance_bg}; color: {performance_color}; padding: 16px 28px; border-radius: 25px; font-size: 16px; font-weight: 700; text-align: center; display: inline-block;">
                    {mattr_performance} ({mattr_percentile}th percentile)
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # NDW Card - FIXED: SINGLE HTML BLOCK (like MLU/MATTR)
            ndw_percentile, ndw_progress, ndw_performance = calculate_percentile_and_progress(ndw_value, group_norms['ndw'], ndw_status)
            ndw_color = "#10b981" if ndw_percentile >= 70 else "#f59e0b" if ndw_percentile >= 40 else "#ef4444"
            ndw_bg = "#d1fae5" if ndw_percentile >= 70 else "#fef3c7" if ndw_percentile >= 40 else "#fee2e2"

            
            st.markdown(f"""
<div style="background: white; border-radius: 24px; padding: 50px; box-shadow: 0 8px 32px rgba(0,0,0,0.08); margin-bottom: 40px; border: 1px solid #f1f5f9;">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 30px;">
        <div style="flex: 1; max-width: 500px;">
            <h3 style="font-size: 32px; font-weight: 700; color: #1f2937; margin-bottom: 20px; line-height: 1.2;">
                Number Different Words (NDW)
            </h3>
            <p style="font-size: 18px; color: #6b7280; line-height: 1.6; margin: 0;">
                Total count of unique words used in the language sample. This measure reflects vocabulary breadth and lexical knowledge.
            </p>
        </div>
        <div style="text-align: right; margin-left: 40px;">
            <div style="font-size: 72px; font-weight: 900; background: linear-gradient(135deg, #6366f1, #8b5cf6, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; line-height: 1; margin-bottom: 10px;">
                {ndw_value}
            </div>
            <div style="font-size: 16px; color: #9ca3af; font-weight: 500;">
                Target: {group_norms['ndw'][0]}-{group_norms['ndw'][1]}
            </div>
        </div>
    </div>
    <div style="margin-bottom: 30px;">
        <div style="width: 100%; height: 16px; background: #f1f5f9; border-radius: 8px; overflow: hidden; margin-bottom: 15px;">
            <div style="height: 100%; background: linear-gradient(90deg, #6366f1, #8b5cf6, #a855f7, #06b6d4); border-radius: 8px; width: {ndw_progress}%;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 14px; color: #9ca3af; font-weight: 500;">
            <span>Below Average</span>
            <span>Average</span>
            <span>Above Average</span>
            <span>Excellent</span>
        </div>
    </div>
    <div style="background: {ndw_bg}; color: {ndw_color}; padding: 16px 28px; border-radius: 25px; font-size: 16px; font-weight: 700; text-align: center; display: inline-block;">
        {ndw_performance} ({ndw_percentile}th percentile)
    </div>
</div>
""", unsafe_allow_html=True)
            
            
            # TTR Card - FIXED: SINGLE HTML BLOCK (like MLU/MATTR)
            ttr_percentile, ttr_progress, ttr_performance = calculate_percentile_and_progress(ttr_value, group_norms['ttr'], ttr_status)
            ttr_color = "#10b981" if ttr_percentile >= 70 else "#f59e0b" if ttr_percentile >= 40 else "#ef4444"
            ttr_bg = "#d1fae5" if ttr_percentile >= 70 else "#fef3c7" if ttr_percentile >= 40 else "#fee2e2"
            
            st.markdown(f"""
<div style="background: white; border-radius: 24px; padding: 50px; box-shadow: 0 8px 32px rgba(0,0,0,0.08); margin-bottom: 40px; border: 1px solid #f1f5f9;">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 30px;">
        <div style="flex: 1; max-width: 500px;">
            <h3 style="font-size: 32px; font-weight: 700; color: #1f2937; margin-bottom: 20px; line-height: 1.2;">
                Type-Token Ratio (TTR)
            </h3>
            <p style="font-size: 18px; color: #6b7280; line-height: 1.6; margin: 0;">
                Ratio of unique words to total words used. This basic measure of lexical diversity shows vocabulary variety within the sample.
            </p>
        </div>
        <div style="text-align: right; margin-left: 40px;">
            <div style="font-size: 72px; font-weight: 900; background: linear-gradient(135deg, #6366f1, #8b5cf6, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; line-height: 1; margin-bottom: 10px;">
                {ttr_value:.3f}
            </div>
            <div style="font-size: 16px; color: #9ca3af; font-weight: 500;">
                Target: {group_norms['ttr'][0]}-{group_norms['ttr'][1]}
            </div>
        </div>
    </div>
    <div style="margin-bottom: 30px;">
        <div style="width: 100%; height: 16px; background: #f1f5f9; border-radius: 8px; overflow: hidden; margin-bottom: 15px;">
            <div style="height: 100%; background: linear-gradient(90deg, #6366f1, #8b5cf6, #a855f7, #06b6d4); border-radius: 8px; width: {ttr_progress}%;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 14px; color: #9ca3af; font-weight: 500;">
            <span>Below Average</span>
            <span>Average</span>
            <span>Above Average</span>
            <span>Excellent</span>
        </div>
    </div>
    <div style="background: {ttr_bg}; color: {ttr_color}; padding: 16px 28px; border-radius: 25px; font-size: 16px; font-weight: 700; text-align: center; display: inline-block;">
        {ttr_performance} ({ttr_percentile}th percentile)
    </div>
</div>
""", unsafe_allow_html=True)
            
            
           
            
            # VocD Card - FIXED: SINGLE HTML BLOCK (like MLU/MATTR)
            vocd_percentile, vocd_progress, vocd_performance = calculate_percentile_and_progress(vocd_value, group_norms['vocd'], vocd_status)
            vocd_color = "#10b981" if vocd_percentile >= 70 else "#f59e0b" if vocd_percentile >= 40 else "#ef4444"
            vocd_bg = "#d1fae5" if vocd_percentile >= 70 else "#fef3c7" if vocd_percentile >= 40 else "#fee2e2"
            
            st.markdown(f"""
<div style="background: white; border-radius: 24px; padding: 50px; box-shadow: 0 8px 32px rgba(0,0,0,0.08); margin-bottom: 40px; border: 1px solid #f1f5f9;">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 30px;">
        <div style="flex: 1; max-width: 500px;">
            <h3 style="font-size: 32px; font-weight: 700; color: #1f2937; margin-bottom: 20px; line-height: 1.2;">
                VocD Score
            </h3>
            <p style="font-size: 18px; color: #6b7280; line-height: 1.6; margin: 0;">
                Vocabulary diversity estimate adjusted for sample length. This sophisticated measure provides a more accurate assessment of lexical richness than simple ratios.
            </p>
        </div>
        <div style="text-align: right; margin-left: 40px;">
            <div style="font-size: 72px; font-weight: 900; background: linear-gradient(135deg, #6366f1, #8b5cf6, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; line-height: 1; margin-bottom: 10px;">
                {vocd_value}
            </div>
            <div style="font-size: 16px; color: #9ca3af; font-weight: 500;">
                Target: {group_norms['vocd'][0]}-{group_norms['vocd'][1]}
            </div>
        </div>
    </div>
    <div style="margin-bottom: 30px;">
        <div style="width: 100%; height: 16px; background: #f1f5f9; border-radius: 8px; overflow: hidden; margin-bottom: 15px;">
            <div style="height: 100%; background: linear-gradient(90deg, #6366f1, #8b5cf6, #a855f7, #06b6d4); border-radius: 8px; width: {vocd_progress}%;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 14px; color: #9ca3af; font-weight: 500;">
            <span>Below Average</span>
            <span>Average</span>
            <span>Above Average</span>
            <span>Excellent</span>
        </div>
    </div>
    <div style="background: {vocd_bg}; color: {vocd_color}; padding: 16px 28px; border-radius: 25px; font-size: 16px; font-weight: 700; text-align: center; display: inline-block;">
        {vocd_performance} ({vocd_percentile}th percentile)
    </div>
</div>
""", unsafe_allow_html=True)
            
            
           
            # Sample Quality Card - SINGLE HTML BLOCK
            st.markdown(f"""
            <div style="background: white; border-radius: 24px; padding: 50px; box-shadow: 0 8px 32px rgba(0,0,0,0.08); margin-bottom: 40px; border: 1px solid #f1f5f9;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 30px;">
                    <div style="flex: 1; max-width: 500px;">
                        <h3 style="font-size: 32px; font-weight: 700; color: #1f2937; margin-bottom: 20px; line-height: 1.2;">
                            Sample Quality Assessment
                        </h3>
                        <p style="font-size: 18px; color: #6b7280; line-height: 1.6; margin: 0;">
                            Evaluation of transcription quality and sample adequacy for reliable language analysis. Higher quality samples provide more accurate assessment results.
                        </p>
                    </div>
                    <div style="text-align: right; margin-left: 40px;">
                        <div style="font-size: 50px; font-weight: 700; background: linear-gradient(135deg, #9477b5, #987db8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; line-height: 1; margin-bottom: 10px;">
                            {sample_quality}
                        </div>
                        <div style="font-size: 28px; color: #9ca3af; font-weight: 500;">
                            Quality: {transcription_quality}
                        </div>
                    </div>
                </div>
                <div style="background: #f0f9ff; padding: 20px; border-radius: 16px; margin-bottom: 20px;">
                    <div style="font-size: 16px; color: #0369a1; font-weight: 600; margin-bottom: 8px;">
                        📊 Sample Details
                    </div>
                    <div style="font-size: 20px; color: #0369a1;">
                        • Total utterances analyzed: {total_utterances}<br>
                        • Transcription accuracy: {transcription_quality}<br>
                        • Sample adequacy: {sample_quality}
                    </div>
                </div>
                <div style="background: #d1fae5; color: #065f46; padding: 16px 28px; border-radius: 25px; font-size: 16px; font-weight: 700; text-align: center; display: inline-block;">
                    ✅ Analysis Ready - Reliable Results
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Summary Card - SINGLE HTML BLOCK
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #8b5cf6, #a855f7); border-radius: 20px; padding: 35px; color: white; margin-bottom: 50px;">
                <h3 style="font-size: 45px; font-weight: 700; margin-bottom: 12px;">
                    Assessment Summary
                </h3>
                <p style="font-size: 30px; opacity: 0.9; margin-bottom: 20px;">
                    Complete analysis results for all language metrics
                </p>
                <div style="font-size: 65px; font-weight: 900; margin-bottom: 8px;">
                    7/7
                </div>
                <div style="font-size: 12px; opacity: 0.8; margin-bottom: 20px;">
                     Metrics Calculated  
                </div>
                <div style="background: rgba(255,255,255,0.2); padding: 12px; border-radius: 12px; font-size: 13px;">
                    <div>• Age Group: {group} ({age_months} months)</div>
                    <div>• Sample: {total_utterances} utterances</div>
                    <div>• Quality: {sample_quality}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Final Recommendations using simple Streamlit
            st.markdown("## 💡 Recommendations")
            
            successful_metrics = sum(1 for status in [mlu_status, mattr_status, ndw_status, ttr_status, vocd_status, complex_status] 
                                   if "Normal" in status)
            
            if successful_metrics >= 5:
                st.success("""
                **Excellent Progress** 🎉
                - Continue current language stimulation activities
                - Regular developmental monitoring  
                - Maintain rich language environment
                """)
            elif successful_metrics >= 3:
                st.warning("""
                **Monitor Development** ⚠️
                - Focus on areas showing delays
                - Consider additional language activities
                - Follow up in 3-6 months
                """)
            else:
                st.error("""
                **Further Evaluation Recommended** 🔍
                - Consult with speech-language pathologist
                - Consider comprehensive assessment
                - Implement targeted interventions
                """)
            
        except Exception as e:
            st.error(f"Error displaying results: {e}")
            st.write("Debug info:")
            st.dataframe(st.session_state.results_df)
# Questionnaire Page - KEEP ALL YOUR EXISTING FUNCTIONALITY
elif st.session_state.current_page == "questionnaire":
    # Back button with modern styling
    if st.button("← Back to Home", key="back_quest"):
        go_to_landing()

    # Modern page header
    st.markdown("""
    <div style="text-align: center; margin: 40px 0;">
        <h1 style="font-size: 48px; font-weight: 700; color: #1f2937; margin-bottom: 16px;">
            📋 Developmental Questionnaire
        </h1>
        <p style="font-size: 18px; color: #6b7280; max-width: 600px; margin: 0 auto;">
            Complete developmental questionnaires based on child's age with comprehensive assessment tools.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Child information form with modern styling
    st.markdown("""
    <div style="background: #8b5cf6; padding: 40px; border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); margin: 40px 0;">
        <h3 style="color: white; margin-bottom: 20px; font-size: 52px;">🧸 Child Information</h3>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        child_name = st.text_input("Child's Name:")
        birth_date = st.date_input("Birth Date:")

    with col2:
        today_date = st.date_input("Today's Date:", value=datetime.now().date())

    if birth_date and today_date:
        age_months = (today_date.year - birth_date.year) * 12 + (today_date.month - birth_date.month)
        st.info(f"Child's age: {age_months} months")

        # Check if exact questionnaire exists, otherwise suggest closest
        if age_months in questionnaire_data:
            st.session_state.selected_age = age_months
        else:
            available_ages = get_available_questionnaires()
            closest_age = find_closest_questionnaire(age_months)

            st.warning(f"⚠️ No exact questionnaire available for {age_months} months.")
            st.info(f"📋 Available questionnaires: {', '.join(map(str, available_ages))} months")
            st.info(f"🎯 Closest match: {closest_age} months questionnaire")

            if st.button(f"Use {closest_age} months questionnaire", type="primary"):
                st.session_state.selected_age = closest_age

        if hasattr(st.session_state, 'selected_age') and st.session_state.selected_age is not None:
            questionnaire = questionnaire_data[st.session_state.selected_age]
            sections = questionnaire["sections"]

            # Show which questionnaire is being used
            if st.session_state.selected_age != age_months:
                st.success(f"📋 Using {st.session_state.selected_age} months questionnaire (closest to {age_months} months)")

            # Questionnaire header with modern styling
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #8b5cf6, #a855f7); padding: 30px; border-radius: 20px; margin: 30px 0; color: white;">
                <h2 style="margin: 0; font-size: 28px; font-weight: 700;">{questionnaire['title']}</h2>
                <p style="margin: 10px 0 0 0; opacity: 0.9;"><strong>{questionnaire['subtitle']}</strong></p>
                <p style="margin: 5px 0 0 0; opacity: 0.8; font-style: italic;">{questionnaire['version']}</p>
            </div>
            """, unsafe_allow_html=True)

            # Current section and question
            current_section_idx = st.session_state.current_section
            current_question_idx = st.session_state.current_question

            # Check if questionnaire is completed
            total_questions = sum(len(section["questions"]) for section in sections)
            completed_questions = len(st.session_state.responses)

            if completed_questions >= total_questions:
                # Show results with modern styling
                st.markdown("""
                <div style="background: linear-gradient(135deg, #10b981, #059669); padding: 40px; border-radius: 20px; margin: 30px 0; color: white; text-align: center;">
                    <h2 style="margin: 0; font-size: 32px; font-weight: 700;">🎉 Questionnaire Completed!</h2>
                    <p style="margin: 10px 0 0 0; font-size: 18px; opacity: 0.9;">Assessment results are ready for review</p>
                </div>
                """, unsafe_allow_html=True)
                st.balloons()

                # Calculate exact age for assessment
                if birth_date and today_date:
                    exact_age_months = calculate_exact_age_in_months(birth_date, today_date)
                    scores = calculate_questionnaire_scores(st.session_state.responses, st.session_state.selected_age, exact_age_months)
                else:
                    scores = calculate_questionnaire_scores(st.session_state.responses)

                # Create Results tabs - Now with 5 tabs for comprehensive display
                result_tabs = st.tabs(["🎯 Milestones", "👶 BPSC", "🧒 PPSC", "👥 POSI", "📊 Summary"])

                with result_tabs[0]:  # Developmental Milestones
                    st.markdown("## 🎯 Developmental Milestones Assessment")

                    # Find the developmental milestones section
                    dm_section = None
                    dm_section_name = None
                    for section_name, section_data in scores.items():
                        if "DEVELOPMENTAL MILESTONES" in section_name and "assessment" in section_data:
                            dm_section = section_data
                            dm_section_name = section_name
                            break

                    if dm_section:
                        # Display the assessment results
                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.metric("Raw Score", f"{dm_section['raw_score']}/20")

                        with col2:
                            if "threshold" in dm_section:
                                st.metric("Threshold", f"≤{dm_section['threshold']}")
                            else:
                                st.metric("Threshold", "N/A")

                        with col3:
                            assessment = dm_section["assessment"]
                            if "Needs Review" in assessment:
                                st.error(assessment)
                            elif "meets age expectations" in assessment:
                                st.success(assessment)
                            else:
                                st.info(assessment)

                        # Additional information
                        st.markdown("---")
                        st.markdown("### Assessment Criteria")
                        st.info("""
                        **Developmental Milestones Scoring:**
                        - Very Much = 2 points
                        - Somewhat = 1 point
                        - Not Yet = 0 points

                        **Assessment:**
                        - Score ≤ threshold: Needs Review
                        - Score > threshold: Appears to meet age expectations
                        """)

                        if birth_date and today_date:
                            st.markdown(f"**Child's exact age:** {exact_age_months} months")
                            st.markdown(f"**Questionnaire used:** {st.session_state.selected_age} months")
                    else:
                        st.warning("Developmental milestones assessment not available for this age group.")

                with result_tabs[1]:  # BPSC
                    st.markdown("## 👶 Baby Pediatric Symptom Checklist (BPSC)")

                    # Find BPSC section
                    bpsc_section = None
                    for section_name, section_data in scores.items():
                        if section_data.get("scoring_method") == "BPSC":
                            bpsc_section = section_data
                            break

                    if bpsc_section:
                        # Overall BPSC result
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Total Score", f"{bpsc_section['raw_score']}/24")
                        with col2:
                            if bpsc_section.get("risk_status") == "At Risk":
                                st.error(f"⚠️ {bpsc_section['risk_status']}")
                            else:
                                st.success(f"✅ {bpsc_section['risk_status']}")

                        # Subscale breakdown
                        if "subscale_scores" in bpsc_section:
                            st.markdown("### Subscale Results")
                            st.markdown("*Any subscale score ≥3 indicates at risk*")

                            subscale_data = bpsc_section["subscale_scores"]

                            for subscale_key, subscale_info in subscale_data.items():
                                with st.expander(f"{subscale_info['name']} - Score: {subscale_info['score']}/8"):
                                    col1, col2 = st.columns([1, 2])

                                    with col1:
                                        if subscale_info["score"] >= 3:
                                            st.error(f"⚠️ At Risk (Score: {subscale_info['score']})")
                                        else:
                                            st.success(f"✅ Not At Risk (Score: {subscale_info['score']})")

                                    with col2:
                                        st.markdown("**Questions in this subscale:**")
                                        for question in subscale_info["questions"]:
                                            st.markdown(f"• {question}")

                        # Scoring explanation
                        st.markdown("---")
                        st.info("""
                        **BPSC Scoring:**
                        - Not at All = 0 points
                        - Somewhat = 1 point
                        - Very Much = 2 points

                        **Risk Assessment:**
                        - 3+ on ANY subscale = At Risk
                        - All subscales <3 = Not At Risk
                        """)
                    else:
                        st.info("No BPSC assessment found in this questionnaire.")

                with result_tabs[2]:  # PPSC
                    st.markdown("## 🧒 Preschool Pediatric Symptom Checklist (PPSC)")

                    # Find PPSC section
                    ppsc_section = None
                    for section_name, section_data in scores.items():
                        if section_data.get("scoring_method") == "PPSC":
                            ppsc_section = section_data
                            break

                    if ppsc_section:
                        # PPSC results
                        col1, col2, col3 = st.columns(3)

                        with col1:
                            max_score = ppsc_section["total_questions"] * 2
                            st.metric("Total Score", f"{ppsc_section['raw_score']}/{max_score}")

                        with col2:
                            st.metric("Threshold", "≥9")

                        with col3:
                            if ppsc_section.get("risk_status") == "At Risk":
                                st.error(f"⚠️ {ppsc_section['risk_status']}")
                            else:
                                st.success(f"✅ {ppsc_section['risk_status']}")

                        # Assessment details
                        st.markdown("### Assessment Result")
                        assessment = ppsc_section.get("assessment", "")
                        if "At Risk" in assessment:
                            st.error(assessment)
                        else:
                            st.success(assessment)

                        # Scoring explanation
                        st.markdown("---")
                        st.info("""
                        **PPSC Scoring:**
                        - Not at All = 0 points
                        - Somewhat = 1 point
                        - Very Much = 2 points

                        **Risk Assessment:**
                        - Total score ≥9 = At Risk
                        - Total score <9 = Not At Risk
                        """)
                    else:
                        st.info("No PPSC assessment found in this questionnaire.")

                with result_tabs[3]:  # POSI
                    st.markdown("## 👥 Parent's Observations of Social Interactions (POSI)")

                    # Find POSI section
                    posi_section = None
                    for section_name, section_data in scores.items():
                        if section_data.get("scoring_method") == "POSI":
                            posi_section = section_data
                            break

                    if posi_section:
                        # POSI results
                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.metric("Total Score", f"{posi_section['raw_score']}/7")

                        with col2:
                            st.metric("Threshold", "≥3")

                        with col3:
                            if posi_section.get("risk_status") == "At Risk":
                                st.error(f"⚠️ {posi_section['risk_status']}")
                            else:
                                st.success(f"✅ {posi_section['risk_status']}")

                        # Assessment details
                        st.markdown("### Assessment Result")
                        assessment = posi_section.get("assessment", "")
                        if "At Risk" in assessment:
                            st.error(assessment)
                        else:
                            st.success(assessment)

                        # Scoring explanation
                        st.markdown("---")
                        st.info("""
                        **POSI Scoring:**
                        - Each question scored as 0 or 1
                        - Score 1 if response is in the last three columns
                        - Score 0 otherwise

                        **Risk Assessment:**
                        - 3+ points = At Risk
                        - <3 points = Not At Risk
                        """)
                    else:
                        st.info("No POSI assessment found in this questionnaire.")

                with result_tabs[4]:  # Summary
                    st.markdown("## 📊 Complete Assessment Summary")

                    # Overall summary
                    st.markdown("### Overall Results")

                    # Count assessments
                    total_assessments = 0
                    at_risk_assessments = 0

                    assessment_results = []

                    for section_name, section_data in scores.items():
                        if "risk_status" in section_data:
                            total_assessments += 1
                            if section_data["risk_status"] == "At Risk":
                                at_risk_assessments += 1

                            assessment_results.append({
                                "Assessment": section_data.get("scoring_method", section_name),
                                "Score": f"{section_data['raw_score']}/{section_data.get('max_score', section_data['total_questions']*2)}",
                                "Status": section_data["risk_status"],
                                "Details": section_data.get("assessment", "")
                            })

                    # Overall risk indicator
                    if at_risk_assessments > 0:
                        st.error(f"⚠️ {at_risk_assessments} of {total_assessments} assessments indicate potential risk")
                    else:
                        st.success(f"✅ All {total_assessments} assessments show no concerning indicators")

                    # Summary table
                    if assessment_results:
                        st.markdown("### Assessment Details")
                        for result in assessment_results:
                            with st.expander(f"{result['Assessment']} - {result['Status']}"):
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.markdown(f"**Score:** {result['Score']}")
                                with col2:
                                    if result['Status'] == "At Risk":
                                        st.error(f"**Status:** {result['Status']}")
                                    else:
                                        st.success(f"**Status:** {result['Status']}")
                                st.markdown(f"**Assessment:** {result['Details']}")

                    # Developmental milestones (if available)
                    dm_section = None
                    for section_name, section_data in scores.items():
                        if "DEVELOPMENTAL MILESTONES" in section_name and "assessment" in section_data:
                            dm_section = section_data
                            break

                    if dm_section:
                        st.markdown("### Developmental Milestones")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Score", f"{dm_section['raw_score']}/20")
                        with col2:
                            assessment = dm_section["assessment"]
                            if "Needs Review" in assessment:
                                st.error(assessment)
                            elif "meets age expectations" in assessment:
                                st.success(assessment)
                            else:
                                st.info(assessment)

                    # Recommendations
                    st.markdown("---")
                    st.markdown("### Clinical Recommendations")
                    if at_risk_assessments > 0:
                        st.warning("""
                        **Next Steps:**
                        - Consider further evaluation or consultation with a healthcare provider
                        - Discuss results with your child's pediatrician
                        - Monitor development and consider follow-up screening
                        - Focus on areas identified as concerning
                        """)
                    else:
                        st.info("""
                        **Continue monitoring:**
                        - Regular developmental check-ups
                        - Continue age-appropriate activities and stimulation
                        - Follow up at next scheduled screening interval
                        - Maintain supportive environment for development
                        """)

                # Modern styled restart button
                st.markdown("""
                <div style="text-align: center; margin: 40px 0;">
                """, unsafe_allow_html=True)
                if st.button("🔄 Start New Questionnaire", type="primary", use_container_width=True):
                    reset_questionnaire()
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

            elif current_section_idx < len(sections):
                current_section = sections[current_section_idx]

                # Show progress with modern styling
                progress = completed_questions / total_questions
                st.markdown("""
                <div style="background: white; padding: 30px; border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); margin: 30px 0;">
                """, unsafe_allow_html=True)
                st.progress(progress)
                st.caption(f"Progress: {completed_questions}/{total_questions} questions completed")
                st.markdown("</div>", unsafe_allow_html=True)

                # Section header with modern styling
                st.markdown(f"""
                <div style="background: white; padding: 30px; border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); margin: 30px 0;">
                    <h3 style="color: #1f2937; margin-bottom: 15px;">{current_section['title']}</h3>
                </div>
                """, unsafe_allow_html=True)
                if current_section.get('description'):
                    st.markdown(f"""
                    <div style="background: #f8f9ff; padding: 20px; border-radius: 15px; margin: 20px 0; border-left: 4px solid #8b5cf6;">
                        <p style="margin: 0; color: #374151;">{current_section['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)

                # Current question
                if current_question_idx < len(current_section["questions"]):
                    # Get question data using helper function
                    question, options, question_data = get_current_question_data(current_section, current_question_idx)

                    # Question number with modern styling
                    section_progress = current_question_idx + 1
                    section_total = len(current_section["questions"])
                    st.markdown(f"""
                    <div style="text-align: center; margin: 30px 0;">
                        <span style="background: linear-gradient(135deg, #8b5cf6, #a855f7); color: white; padding: 8px 16px; border-radius: 20px; font-size: 14px; font-weight: 600;">
                            Question {section_progress} of {section_total}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)

                    response_key = f"section_{current_section_idx}_q_{current_question_idx}"

                    # Render question based on type
                    if question_data is not None:
                        # Special question (POSI section)
                        render_special_question(question_data, response_key, current_section_idx, current_question_idx, current_section)
                    else:
                        # Regular question
                        render_standard_question(question, options, response_key, current_section_idx, current_question_idx, current_section)

def reset_questionnaire():
    """Reset questionnaire to start over"""
    st.session_state.current_section = 0
    st.session_state.current_question = 0
    st.session_state.responses = {}
    st.session_state.section_completed = {}
    if hasattr(st.session_state, 'selected_age'):
        del st.session_state.selected_age
