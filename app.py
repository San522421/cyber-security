import streamlit as st
import math
import re
import string
import secrets
import zxcvbn

st.set_page_config(
    page_title="PassGuard — Password Integrity Tester",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #0a0e1a;
}

/* Header */
.pg-header {
    text-align: center;
    padding: 2rem 0 1rem;
    border-bottom: 1px solid #1e2d47;
    margin-bottom: 2rem;
}
.pg-logo {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2.8rem;
    font-weight: 700;
    background: linear-gradient(135deg, #00d4ff 0%, #7c3aed 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -1px;
}
.pg-tagline {
    color: #64748b;
    font-size: 0.95rem;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.08em;
    margin-top: 0.3rem;
}

/* Metric cards */
.metric-card {
    background: #111827;
    border: 1px solid #1e2d47;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.3s;
}
.metric-card:hover {
    border-color: #00d4ff40;
}
.metric-title {
    color: #64748b;
    font-size: 0.7rem;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.metric-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    line-height: 1;
}
.metric-sub {
    color: #64748b;
    font-size: 0.8rem;
    margin-top: 0.3rem;
    font-family: 'JetBrains Mono', monospace;
}

/* Strength label */
.strength-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.1rem;
    font-weight: 600;
    letter-spacing: 0.05em;
}

/* Warning badge */
.warn-badge {
    display: inline-block;
    background: #7f1d1d22;
    border: 1px solid #ef444444;
    color: #f87171;
    border-radius: 6px;
    padding: 0.2rem 0.6rem;
    font-size: 0.75rem;
    font-family: 'JetBrains Mono', monospace;
    margin: 0.15rem;
}
.ok-badge {
    display: inline-block;
    background: #14532d22;
    border: 1px solid #22c55e44;
    color: #4ade80;
    border-radius: 6px;
    padding: 0.2rem 0.6rem;
    font-size: 0.75rem;
    font-family: 'JetBrains Mono', monospace;
    margin: 0.15rem;
}
.info-badge {
    display: inline-block;
    background: #1e3a5f22;
    border: 1px solid #3b82f644;
    color: #60a5fa;
    border-radius: 6px;
    padding: 0.2rem 0.6rem;
    font-size: 0.75rem;
    font-family: 'JetBrains Mono', monospace;
    margin: 0.15rem;
}

/* Section headers */
.section-header {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #475569;
    border-bottom: 1px solid #1e2d47;
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
}

/* Tip item */
.tip-item {
    padding: 0.6rem 0.8rem;
    border-radius: 8px;
    margin-bottom: 0.4rem;
    font-size: 0.85rem;
    font-family: 'JetBrains Mono', monospace;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.tip-pass {
    background: #14532d15;
    border: 1px solid #22c55e33;
    color: #4ade80;
}
.tip-fail {
    background: #7f1d1d15;
    border: 1px solid #ef444433;
    color: #fca5a5;
}

/* Generator card */
.gen-card {
    background: #0d1526;
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 1.5rem;
}

/* Password display */
.pw-display {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.1rem;
    background: #070b14;
    border: 1px solid #1e2d47;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    color: #00d4ff;
    word-break: break-all;
    letter-spacing: 0.05em;
    min-height: 3rem;
}

/* HIBP card */
.hibp-card {
    border-radius: 10px;
    padding: 1rem 1.25rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
}

/* Divider */
hr {
    border-color: #1e2d47 !important;
}

/* Override input style */
.stTextInput > div > div > input {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.1rem !important;
    letter-spacing: 0.05em !important;
    background: #070b14 !important;
    border: 2px solid #1e3a5f !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    padding: 0.75rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #00d4ff !important;
    box-shadow: 0 0 0 3px #00d4ff20 !important;
}

/* Button styling */
.stButton > button {
    font-family: 'JetBrains Mono', monospace !important;
    background: linear-gradient(135deg, #0369a1, #7c3aed) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover {
    opacity: 0.85 !important;
}

/* Progress bar colors */
.stProgress > div > div > div > div {
    border-radius: 99px !important;
}
</style>
""", unsafe_allow_html=True)

# ── Constants ──────────────────────────────────────────────────────────────────
COMMON_PASSWORDS = {
    "password", "123456", "qwerty", "abc123", "letmein", "monkey",
    "iloveyou", "admin", "welcome", "login", "master", "111111",
    "password1", "sunshine", "princess", "shadow", "superman", "dragon",
    "football", "baseball", "pass", "test", "guest", "root", "toor",
    "12345678", "1234567", "1234567890", "qwerty123", "passw0rd",
    "trustno1", "hello", "charlie", "donald", "696969", "mustang",
    "access", "batman", "michael", "jessica", "666666", "ashley",
    "bailey", "000000", "7777777", "password2", "hunter2", "hunter",
}

KEYBOARD_SEQUENCES = [
    "qwerty", "qwertyuiop", "asdf", "asdfghjkl", "zxcv", "zxcvbnm",
    "1234567890", "0987654321", "abcdefgh", "abcdef",
    "qwer", "asdfgh", "zxcvbn", "poiuyt", "lkjhgf", "mnbvcx",
]

# ── Analysis functions ────────────────────────────────────────────────────────
def calc_charset_size(password: str) -> int:
    size = 0
    if re.search(r"[a-z]", password):
        size += 26
    if re.search(r"[A-Z]", password):
        size += 26
    if re.search(r"[0-9]", password):
        size += 10
    if re.search(r"[!-/:-@\[-`{-~]", password):
        size += 32
    return max(size, 1)

def calc_entropy(password: str) -> float:
    charset = calc_charset_size(password)
    return len(password) * math.log2(charset)

def detect_patterns(password: str) -> list[str]:
    patterns = []
    lower = password.lower()

    for seq in KEYBOARD_SEQUENCES:
        if seq in lower:
            patterns.append(f"keyboard pattern '{seq}'")
            break

    if re.search(r"(.)\1{2,}", password):
        patterns.append("repeated characters (e.g. aaa)")

    if re.search(r"(012|123|234|345|456|567|678|789|890|987|876|765|654|543|432|321|210)", password):
        patterns.append("numeric sequence")

    if re.search(r"(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)", lower):
        patterns.append("alphabetic sequence")

    if re.search(r"(19|20)\d{2}", password):
        patterns.append("year pattern")

    if re.search(r"\b(0[1-9]|1[0-2])(\/|-)(0[1-9]|[12]\d|3[01])\b", password):
        patterns.append("date pattern")

    if lower in COMMON_PASSWORDS:
        patterns.append("common/breached password")

    # Check if any word matches common passwords
    words = re.findall(r"[a-zA-Z]{4,}", password)
    for w in words:
        if w.lower() in COMMON_PASSWORDS:
            patterns.append(f"common word '{w}'")
            break

    return patterns[:5]

def crack_time_label(seconds: float) -> tuple[str, str]:
    if seconds < 1:
        return "Instantly", "#ef4444"
    elif seconds < 60:
        return f"{seconds:.0f} seconds", "#f97316"
    elif seconds < 3600:
        return f"{seconds/60:.0f} minutes", "#f97316"
    elif seconds < 86400:
        return f"{seconds/3600:.1f} hours", "#eab308"
    elif seconds < 2_592_000:
        return f"{seconds/86400:.0f} days", "#eab308"
    elif seconds < 31_536_000:
        return f"{seconds/2_592_000:.0f} months", "#84cc16"
    elif seconds < 3_153_600_000:
        return f"{seconds/31_536_000:.0f} years", "#22c55e"
    elif seconds < 315_360_000_000:
        return f"{seconds/3_153_600_000:.0f} centuries", "#00d4ff"
    else:
        return "Practically forever", "#7c3aed"

def get_strength_info(score: int) -> tuple[str, str, float]:
    levels = [
        (0,  20,  "VERY WEAK",  "#ef4444", 0.1),
        (20, 40,  "WEAK",       "#f97316", 0.3),
        (40, 60,  "FAIR",       "#eab308", 0.55),
        (60, 80,  "STRONG",     "#22c55e", 0.8),
        (80, 101, "VERY STRONG","#00d4ff", 1.0),
    ]
    for lo, hi, label, color, pct in levels:
        if lo <= score < hi:
            return label, color, pct
    return "VERY STRONG", "#00d4ff", 1.0

def custom_score(password: str) -> int:
    if not password:
        return 0
    score = min(len(password) * 4, 40)
    if re.search(r"[A-Z]", password): score += 10
    if re.search(r"[a-z]", password): score += 10
    if re.search(r"[0-9]", password): score += 10
    if re.search(r"[^a-zA-Z0-9]", password): score += 15
    if len(password) >= 16: score += 5
    if len(password) >= 20: score += 5
    patterns = detect_patterns(password)
    score -= len(patterns) * 12
    return max(0, min(100, score))

def analyze_password(password: str) -> dict:
    if not password:
        return {}

    zx = zxcvbn.zxcvbn(password)
    entropy = calc_entropy(password)
    patterns = detect_patterns(password)
    score = custom_score(password)
    strength_label, strength_color, strength_pct = get_strength_info(score)

    # Crack time: combine zxcvbn + entropy estimation
    guesses_per_sec = 1e10
    entropy_seconds = (2 ** entropy) / guesses_per_sec

    crack_secs = min(
        float(zx["crack_times_seconds"]["offline_fast_hashing_1e10_per_second"]),
        entropy_seconds
    ) if entropy_seconds > 0 else float(zx["crack_times_seconds"]["offline_fast_hashing_1e10_per_second"])

    crack_display, crack_color = crack_time_label(crack_secs)

    # Character composition
    upper = len(re.findall(r"[A-Z]", password))
    lower = len(re.findall(r"[a-z]", password))
    digits = len(re.findall(r"[0-9]", password))
    special = len(re.findall(r"[^a-zA-Z0-9]", password))

    # Tips
    tips = []
    tips.append(("At least 12 characters",    len(password) >= 12))
    tips.append(("At least 16 characters",    len(password) >= 16))
    tips.append(("Uppercase letters (A-Z)",   upper > 0))
    tips.append(("Lowercase letters (a-z)",   lower > 0))
    tips.append(("Numbers (0-9)",              digits > 0))
    tips.append(("Special characters (!@#…)", special > 0))
    tips.append(("No common words/passwords", password.lower() not in COMMON_PASSWORDS))
    tips.append(("No keyboard sequences",     not any(seq in password.lower() for seq in KEYBOARD_SEQUENCES)))
    tips.append(("No repeated characters",    not bool(re.search(r"(.)\1{2,}", password))))
    tips.append(("Entropy above 60 bits",      entropy >= 60))

    return {
        "score": score,
        "strength_label": strength_label,
        "strength_color": strength_color,
        "strength_pct": strength_pct,
        "entropy": entropy,
        "patterns": patterns,
        "crack_display": crack_display,
        "crack_color": crack_color,
        "upper": upper,
        "lower": lower,
        "digits": digits,
        "special": special,
        "tips": tips,
        "zx_score": zx["score"],
    }

def get_suggestions(password: str, analysis: dict) -> list[dict]:
    """Return prioritized, specific suggestions with icons and detail text."""
    suggestions = []
    length = len(password)
    upper = analysis["upper"]
    lower = analysis["lower"]
    digits = analysis["digits"]
    special = analysis["special"]
    entropy = analysis["entropy"]
    patterns = analysis["patterns"]

    # Length suggestions
    if length < 8:
        need = 8 - length
        suggestions.append({
            "icon": "📏",
            "priority": "critical",
            "title": f"Add {need} more character{'s' if need > 1 else ''}",
            "detail": f"Your password is only {length} chars. Aim for at least 12 — every extra character multiplies crack time exponentially.",
        })
    elif length < 12:
        need = 12 - length
        suggestions.append({
            "icon": "📏",
            "priority": "high",
            "title": f"Add {need} more character{'s' if need > 1 else ''} (reach 12)",
            "detail": "Passwords under 12 characters are crackable in hours with modern hardware.",
        })
    elif length < 16:
        suggestions.append({
            "icon": "📏",
            "priority": "medium",
            "title": "Consider making it 16+ characters",
            "detail": "16+ character passwords are dramatically harder to crack, especially with mixed types.",
        })

    # Missing character types
    if upper == 0:
        suggestions.append({
            "icon": "🔠",
            "priority": "high",
            "title": "Add uppercase letters (A–Z)",
            "detail": "Including uppercase letters expands your character pool from 26 to 52, doubling entropy per character.",
        })
    if lower == 0:
        suggestions.append({
            "icon": "🔡",
            "priority": "high",
            "title": "Add lowercase letters (a–z)",
            "detail": "Using lowercase alongside other types is a basic requirement for strong passwords.",
        })
    if digits == 0:
        suggestions.append({
            "icon": "🔢",
            "priority": "high",
            "title": "Include at least one number (0–9)",
            "detail": "Adding digits like 3, 7, or 9 increases your character pool and makes dictionary attacks harder.",
        })
    if special == 0:
        suggestions.append({
            "icon": "✳️",
            "priority": "high",
            "title": "Add a special character (e.g. ! @ # $ %)",
            "detail": "Symbols add 32+ extra characters to your pool. Even one symbol like ! or @ dramatically boosts strength.",
        })

    # Pattern-based suggestions
    for pat in patterns:
        if "keyboard" in pat:
            suggestions.append({
                "icon": "⌨️",
                "priority": "critical",
                "title": "Remove keyboard sequence",
                "detail": f"Detected: {pat}. Attackers test these first. Replace with random characters.",
            })
        elif "repeated" in pat:
            suggestions.append({
                "icon": "🔁",
                "priority": "high",
                "title": "Remove repeated characters",
                "detail": "Sequences like 'aaa' or '111' drastically reduce effective entropy. Use varied characters.",
            })
        elif "numeric sequence" in pat:
            suggestions.append({
                "icon": "🔢",
                "priority": "high",
                "title": "Avoid number sequences (123, 456…)",
                "detail": "Sequential numbers are among the first patterns tested in brute-force attacks.",
            })
        elif "year" in pat:
            suggestions.append({
                "icon": "📅",
                "priority": "medium",
                "title": "Remove the year pattern",
                "detail": "Years like 1990 or 2024 are predictable. Replace with a random number cluster.",
            })
        elif "common" in pat or "breached" in pat:
            suggestions.append({
                "icon": "🚨",
                "priority": "critical",
                "title": "This password is in breach lists",
                "detail": "Common or previously leaked passwords are cracked instantly. Change it entirely.",
            })

    # Entropy advice
    if entropy < 36:
        suggestions.append({
            "icon": "⚡",
            "priority": "critical",
            "title": "Entropy too low — easy to crack",
            "detail": f"Only {entropy:.0f} bits of entropy. Try a passphrase: combine 4 random words like 'blue-cake-moon-river'.",
        })
    elif entropy < 60:
        suggestions.append({
            "icon": "⚡",
            "priority": "medium",
            "title": "Boost entropy above 60 bits",
            "detail": f"At {entropy:.0f} bits, this could be cracked offline. Add length or more character variety.",
        })

    # Passphrase tip for short single-word passwords
    word_only = bool(re.match(r"^[a-zA-Z]+$", password))
    if word_only and length < 16:
        suggestions.append({
            "icon": "💡",
            "priority": "medium",
            "title": "Try a passphrase instead",
            "detail": "Example: 'River$Lamp9Cobalt!' — easy to remember, hard to crack. 4 random words + symbols = very strong.",
        })

    if not suggestions:
        suggestions.append({
            "icon": "🏆",
            "priority": "great",
            "title": "Excellent password!",
            "detail": "No major weaknesses detected. This password scores well on length, entropy, and character variety.",
        })

    # Sort: critical first, then high, medium, great
    order = {"critical": 0, "high": 1, "medium": 2, "great": 3}
    suggestions.sort(key=lambda s: order.get(s["priority"], 9))
    return suggestions[:6]


def generate_password(length: int, use_upper: bool, use_digits: bool, use_symbols: bool) -> str:
    chars = string.ascii_lowercase
    guaranteed = []
    if use_upper:
        chars += string.ascii_uppercase
        guaranteed.append(secrets.choice(string.ascii_uppercase))
    if use_digits:
        chars += string.digits
        guaranteed.append(secrets.choice(string.digits))
    if use_symbols:
        symbols = "!@#$%^&*()-_=+[]{}|;:,.<>?"
        chars += symbols
        guaranteed.append(secrets.choice(symbols))

    remaining = length - len(guaranteed)
    password_chars = [secrets.choice(chars) for _ in range(remaining)] + guaranteed
    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)



# ── Session state ─────────────────────────────────────────────────────────────
if "generated_pw" not in st.session_state:
    st.session_state.generated_pw = ""


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="pg-header">
  <div class="pg-logo">🔐 PassGuard</div>
  <div class="pg-tagline">// password integrity tester v1.0 · cybersecurity toolkit</div>
</div>
""", unsafe_allow_html=True)

# ── Main input ────────────────────────────────────────────────────────────────
password = st.text_input(
    "Enter password to analyze",
    value=st.session_state.generated_pw,
    type="password",
    placeholder="Type or paste your password here...",
    label_visibility="collapsed",
)

# ── Analysis ──────────────────────────────────────────────────────────────────
analysis = analyze_password(password) if password else {}

# ── Inline strength label + bar ───────────────────────────────────────────────
if password and analysis:
    sl = analysis["strength_label"]
    sc = analysis["strength_color"]
    sp = analysis["strength_pct"]
    score_val = analysis["score"]

    dot_colors = {"VERY WEAK": "#ef4444", "WEAK": "#f97316", "FAIR": "#eab308",
                  "STRONG": "#22c55e", "VERY STRONG": "#00d4ff"}
    dot = dot_colors.get(sl, "#64748b")

    st.markdown(f"""
    <div style="
        display:flex; align-items:center; gap:0.6rem;
        margin: 0.55rem 0 0.5rem;
        padding: 0.45rem 0.9rem;
        background:#111827;
        border:1px solid {sc}55;
        border-radius:8px;
        width:fit-content;
    ">
      <span style="
          width:9px; height:9px; border-radius:50%;
          background:{dot};
          box-shadow: 0 0 6px {dot};
          display:inline-block;
      "></span>
      <span style="
          font-family:'JetBrains Mono',monospace;
          font-size:0.82rem; font-weight:700;
          letter-spacing:0.1em;
          color:{sc};
      ">{sl}</span>
      <span style="
          font-family:'JetBrains Mono',monospace;
          font-size:0.75rem; color:#475569;
          border-left:1px solid #1e2d47;
          padding-left:0.6rem; margin-left:0.2rem;
      ">score {score_val}/100</span>
    </div>
    """, unsafe_allow_html=True)
    st.progress(sp)
else:
    st.markdown("""
    <div style="
        display:flex; align-items:center; gap:0.6rem;
        margin: 0.55rem 0 0.5rem;
        padding: 0.45rem 0.9rem;
        background:#0d1526;
        border:1px solid #1e2d47;
        border-radius:8px;
        width:fit-content;
    ">
      <span style="width:9px;height:9px;border-radius:50%;background:#1e2d47;display:inline-block;"></span>
      <span style="font-family:'JetBrains Mono',monospace;font-size:0.82rem;color:#1e3a5f;letter-spacing:0.1em;">AWAITING INPUT</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── Security Requirements Checklist (full width) ──────────────────────────────
st.markdown('<div class="section-header">Security Requirements</div>', unsafe_allow_html=True)

chk_cols = st.columns(2)
if password and analysis:
    tips = analysis["tips"]
    half = (len(tips) + 1) // 2
    for col_idx, col in enumerate(chk_cols):
        with col:
            for tip_text, passed in tips[col_idx * half:(col_idx + 1) * half]:
                icon = "✓" if passed else "✗"
                css = "tip-pass" if passed else "tip-fail"
                st.markdown(f'<div class="tip-item {css}"><span>{icon}</span><span>{tip_text}</span></div>', unsafe_allow_html=True)
else:
    placeholder_tips = [
        "At least 12 characters", "At least 16 characters",
        "Uppercase letters (A-Z)", "Lowercase letters (a-z)",
        "Numbers (0-9)", "Special characters (!@#…)",
        "No common words/passwords", "No keyboard sequences",
        "No repeated characters", "Entropy above 60 bits",
    ]
    half = len(placeholder_tips) // 2
    for col_idx, col in enumerate(chk_cols):
        with col:
            for text in placeholder_tips[col_idx * half:(col_idx + 1) * half]:
                st.markdown(f'<div class="tip-item" style="background:#0d1526; border:1px solid #1e2d47; color:#1e3a5f;"><span>—</span><span>{text}</span></div>', unsafe_allow_html=True)

# ── Password Generator ────────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="section-header">Secure Password Generator</div>', unsafe_allow_html=True)

g1, g2 = st.columns([3, 2], gap="large")

with g1:
    gen_length = st.slider("Length", min_value=8, max_value=64, value=20, step=1)
    gc1, gc2, gc3 = st.columns(3)
    with gc1:
        gen_upper = st.checkbox("Uppercase (A-Z)", value=True)
    with gc2:
        gen_digits = st.checkbox("Numbers (0-9)", value=True)
    with gc3:
        gen_symbols = st.checkbox("Symbols (!@#)", value=True)

    if st.button("⚡ Generate Strong Password", use_container_width=False):
        st.session_state.generated_pw = generate_password(gen_length, gen_upper, gen_digits, gen_symbols)
        st.rerun()

with g2:
    st.markdown('<div style="margin-top:0.2rem; color:#475569; font-family:JetBrains Mono; font-size:0.7rem; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:0.5rem;">Generated password</div>', unsafe_allow_html=True)
    if st.session_state.generated_pw:
        st.markdown(f'<div class="pw-display">{st.session_state.generated_pw}</div>', unsafe_allow_html=True)
        st.code(st.session_state.generated_pw, language=None)
        st.caption("Use the code block above to copy the password")
    else:
        st.markdown('<div class="pw-display" style="color:#1e3a5f;">press Generate to create a password</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; font-family:'JetBrains Mono',monospace; color:#1e3a5f; font-size:0.75rem; padding:0.5rem 0 1rem;">
  PassGuard · all analysis runs locally in your browser · no passwords are stored or transmitted
</div>
""", unsafe_allow_html=True)
