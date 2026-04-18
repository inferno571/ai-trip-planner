import streamlit as st
import requests
import datetime
import sys
import json
import os

BASE_URL = os.getenv("API_BACKEND_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Wanderlust AI — Smart Trip Planner",
    page_icon=":material/flight:",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap');

    /* Material icon inline helper */
    .mi {
        font-family: 'Material Symbols Outlined' !important;
        font-size: inherit;
        vertical-align: middle;
        display: inline-block;
        line-height: 1;
        font-weight: normal;
        font-style: normal;
        letter-spacing: normal;
        text-transform: none;
        white-space: nowrap;
        word-wrap: normal;
        direction: ltr;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        font-feature-settings: 'liga';
        margin-right: 4px;
    }
    /* Size modifiers */
    .mi-sm { font-size: 1rem;  }
    .mi-md { font-size: 1.25rem; }
    .mi-lg { font-size: 1.5rem; }

    /* ── Global Typography ──────────────────────────────── */
    *, html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Exhaustive Streamlit element coverage */
    .stApp,
    .stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown td, .stMarkdown th,
    .stTextInput input, .stTextInput label,
    .stSelectbox label, .stSelectbox div,
    .stButton > button,
    .stFormSubmitButton button,
    .stChatMessage, .stChatMessage p,
    div[data-testid="stExpander"] summary,
    div[data-testid="stMetric"] label,
    div[data-testid="stMetric"] div,
    .stTabs [data-baseweb="tab"],
    .stAlert p,
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li,
    section[data-testid="stSidebar"] .stButton > button,
    span, label, div, p, a, li, td, th, button, input, textarea, select {
        font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Preserve Streamlit's internal icon fonts */
    [data-testid="stIconMaterial"],
    .material-symbols-rounded,
    [data-baseweb] span[aria-hidden="true"] {
        font-family: 'Material Symbols Rounded' !important;
    }

    /* Heading typographic scale */
    .stMarkdown h1, .hero-title {
        font-weight: 800 !important;
        letter-spacing: -0.02em !important;
        line-height: 1.1 !important;
    }
    .stMarkdown h2 {
        font-weight: 700 !important;
        letter-spacing: -0.015em !important;
        line-height: 1.2 !important;
    }
    .stMarkdown h3 {
        font-weight: 600 !important;
        letter-spacing: -0.01em !important;
        line-height: 1.25 !important;
    }
    .stMarkdown h4 {
        font-weight: 600 !important;
        letter-spacing: -0.005em !important;
        line-height: 1.3 !important;
    }

    /* Body text rendering */
    .stMarkdown p, .stMarkdown li {
        font-weight: 400;
        line-height: 1.65;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }

    /* Button typography */
    .stButton > button, .stFormSubmitButton button {
        font-weight: 600 !important;
        letter-spacing: 0.01em !important;
    }

    .stApp {
        background: transparent !important;
    }

    /* ── Ambient Background Slideshow ───────────────────── */
    .bg-slideshow {
        position: fixed;
        inset: 0;
        z-index: -1;
        overflow: hidden;
        background-color: #0f172a;
    }
    .bg-img {
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        background-size: cover;
        background-position: center;
        opacity: 0;
        animation: crossfade 40s ease-in-out infinite;
        will-change: opacity, transform;
    }
    .bg-img:nth-child(1) { animation-delay: -2s; }
    .bg-img:nth-child(2) { animation-delay: 8s; }
    .bg-img:nth-child(3) { animation-delay: 18s; }
    .bg-img:nth-child(4) { animation-delay: 28s; }

    @keyframes crossfade {
        0%   { opacity: 0; transform: scale(1.0); }
        5%   { opacity: 1; transform: scale(1.02); }
        25%  { opacity: 1; transform: scale(1.10); }
        30%  { opacity: 0; transform: scale(1.12); }
        100% { opacity: 0; transform: scale(1.12); }
    }

    /* Dark overlay on top of the slideshow so the foreground UI is legible */
    .bg-overlay {
        position: absolute;
        inset: 0;
        background: rgba(15, 23, 42, 0.7);
        pointer-events: none;
    }

    /* ── Center main content ────────────────────────────── */
    .main .block-container {
        max-width: 780px !important;
        margin: 0 auto !important;
        padding-top: 48px !important;
    }

    /* Hide default header & footer */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* ── Scrollbar ──────────────────────────────────────── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0a0e17; }
    ::-webkit-scrollbar-thumb { background: #2DD4BF44; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #2DD4BF88; }

    /* ── Sidebar ────────────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1117 0%, #080b12 100%) !important;
        border-right: 1px solid rgba(45, 212, 191, 0.08) !important;
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li {
        color: #B0BEC5 !important;
        font-size: 0.88rem !important;
    }

    /* ── Animations ─────────────────────────────────────── */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(18px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes shimmer {
        0%   { background-position: -200% center; }
        100% { background-position: 200% center; }
    }
    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 0 8px #2DD4BF33; }
        50%      { box-shadow: 0 0 20px #2DD4BF55; }
    }
    .fade-in {
        animation: fadeInUp 0.5s ease-out;
    }

    /* ── Hero Section ───────────────────────────────────── */
    .hero-container {
        text-align: center;
        padding: 36px 0 8px 0;
    }
    .hero-title {
        font-size: 3.6rem;
        font-weight: 800;
        color: #F1F5F9;
        letter-spacing: -0.02em;
        margin-bottom: 0;
        line-height: 1.1;
    }
    .hero-subtitle {
        color: #94A3B8 !important;
        font-size: 1.15rem;
        font-weight: 400;
        margin-top: 14px;
        margin-bottom: 36px;
        letter-spacing: 0.2px;
    }

    /* ── Feature Pills ──────────────────────────────────── */
    .feature-row {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
        justify-content: center;
        margin-bottom: 28px;
    }
    .feature-pill {
        background: rgba(45, 212, 191, 0.08);
        border: 1px solid rgba(45, 212, 191, 0.2);
        padding: 8px 18px;
        border-radius: 100px;
        color: #2DD4BF;
        font-size: 0.82rem;
        font-weight: 500;
        transition: all 0.25s ease;
        letter-spacing: 0.2px;
    }
    .feature-pill:hover {
        background: rgba(45, 212, 191, 0.15);
        border-color: rgba(45, 212, 191, 0.4);
        transform: translateY(-1px);
    }

    /* ── Chat Bubbles ───────────────────────────────────── */
    .chat-user {
        background: rgba(45, 212, 191, 0.06);
        border-left: 3px solid #2DD4BF;
        padding: 16px 20px;
        border-radius: 4px 14px 14px 4px;
        margin: 12px 0;
        animation: fadeInUp 0.35s ease-out;
    }
    .chat-user p { color: #D1D5DB !important; margin: 0; }
    .chat-user .chat-label {
        color: #2DD4BF;
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 6px;
    }

    .chat-assistant {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.05) 0%, rgba(251, 113, 133, 0.04) 100%);
        border-left: 3px solid #F59E0B;
        padding: 16px 20px;
        border-radius: 4px 14px 14px 4px;
        margin: 12px 0;
        animation: fadeInUp 0.35s ease-out;
    }
    .chat-assistant .chat-label {
        color: #F59E0B;
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 6px;
    }
    .chat-assistant p, .chat-assistant li, .chat-assistant td {
        color: #D1D5DB !important;
    }
    .chat-assistant h1, .chat-assistant h2, .chat-assistant h3 {
        color: #F0F0F0 !important;
    }
    .chat-assistant strong { color: #F59E0B !important; }
    .chat-assistant hr {
        border-color: #F59E0B22 !important;
    }

    /* ── Glass Card ─────────────────────────────────────── */
    .glass-card {
        background: rgba(17, 24, 39, 0.6);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 28px;
        margin: 16px auto;
        max-width: 640px;
        animation: fadeInUp 0.4s ease-out;
    }

    /* ── Timestamp Badge ────────────────────────────────── */
    .timestamp {
        font-size: 0.68rem;
        color: #5C6B7A;
        font-weight: 400;
        margin-top: 10px;
        text-align: right;
    }

    /* ── Divider ────────────────────────────────────────── */
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, #2DD4BF33 50%, transparent 100%);
        border: none;
        margin: 24px 0;
    }

    /* ── Search Bar (Custom Form) ──────────────────────── */
    div[data-testid="stForm"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        max-width: 640px;
        margin: 8px auto 0 auto;
    }

    /* The vertical block inside the form is our positioning context */
    div[data-testid="stForm"] div[data-testid="stVerticalBlock"] {
        position: relative !important;
        gap: 0 !important;
    }

    /* Pill-shaped glassmorphism input */
    div[data-testid="stForm"] .stTextInput > div {
        background: rgba(13, 17, 23, 0.55) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(45, 212, 191, 0.15) !important;
        border-radius: 999px !important;
        padding: 4px 64px 4px 24px !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="stForm"] .stTextInput > div:focus-within {
        border-color: rgba(45, 212, 191, 0.4) !important;
        box-shadow: 0 0 24px rgba(45, 212, 191, 0.1),
                    0 0 48px rgba(45, 212, 191, 0.04) !important;
    }
    div[data-testid="stForm"] .stTextInput input {
        color: #F1F5F9 !important;
        font-size: 1rem !important;
        padding: 14px 0 !important;
        background: transparent !important;
        caret-color: #2DD4BF !important;
    }
    div[data-testid="stForm"] .stTextInput input::placeholder {
        color: #4B5C6B !important;
        font-weight: 400 !important;
    }
    /* Hide the label */
    div[data-testid="stForm"] .stTextInput label {
        display: none !important;
    }

    /* Position the button's stElementContainer absolutely over the input */
    div[data-testid="stForm"] div[data-testid="stVerticalBlock"] > div[data-testid="stElementContainer"]:last-child {
        position: absolute !important;
        right: 6px !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        z-index: 10 !important;
        width: auto !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Submit button → teal accent circle icon */
    div[data-testid="stForm"] .stFormSubmitButton {
        margin: 0 !important;
        padding: 0 !important;
    }
    div[data-testid="stForm"] .stFormSubmitButton button {
        background: linear-gradient(135deg, #2DD4BF 0%, #14B8A6 100%) !important;
        border: none !important;
        border-radius: 50% !important;
        width: 42px !important;
        height: 42px !important;
        min-height: 42px !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        color: #0a0e17 !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        cursor: pointer !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 2px 12px rgba(45, 212, 191, 0.3) !important;
    }
    div[data-testid="stForm"] .stFormSubmitButton button:hover {
        background: linear-gradient(135deg, #34D399 0%, #2DD4BF 100%) !important;
        box-shadow: 0 4px 20px rgba(45, 212, 191, 0.45) !important;
        transform: scale(1.06) !important;
    }
    div[data-testid="stForm"] .stFormSubmitButton button:active {
        transform: scale(0.96) !important;
    }

    /* ── Sidebar Prompt Buttons ─────────────────────────── */
    section[data-testid="stSidebar"] .stButton > button {
        background: rgba(45, 212, 191, 0.06) !important;
        border: 1px solid rgba(45, 212, 191, 0.18) !important;
        color: #B0BEC5 !important;
        border-radius: 10px !important;
        padding: 8px 14px !important;
        font-size: 0.82rem !important;
        text-align: left !important;
        width: 100% !important;
        transition: all 0.25s ease !important;
        margin-bottom: 4px !important;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(45, 212, 191, 0.14) !important;
        border-color: rgba(45, 212, 191, 0.35) !important;
        color: #2DD4BF !important;
        transform: translateX(3px) !important;
    }

    /* ── Footer ─────────────────────────────────────────── */
    .app-footer {
        text-align: center;
        color: #3D4F5F;
        font-size: 0.72rem;
        padding: 32px 0 16px 0;
        letter-spacing: 0.5px;
    }
    .app-footer a {
        color: #2DD4BF88;
        text-decoration: none;
    }

    /* ── Sidebar Logo ───────────────────────────────────── */
    .sidebar-logo {
        font-size: 1.4rem;
        font-weight: 700;
        color: #2DD4BF;
        margin-bottom: 2px;
    }
    .sidebar-tagline {
        color: #5C6B7A;
        font-size: 0.78rem;
        margin-bottom: 24px;
        font-weight: 300;
    }
    .sidebar-section-title {
        color: #8899A6;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.6px;
        margin: 20px 0 10px 0;
    }

    /* ── Welcome Card Features ──────────────────────────── */
    .welcome-feature {
        display: flex;
        align-items: flex-start;
        gap: 14px;
        padding: 14px 0;
    }
    .welcome-feature-icon {
        font-size: 1.6rem;
        min-width: 36px;
        text-align: center;
    }
    .welcome-feature-text h4 {
        color: #E8E6E3 !important;
        margin: 0 0 3px 0;
        font-size: 0.95rem;
        font-weight: 600;
    }
    .welcome-feature-text p {
        color: #6B7D8D !important;
        margin: 0;
        font-size: 0.82rem;
        line-height: 1.4;
    }
</style>

<div class="bg-slideshow">
    <div class="bg-img" style="background-image: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1920&q=80');"></div>
    <div class="bg-img" style="background-image: url('https://images.unsplash.com/photo-1519681393784-d120267933ba?w=1920&q=80');"></div>
    <div class="bg-img" style="background-image: url('https://images.unsplash.com/photo-1448375240586-882707db8855?w=1920&q=80');"></div>
    <div class="bg-img" style="background-image: url('https://images.unsplash.com/photo-1519501025264-65ba15a82390?w=1920&q=80');"></div>
    <div class="bg-overlay"></div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="sidebar-logo"><span class="mi mi-md">flight</span> Wanderlust AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-tagline">Your intelligent travel companion</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-title"><span class="mi mi-sm">build</span> Capabilities</div>', unsafe_allow_html=True)
    st.markdown("""
    <ul style="list-style:none; padding-left:0; margin:0;">
        <li style="padding:3px 0;"><span class="mi mi-sm" style="color:#2DD4BF;">cloud</span> <strong>Real-time weather</strong> forecasts</li>
        <li style="padding:3px 0;"><span class="mi mi-sm" style="color:#2DD4BF;">location_on</span> <strong>Place discovery</strong> &amp; attractions</li>
        <li style="padding:3px 0;"><span class="mi mi-sm" style="color:#2DD4BF;">payments</span> <strong>Expense estimation</strong> &amp; budgeting</li>
        <li style="padding:3px 0;"><span class="mi mi-sm" style="color:#2DD4BF;">currency_exchange</span> <strong>Currency conversion</strong> rates</li>
        <li style="padding:3px 0;"><span class="mi mi-sm" style="color:#2DD4BF;">calendar_month</span> <strong>Day-by-day</strong> itinerary planning</li>
        <li style="padding:3px 0;"><span class="mi mi-sm" style="color:#2DD4BF;">hotel</span> <strong>Hotel &amp; restaurant</strong> suggestions</li>
    </ul>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-title"><span class="mi mi-sm">bolt</span> Quick Prompts</div>', unsafe_allow_html=True)

    sample_prompts = [
        ("Plan a 5-day trip to Goa", "Plan a 5-day trip to Goa"),
        ("Weekend getaway to Paris on a budget", "Weekend getaway to Paris on a budget"),
        ("7-day backpacking trip to Manali", "7-day backpacking trip to Manali"),
        ("Best time to visit Japan for cherry blossoms", "Best time to visit Japan for cherry blossoms"),
        ("Honeymoon in Maldives", "Honeymoon in Maldives — luxury plan"),
    ]

    for label, query in sample_prompts:
        if st.button(label, key=f"prompt_{query}"):
            st.session_state["prefilled_prompt"] = query

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="color: #3D4F5F; font-size: 0.72rem; padding-top: 12px;">
        <strong style="color: #5C6B7A;">Wanderlust AI</strong><br/>
        Powered by LangGraph
    </div>
    """, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages:
    st.markdown("""
    <div class="hero-container fade-in">
        <div class="hero-title">Where to next?</div>
        <div class="hero-subtitle">
            Your dream trip, planned in seconds.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-row">
        <span class="feature-pill"><span class="mi mi-sm">cloud</span> Live Weather</span>
        <span class="feature-pill"><span class="mi mi-sm">location_on</span> Places & Attractions</span>
        <span class="feature-pill"><span class="mi mi-sm">payments</span> Smart Budgeting</span>
        <span class="feature-pill"><span class="mi mi-sm">currency_exchange</span> Currency Rates</span>
        <span class="feature-pill"><span class="mi mi-sm">map</span> Custom Itineraries</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
        <div class="welcome-feature">
            <div class="welcome-feature-icon"><span class="mi mi-lg">calendar_month</span></div>
            <div class="welcome-feature-text">
                <h4>Day-by-Day Itineraries</h4>
                <p>Get detailed plans with morning, afternoon & evening activities tailored to your style.</p>
            </div>
        </div>
        <div class="welcome-feature">
            <div class="welcome-feature-icon"><span class="mi mi-lg">explore</span></div>
            <div class="welcome-feature-text">
                <h4>Off-Beat Recommendations</h4>
                <p>Discover hidden gems alongside popular tourist spots for a richer travel experience.</p>
            </div>
        </div>
        <div class="welcome-feature">
            <div class="welcome-feature-icon"><span class="mi mi-lg">bar_chart</span></div>
            <div class="welcome-feature-text">
                <h4>Complete Cost Breakdowns</h4>
                <p>Per-day budgets covering hotels, food, transport & activities — no hidden surprises.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="chat-user">
            <div class="chat-label"><span class="mi mi-sm">person</span> You</div>
            <p>{msg["content"]}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-assistant">
            <div class="chat-label"><span class="mi mi-sm">public</span> Wanderlust AI</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(msg["content"])
        if "timestamp" in msg:
            st.markdown(f'<div class="timestamp">{msg["timestamp"]}</div>', unsafe_allow_html=True)

prefilled = st.session_state.pop("prefilled_prompt", None)

with st.form(key="search_form", clear_on_submit=True, border=False):
    user_input = st.text_input(
        "Search",
        value=prefilled or "",
        placeholder="Where would you like to go? e.g., Plan a 5-day trip to Bali...",
        label_visibility="collapsed",
    )
    submitted = st.form_submit_button("➔")

if not submitted:
    user_input = None

if user_input:
    st.markdown(f"""
    <div class="chat-user fade-in">
        <div class="chat-label"><span class="mi mi-sm">person</span> You</div>
        <p>{user_input}</p>
    </div>
    """, unsafe_allow_html=True)

    success = False
    try:
        payload = {"question": user_input}
        response = requests.post(f"{BASE_URL}/query", json=payload, stream=True, timeout=300)

        if response.status_code == 200:
            answer = ""
            with st.status("Wanderlust AI is crafting your travel plan...", expanded=True) as status:
                for line in response.iter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            if data.get("type") == "tool_call":
                                tool_name = data.get("tool")
                                
                                TOOL_LOGO_MAP = {
                                    "get_current_weather": ("openweathermap.png", "OpenWeatherMap"),
                                    "get_weather_forecast": ("openweathermap.png", "OpenWeatherMap"),
                                    "search_attractions": ("google.png", "Google Places"),
                                    "search_restaurants": ("google.png", "Google Places"),
                                    "search_activities": ("google.png", "Google Places"),
                                    "search_transportation": ("google.png", "Google Places"),
                                    "convert_currency": ("exchangerate.png", "ExchangeRate-API"),
                                    "estimate_total_hotel_cost": ("calculator.png", "Expense Calculator"),
                                    "calculate_total_expense": ("calculator.png", "Expense Calculator"),
                                    "calculate_daily_expense_budget": ("calculator.png", "Expense Calculator"),
                                }
                                logo_filename, api_name = TOOL_LOGO_MAP.get(tool_name, ("default.png", "Tool"))
                                logo_path = f"static/logos/{logo_filename}"
                                
                                col1, col2 = st.columns([1, 15])
                                with col1:
                                    if os.path.exists(logo_path):
                                        st.image(logo_path, width=24)
                                    else:
                                        st.markdown(f'<span class="mi mi-sm">build</span>', unsafe_allow_html=True)
                                with col2:
                                    st.markdown(f"**{api_name}:** `{tool_name}`...")
                            elif data.get("type") == "final_answer":
                                answer = data.get("content", "")
                                status.update(label="Travel plan ready!", state="complete", expanded=False)
                            elif data.get("type") == "system_status":
                                col1, col2 = st.columns([1, 15])
                                with col1:
                                    st.markdown(f'<span class="mi mi-sm">auto_awesome</span>', unsafe_allow_html=True)
                                with col2:
                                    st.markdown(f"**AI Brain:** `{data.get('content')}`")
                            elif data.get("type") == "error":
                                st.error(data.get("content"))
                        except Exception as e:
                            pass

            if answer:
                timestamp = datetime.datetime.now().strftime("%b %d, %Y at %I:%M %p")

                # Only add messages to session state after successful response
                st.session_state.messages.append({"role": "user", "content": user_input})
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "timestamp": timestamp,
                })

                # Display assistant response
                st.markdown("""
                <div class="chat-assistant fade-in">
                    <div class="chat-label"><span class="mi mi-sm">public</span> Wanderlust AI</div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(answer)

                st.markdown(f'<div class="timestamp">Generated on {timestamp}</div>', unsafe_allow_html=True)
                success = True
        else:
            # Parse the error detail from the backend JSON response
            try:
                error_detail = response.json().get("error", response.text)
            except Exception:
                error_detail = response.text
            st.error(f"Server error ({response.status_code}): {error_detail}")

    except requests.exceptions.ConnectionError:
        st.warning("⚠️ Could not connect to the backend. Make sure `uvicorn main:app` is running on port 8000.")
    except requests.exceptions.Timeout:
        st.warning("⏳ The request timed out. The AI might be processing a complex query — try again.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")

    # Only rerun on success so the page refreshes with the new messages.
    # On failure, DON'T rerun — let the user see the error message.
    if success:
        st.rerun()

st.markdown("""
<div class="app-footer">
    <span class="mi mi-sm">flight</span> Wanderlust AI · Built with Streamlit & LangGraph
</div>
""", unsafe_allow_html=True)