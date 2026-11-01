
import streamlit as st
from agent.app import run as run_strands_agent

# ==================================================
# PAGE SETTINGS
# ==================================================

st.set_page_config(
    page_title="Ninaivu Thunai",
    page_icon="🧠",
    layout="centered"
)

# ==================================================
# LANGUAGE TEXT
# ==================================================

TEXT = {
    "English": {
        "title": "🧠 Ninaivu Thunai",
        "subtitle": "Your friendly memory and daily assistance companion",
        "chat": "Chat",
        "welcome": "Hello! 👋 How can I help you today?",
        "placeholder": "Type your message here...",
        "suggestions": "Try asking",
        "suggestion1": "How can I remember my daily tasks?",
        "suggestion2": "Give me medicine reminders",
        "suggestion3": "What should I do if I feel confused?",
        "safety": "⚠️ I provide general assistance, not a medical diagnosis. For medical concerns, contact a healthcare professional.",
        "routine": "Try using a simple daily schedule. Write your tasks on a calendar, set reminders, and keep important items in the same place.",
        "medicine": "Take medicines only as prescribed by your doctor. Set reminders for medicine times or ask a trusted caregiver to help. Do not change your dose without medical advice.",
        "confused": "I can help with confusion, if you require daily reminders for day to day tasks. If confusion happens repeatedly, tell your doctor or caregiver.",
        "general": "I can help with daily routines, memory support, home safety, and reminders. Could you tell me a little more about what you need?",
        "clear": "Clear conversation",
        "settings": "⚙️ Settings",
        "language": "Language / மொழி",
        "appearance": "Appearance",
        "dark": "Dark",
        "light": "Light"
    },
    "தமிழ்": {
        "title": "🧠 நினைவுத் துணை",
        "subtitle": "உங்கள் நினைவாற்றலுக்கும் அன்றாட உதவிகளுக்கும் துணையாக இருக்கும் நண்பர்",
        "chat": "உரையாடல்",
        "welcome": "வணக்கம்! 👋 இன்று நான் உங்களுக்கு எப்படி உதவலாம்?",
        "placeholder": "உங்கள் செய்தியை இங்கே தட்டச்சு செய்யுங்கள்...",
        "suggestions": "இவற்றைக் கேட்கலாம்",
        "suggestion1": "எனது அன்றாட வேலைகளை நினைவில் வைத்துக்கொள்வது எப்படி?",
        "suggestion2": "மருந்து நினைவூட்டல்கள் வேண்டும்",
        "suggestion3": "திடீரென குழப்பமாக உணர்ந்தால் என்ன செய்ய வேண்டும்?",
        "safety": "⚠️ நான் பொதுவான உதவிகளை மட்டுமே வழங்குகிறேன்; மருத்துவ நோயறிதல் வழங்க முடியாது. மருத்துவப் பிரச்சினைகளுக்கு சுகாதார நிபுணரை அணுகுங்கள்.",
        "routine": "அன்றாட வேலைகளை நினைவில் வைத்துக்கொள்ள ஒரு எளிய அட்டவணையைப் பயன்படுத்துங்கள். வேலைகளை நாட்காட்டியில் எழுதுங்கள், நினைவூட்டல்களை அமைக்குங்கள், முக்கியமான பொருட்களை ஒரே இடத்தில் வையுங்கள்.",
        "medicine": "மருத்துவர் பரிந்துரைத்தபடி மட்டுமே மருந்துகளை எடுத்துக்கொள்ளுங்கள். மருந்து எடுத்துக்கொள்ளும் நேரத்திற்கு நினைவூட்டல் அமைக்கவும் அல்லது நம்பகமான பராமரிப்பாளரின் உதவியைப் பெறவும். மருத்துவ ஆலோசனையின்றி மருந்தின் அளவை மாற்ற வேண்டாம்.",
        "confused": "தினசரி பணிகளைச் செய்வதில் உங்களுக்குக் குழப்பம் இருந்தால், அவற்றை நினைவூட்டுவதன் மூலம் நான் உங்களுக்கு உதவுகிறேன். அடிக்கடி குழப்பம் ஏற்பட்டால் மருத்துவர் அல்லது பராமரிப்பாளரிடம் தெரிவியுங்கள்.",
        "general": "அன்றாட வேலைகள், நினைவாற்றல் உதவி, வீட்டுப் பாதுகாப்பு மற்றும் நினைவூட்டல்கள் தொடர்பாக நான் உதவுவேன். உங்களுக்கு என்ன உதவி தேவை என்பதைச் சிறிது விளக்க முடியுமா?",
        "clear": "உரையாடலை அழிக்கவும்",
        "settings": "⚙️ அமைப்புகள்",
        "language": "மொழி / Language",
        "appearance": "தோற்றம்",
        "dark": "இருண்ட நிறம்",
        "light": "வெளிர் நிறம்"
    }
}

# ==================================================
# SESSION STATE
# ==================================================

if "language" not in st.session_state:
    st.session_state.language = "English"

if "appearance" not in st.session_state:
    st.session_state.appearance = "Dark"

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==================================================
# SIDEBAR SETTINGS
# ==================================================

with st.sidebar:
    st.subheader("⚙️ Settings")

    language = st.selectbox(
        "Language / மொழி",
        ["English", "தமிழ்"],
        index=["English", "தமிழ்"].index(st.session_state.language)
    )

    st.session_state.language = language
    t = TEXT[language]

    appearance_options = ["Dark", "Light"]

    appearance = st.selectbox(
        t["appearance"],
        appearance_options,
        index=appearance_options.index(st.session_state.appearance),
        format_func=lambda value: (
            t["dark"] if value == "Dark" else t["light"]
        )
    )

    st.session_state.appearance = appearance

    if st.button(t["clear"], use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Refresh translated labels after language selection
language = st.session_state.language
t = TEXT[language]

# ==================================================
# THEME
# ==================================================

if st.session_state.appearance == "Dark":
    colors = {
        "background": "#0E1117",
        "secondary": "#161B22",
        "message": "#202938",
        "text": "#F1F5F9",
        "muted": "#CBD5E1",
        "border": "#394150",
        "input": "#1B2430",
        "button": "#263449",
        "hover": "#35465E",
        "accent": "#55D6BE"
    }
else:
    colors = {
        "background": "#FFFFFF",
        "secondary": "#F4F6F9",
        "message": "#F0F4F8",
        "text": "#17202A",
        "muted": "#475569",
        "border": "#D1D9E0",
        "input": "#FFFFFF",
        "button": "#E8EEF5",
        "hover": "#D9E4EF",
        "accent": "#087F6A"
    }

css = """
<style>
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
[data-testid="stHeader"] {
    background-color: __BG__ !important;
    color: __TEXT__ !important;
}

[data-testid="stSidebar"],
[data-testid="stSidebar"] > div {
    background-color: __SECONDARY__ !important;
    color: __TEXT__ !important;
}

html, body, p, span, label, li, h1, h2, h3, h4,
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] p {
    color: __TEXT__;
}

[data-testid="stChatMessage"] {
    background-color: __MESSAGE__ !important;
    border: 1px solid __BORDER__ !important;
    border-radius: 14px !important;
    padding: 14px !important;
    margin-bottom: 12px !important;
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] span,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] strong,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
    color: __TEXT__ !important;
}

[data-testid="stChatInput"],
[data-testid="stChatInput"] > div,
[data-testid="stChatInput"] > div > div {
    background-color: __INPUT__ !important;
    border-color: __BORDER__ !important;
    color: __TEXT__ !important;
}

[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"] textarea:focus {
    background-color: __INPUT__ !important;
    color: __TEXT__ !important;
    -webkit-text-fill-color: __TEXT__ !important;
    caret-color: __TEXT__ !important;
    border-color: __BORDER__ !important;
    box-shadow: none !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: __MUTED__ !important;
    -webkit-text-fill-color: __MUTED__ !important;
    opacity: 1 !important;
}

[data-testid="stChatInput"] button {
    background-color: __BUTTON__ !important;
    color: __TEXT__ !important;
    border: 1px solid __BORDER__ !important;
}

[data-testid="stChatInput"] button:hover {
    background-color: __HOVER__ !important;
}

[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background-color: __INPUT__ !important;
    color: __TEXT__ !important;
    -webkit-text-fill-color: __TEXT__ !important;
    border-color: __BORDER__ !important;
}

[data-baseweb="select"] > div {
    background-color: __INPUT__ !important;
    color: __TEXT__ !important;
    border-color: __BORDER__ !important;
}

[data-baseweb="select"] span,
[data-baseweb="select"] input {
    color: __TEXT__ !important;
}

[data-baseweb="popover"],
[data-baseweb="menu"],
[data-baseweb="menu"] li {
    background-color: __SECONDARY__ !important;
    color: __TEXT__ !important;
}

.stButton > button {
    background-color: __BUTTON__ !important;
    color: __TEXT__ !important;
    border: 1px solid __BORDER__ !important;
    border-radius: 10px !important;
}

.stButton > button:hover {
    background-color: __HOVER__ !important;
    color: __TEXT__ !important;
    border-color: __ACCENT__ !important;
}

hr {
    border-color: __BORDER__ !important;
}

a {
    color: __ACCENT__ !important;
}

[data-testid="stAlert"] {
    background-color: __SECONDARY__ !important;
    color: __TEXT__ !important;
    border-color: __BORDER__ !important;
}

footer {
    visibility: hidden;
}
</style>
"""

replacements = {
    "__BG__": colors["background"],
    "__SECONDARY__": colors["secondary"],
    "__MESSAGE__": colors["message"],
    "__TEXT__": colors["text"],
    "__MUTED__": colors["muted"],
    "__BORDER__": colors["border"],
    "__INPUT__": colors["input"],
    "__BUTTON__": colors["button"],
    "__HOVER__": colors["hover"],
    "__ACCENT__": colors["accent"]
}

for key, value in replacements.items():
    css = css.replace(key, value)

st.markdown(css, unsafe_allow_html=True)

# ==================================================
# LOCAL FALLBACK RESPONSES
# (used when AWS Bedrock is unavailable or access is denied)
# ==================================================

import re as _re

def _normalise(text: str) -> str:
    """Lowercase, strip punctuation, and pad with spaces so whole-word checks work."""
    cleaned = _re.sub(r"[^\w\s\u0B80-\u0BFF]", " ", text.lower())
    # Collapse multiple spaces and pad both ends so ' hi ' matches at boundaries
    return " " + _re.sub(r"\s+", " ", cleaned).strip() + " "

def _kw_match(normalised: str, keyword: str) -> bool:
    """Match keyword as a whole word (space-padded) to prevent 'hi' matching 'things'."""
    # Short words (≤3 chars) are checked as whole words; longer ones as substrings.
    if len(keyword) <= 3:
        return (" " + keyword + " ") in normalised
    return keyword in normalised

# Keyword rules — checked top to bottom; first match wins.
# More specific emotional states come before broader topic buckets.
# Each entry: (tuple-of-keywords, response-key)
_KEYWORD_RULES = [
    # Greetings — short words like "hi" use whole-word matching via _kw_match
    (("hello", "hi", "hey", "good morning", "good afternoon", "good evening",
      "வணக்கம்", "நமஸ்தே"),                                                       "greeting"),
    # Emotional: confusion (checked before generic "memory" words)
    (("confused", "confusing", "dont understand", "don't understand",
      "not understanding", "குழப்பம்", "குழப்பமாக", "புரியவில்லை"),             "confused"),
    # Emotional: sadness
    (("sad", "unhappy", "upset", "crying", "cry", "depressed", "depression",
      "feel bad", "feeling bad", "கஷ்டம்", "சோகம்", "சோகமாக", "அழுகிறேன்"),    "sad"),
    # Emotional: loneliness
    (("lonely", "alone", "no one", "nobody", "isolated", "loneliness",
      "தனிமை", "தனியாக", "யாரும் இல்லை"),                                        "lonely"),
    # Forgetfulness (specific: "keep forgetting", "forgot", "can't remember")
    (("forget", "forgot", "forgetting", "cant remember", "can't remember",
      "keep forgetting", "மறந்து", "மறந்துவிட்டேன்", "நினைவில்லை"),             "forgetting"),
    # Medicine / medication
    (("medicine", "medication", "pill", "tablet", "dose", "dosage", "pharmacy",
      "மருந்து", "மாத்திரை", "டோஸ்", "மருந்தகம்"),                               "medicine"),
    # Daily routine / tasks
    (("task", "routine", "daily", "schedule", "reminder", "checklist",
      "plan my day", "வேலை", "அட்டவணை", "தினசரி", "நினைவூட்டல்"),              "routine"),
    # Memory exercises / activities
    (("exercise", "activity", "game", "puzzle", "music", "hobby", "garden",
      "பயிற்சி", "செயல்பாடு", "விளையாட்டு", "இசை", "தோட்டம்"),                 "exercise"),
    # Family / contacts / emergency help
    (("family", "contact", "emergency", "call", "phone", "caregiver",
      "குடும்பம்", "தொடர்பு", "அவசரம்", "அழைப்பு", "பராமரிப்பாளர்"),           "family"),
    # General memory support (broader fallback within memory topic)
    (("memory", "remember", "recollect", "mind", "brain",
      "நினைவு", "நினைவாற்றல்"),                                                   "memory"),
    # Asking for help (catch-all help request before true fallback)
    (("help", "assist", "support", "உதவி", "உதவுங்கள்"),                         "family"),
]

LOCAL_RESPONSES = {
    "greeting": {
        "en": (
            "👋 **Hello! Welcome to Ninaivu Thunai.** *(local assistance — not AI-generated)*\n\n"
            "I am here to help you with daily reminders, memory tips, and gentle support.\n\n"
            "What would you like help with today? You can ask me about:\n"
            "- Your daily tasks or schedule\n"
            "- Medicine reminders\n"
            "- Memory activities\n"
            "- Reaching a family member or caregiver"
        ),
        "ta": (
            "👋 **வணக்கம்! நினைவுத் துணைக்கு வரவேற்கிறோம்.** *(உள்ளூர் உதவி — AI உருவாக்கியது அல்ல)*\n\n"
            "அன்றாட நினைவூட்டல்கள், நினைவாற்றல் குறிப்புகள், மற்றும் அன்பான உதவிகளுக்காக நான் இங்கே இருக்கிறேன்.\n\n"
            "இன்று உங்களுக்கு எதில் உதவி தேவை? கேட்கலாம்:\n"
            "- அன்றாட வேலைகள் அல்லது அட்டவணை\n"
            "- மருந்து நினைவூட்டல்கள்\n"
            "- நினைவாற்றல் செயல்பாடுகள்\n"
            "- குடும்பத்தினர் அல்லது பராமரிப்பாளரை அணுகுவது"
        ),
    },
    "confused": {
        "en": (
            "🤗 **It's okay to feel confused sometimes.** *(local assistance — not AI-generated)*\n\n"
            "Let's take one step at a time — there is no rush.\n\n"
            "Can you tell me a little more about what is confusing you right now? "
            "For example:\n"
            "- Are you unsure what day or time it is?\n"
            "- Are you having trouble remembering a task?\n"
            "- Is something around you not feeling familiar?\n\n"
            "If you need help with something nearby, consider asking a trusted family member or caregiver. "
            "They are there to support you.\n\n"
            "*(Source: NIA Communication guidance)*"
        ),
        "ta": (
            "🤗 **சில நேரம் குழப்பமாக உணர்வது இயல்பானது.** *(உள்ளூர் உதவி — AI உருவாக்கியது அல்ல)*\n\n"
            "ஒரு படி ஒரு படியாக போகலாம் — அவசரப்பட வேண்டாம்.\n\n"
            "இப்போது உங்களுக்கு எது குழப்பமாக இருக்கிறது என்று கொஞ்சம் சொல்ல முடியுமா? "
            "உதாரணமாக:\n"
            "- இன்று என்ன நாள் அல்லது நேரம் என்று தெரியவில்லையா?\n"
            "- ஒரு வேலையை நினைவில் வைத்துக்கொள்வதில் சிரமம் உள்ளதா?\n"
            "- சுற்றியுள்ள ஒன்று பழக்கமில்லாமல் தோன்றுகிறதா?\n\n"
            "அருகில் உள்ள நம்பகமான குடும்பத்தினர் அல்லது பராமரிப்பாளரிடம் உதவி கேட்கலாம். "
            "அவர்கள் உங்களுக்கு உதவ இங்கே இருக்கிறார்கள்.\n\n"
            "*(ஆதாரம்: NIA தொடர்பு வழிகாட்டுதல்)*"
        ),
    },
    "sad": {
        "en": (
            "💙 **I hear you — it's okay to feel sad.** *(local assistance — not AI-generated)*\n\n"
            "Your feelings matter, and you are not alone.\n\n"
            "A few gentle things that may help:\n"
            "- Spend a little time with a family member or a friend you trust.\n"
            "- Listen to music you enjoy, or sit in a comfortable, familiar spot.\n"
            "- A short, gentle walk outside can sometimes lift the mood.\n\n"
            "If feelings of sadness continue for a long time, please let a family member "
            "or your doctor know — they can help.\n\n"
            "*(Source: WHO Dementia caregiver guidance)*"
        ),
        "ta": (
            "💙 **நான் கேட்கிறேன் — சோகமாக உணர்வது இயல்பானது.** *(உள்ளூர் உதவி — AI உருவாக்கியது அல்ல)*\n\n"
            "உங்கள் உணர்வுகள் முக்கியம், நீங்கள் தனியில்லை.\n\n"
            "உதவக்கூடிய சில அன்பான வழிகள்:\n"
            "- நம்பகமான குடும்பத்தினர் அல்லது நண்பருடன் சிறிது நேரம் செலவிடுங்கள்.\n"
            "- மனதிற்கு பிடித்த இசை கேளுங்கள், அல்லது பழக்கமான வசதியான இடத்தில் அமருங்கள்.\n"
            "- வெளியே லேசான, அமைதியான நடை சில நேரங்களில் மனநிலையை மேம்படுத்தும்.\n\n"
            "சோகம் நீண்ட நேரம் தொடர்ந்தால், குடும்பத்தினர் அல்லது மருத்துவரிடம் தெரிவியுங்கள் — "
            "அவர்கள் உதவுவார்கள்.\n\n"
            "*(ஆதாரம்: WHO டிமென்ஷியா பராமரிப்பாளர் வழிகாட்டுதல்)*"
        ),
    },
    "lonely": {
        "en": (
            "🌸 **Feeling lonely is hard — I'm glad you reached out.** *(local assistance — not AI-generated)*\n\n"
            "Staying connected with others is good for both memory and mood.\n\n"
            "A few ideas:\n"
            "- Call or message a family member or friend today, even just to say hello.\n"
            "- If you enjoy it, look through old family photos — it can bring warm memories.\n"
            "- A caregiver or trusted neighbour can be good company too.\n\n"
            "You do not have to feel lonely alone. Please reach out to someone near you.\n\n"
            "*(Source: WHO Dementia caregiver guidance)*"
        ),
        "ta": (
            "🌸 **தனிமையாக உணர்வது கஷ்டமானது — நீங்கள் தொடர்பு கொண்டதற்கு மகிழ்ச்சி.** *(உள்ளூர் உதவி — AI உருவாக்கியது அல்ல)*\n\n"
            "மற்றவர்களுடன் தொடர்பில் இருப்பது நினைவாற்றலுக்கும் மனநிலைக்கும் நல்லது.\n\n"
            "சில யோசனைகள்:\n"
            "- இன்றே ஒரு குடும்பத்தினர் அல்லது நண்பரை அழையுங்கள் — வெறும் வணக்கம் சொல்வதே போதும்.\n"
            "- பழைய குடும்ப புகைப்படங்களை பாருங்கள் — அது அன்பான நினைவுகளை கொண்டுவரும்.\n"
            "- பராமரிப்பாளர் அல்லது நம்பகமான அண்டை வீட்டினரும் நல்ல தோழமையாக இருப்பார்கள்.\n\n"
            "தனிமையை தனியாக அனுபவிக்க வேண்டாம். அருகில் உள்ள யாரையாவது அணுகுங்கள்.\n\n"
            "*(ஆதாரம்: WHO டிமென்ஷியா பராமரிப்பாளர் வழிகாட்டுதல்)*"
        ),
    },
    "forgetting": {
        "en": (
            "🧠 **Forgetting things can be frustrating — you are not alone in this.** *(local assistance — not AI-generated)*\n\n"
            "Here are some gentle strategies that can help:\n\n"
            "- **Write it down straight away** — keep a small notebook or sticky notes near you.\n"
            "- **Same place, every time** — put keys, glasses, and important items in one fixed spot.\n"
            "- **Daily routine** — doing things in the same order each day makes them easier to remember.\n"
            "- **Ask for a reminder** — a family member or caregiver can give you a gentle prompt.\n\n"
            "If forgetting is affecting your daily life more than before, it is worth mentioning to your doctor.\n\n"
            "*(Source: WHO Dementia fact sheet)*"
        ),
        "ta": (
            "🧠 **தினமும் மறந்துவிடுவது வருத்தமாக இருக்கும் — இது உங்களுக்கு மட்டுமல்ல.** *(உள்ளூர் உதவி — AI உருவாக்கியது அல்ல)*\n\n"
            "உதவக்கூடிய சில எளிய வழிகள்:\n\n"
            "- **உடனே எழுதுங்கள்** — சிறிய நோட்புக் அல்லது ஸ்டிக்கி குறிப்புகளை அருகில் வையுங்கள்.\n"
            "- **ஒரே இடம், எப்போதும்** — சாவி, கண்ணாடி, முக்கியமான பொருட்களை ஒரே நிலையான இடத்தில் வையுங்கள்.\n"
            "- **தினசரி அட்டவணை** — ஒவ்வொரு நாளும் ஒரே வரிசையில் செய்தால் நினைவில் வைக்க எளிதாக இருக்கும்.\n"
            "- **நினைவூட்டல் கேளுங்கள்** — குடும்பத்தினர் அல்லது பராமரிப்பாளர் லேசாக நினைவூட்டலாம்.\n\n"
            "மறதி முன்பை விட அதிகமாக அன்றாட வாழ்க்கையை பாதிக்கிறது என்றால், மருத்துவரிடம் சொல்வது நல்லது.\n\n"
            "*(ஆதாரம்: WHO டிமென்ஷியா உண்மைத்தாள்)*"
        ),
    },
    "routine": {
        "en": (
            "📋 **Daily task tips** *(local assistance — not AI-generated)*\n\n"
            "- Write tomorrow's tasks on paper or a calendar before you sleep.\n"
            "- Keep a fixed time for meals, medicines, and rest every day.\n"
            "- Place important items (keys, glasses, phone) in the same spot always.\n"
            "- A simple checklist on the fridge can help you track what you have done.\n\n"
            "*(Source: WHO Dementia caregiver guidance)*"
        ),
        "ta": (
            "📋 **அன்றாட வேலை குறிப்புகள்** *(உள்ளூர் உதவி — AI உருவாக்கியது அல்ல)*\n\n"
            "- தூங்குவதற்கு முன் நாளைய வேலைகளை காகிதத்தில் அல்லது நாட்காட்டியில் எழுதுங்கள்.\n"
            "- சாப்பிடும் நேரம், மருந்து நேரம், ஓய்வு நேரம் ஒவ்வொரு நாளும் ஒரே நேரத்தில் வையுங்கள்.\n"
            "- முக்கியமான பொருட்களை (சாவி, கண்ணாடி, தொலைபேசி) எப்போதும் ஒரே இடத்தில் வையுங்கள்.\n"
            "- குளிர்சாதன பெட்டியில் ஒரு சோதனைப் பட்டியல் வைத்தால் என்ன செய்தீர்கள் என்று தெரியும்.\n\n"
            "*(ஆதாரம்: WHO டிமென்ஷியா பராமரிப்பாளர் வழிகாட்டுதல்)*"
        ),
    },
    "medicine": {
        "en": (
            "💊 **Medicine reminder guidance** *(local assistance — not AI-generated)*\n\n"
            "- Take medicines only as prescribed by your doctor — do not change the dose yourself.\n"
            "- Set a phone alarm or use a pill organiser to help remember each dose.\n"
            "- If you are unsure whether you took a dose, check your pill organiser or ask a caregiver.\n"
            "- **If a dose was missed or an extra dose was taken, contact your pharmacist or doctor** — "
            "do not try to correct it without professional advice.\n\n"
            "⚠️ *This reminder does not replace advice from your healthcare professional.*\n\n"
            "*(Source: NIA Medicines guidance for caregivers)*"
        ),
        "ta": (
            "💊 **மருந்து நினைவூட்டல் வழிகாட்டுதல்** *(உள்ளூர் உதவி — AI உருவாக்கியது அல்ல)*\n\n"
            "- மருத்துவர் சொன்னபடி மட்டுமே மருந்து எடுங்கள் — அளவை நீங்களாக மாற்றாதீர்கள்.\n"
            "- ஒவ்வொரு மருந்து நேரத்திலும் தொலைபேசி அலாரம் வையுங்கள் அல்லது மருந்து பெட்டி பயன்படுத்துங்கள்.\n"
            "- மருந்து எடுத்தீர்களா என்று சந்தேகம் ஏற்பட்டால், மருந்து பெட்டியை சரிபாருங்கள் அல்லது பராமரிப்பாளரிடம் கேளுங்கள்.\n"
            "- **ஒரு மருந்தை தவறவிட்டாலோ அல்லது அதிகமாக எடுத்துவிட்டாலோ, மருந்தாளுனர் அல்லது மருத்துவரை அழையுங்கள்** — "
            "தொழில்முறை ஆலோசனை இல்லாமல் சரி செய்ய முயற்சிக்காதீர்கள்.\n\n"
            "⚠️ *இந்த நினைவூட்டல் உங்கள் சுகாதார நிபுணரின் ஆலோசனைக்கு மாற்றாகாது.*\n\n"
            "*(ஆதாரம்: NIA பராமரிப்பாளர்களுக்கான மருந்து வழிகாட்டுதல்)*"
        ),
    },
    "exercise": {
        "en": (
            "🎵 **Memory exercises and activities** *(local assistance — not AI-generated)*\n\n"
            "- Familiar music, light gardening, and simple household tasks can be enjoyable.\n"
            "- Short walks, puzzles, or looking through family photos may help keep the mind active.\n"
            "- Choose activities that match your current abilities — stop or adjust if they cause frustration.\n"
            "- Shared conversations and time with family are also very beneficial.\n\n"
            "*(Source: NIA Activities guidance)*"
        ),
        "ta": (
            "🎵 **நினைவாற்றல் பயிற்சிகள் மற்றும் செயல்பாடுகள்** *(உள்ளூர் உதவி — AI உருவாக்கியது அல்ல)*\n\n"
            "- பழக்கமான இசை, லேசான தோட்ட வேலை, எளிய வீட்டு வேலைகள் மகிழ்ச்சி அளிக்கும்.\n"
            "- குறுகிய நடை, புதிர்கள், அல்லது குடும்ப புகைப்படங்களை பார்ப்பது மனதை சுறுசுறுப்பாக வைக்கலாம்.\n"
            "- உங்கள் தற்போதைய திறன்களுக்கு ஏற்ற செயல்பாடுகளை தேர்ந்தெடுங்கள் — விரக்தி ஏற்பட்டால் நிறுத்துங்கள்.\n"
            "- குடும்பத்தினருடன் உரையாடல் மற்றும் சமூக நேரமும் மிகவும் நன்மை அளிக்கும்.\n\n"
            "*(ஆதாரம்: NIA செயல்பாடுகள் வழிகாட்டுதல்)*"
        ),
    },
    "family": {
        "en": (
            "📞 **Reaching family or getting help** *(local assistance — not AI-generated)*\n\n"
            "- Keep a written list of family contacts, your doctor, and a local emergency number near the phone.\n"
            "- In a medical emergency, call your local emergency services immediately.\n"
            "- Let a trusted family member or caregiver know your daily schedule so they can check in.\n"
            "- If you feel unsafe or unwell, contact a trusted person straight away — do not wait.\n\n"
            "⚠️ *This app does not store or dial contacts. Please save numbers in your phone directly.*"
        ),
        "ta": (
            "📞 **குடும்பத்தினரை அடைவது அல்லது உதவி பெறுவது** *(உள்ளூர் உதவி — AI உருவாக்கியது அல்ல)*\n\n"
            "- குடும்பத்தினர், மருத்துவர், மற்றும் உள்ளூர் அவசர எண்ணை தொலைபேசி அருகில் எழுதி வையுங்கள்.\n"
            "- மருத்துவ அவசரநிலையில் உடனடியாக உள்ளூர் அவசர சேவைகளை அழையுங்கள்.\n"
            "- நம்பகமான குடும்பத்தினர் அல்லது பராமரிப்பாளருக்கு உங்கள் தினசரி அட்டவணையை தெரியப்படுத்துங்கள்.\n"
            "- பாதுகாப்பற்றதாக அல்லது உடல்நலமற்றதாக உணர்ந்தால், நம்பகமான ஒருவரை உடனே தொடர்பு கொள்ளுங்கள்.\n\n"
            "⚠️ *இந்த செயலி தொடர்புகளை சேமிக்கவோ அழைக்கவோ செய்யாது. எண்களை நேரடியாக உங்கள் தொலைபேசியில் சேமிக்கவும்.*"
        ),
    },
    "memory": {
        "en": (
            "🧠 **Memory support** *(local assistance — not AI-generated)*\n\n"
            "- Written notes, calendars, and sticky reminders help keep track of daily tasks.\n"
            "- A consistent daily routine makes it easier to remember what comes next.\n"
            "- Staying socially connected — talking with family and friends — supports memory and mood.\n"
            "- If memory changes are affecting daily life, speak to a healthcare professional.\n\n"
            "*(Source: WHO Dementia fact sheet)*"
        ),
        "ta": (
            "🧠 **நினைவாற்றல் உதவி** *(உள்ளூர் உதவி — AI உருவாக்கியது அல்ல)*\n\n"
            "- எழுதிய குறிப்புகள், நாட்காட்டிகள், மற்றும் ஸ்டிக்கி நினைவூட்டல்கள் தினசரி வேலைகளை கண்காணிக்க உதவும்.\n"
            "- ஒரே மாதிரியான தினசரி அட்டவணையை பின்பற்றுவது அடுத்து என்ன செய்வது என்பதை நினைவில் வைக்க உதவும்.\n"
            "- குடும்பம் மற்றும் நண்பர்களுடன் தொடர்பில் இருப்பது நினைவாற்றலுக்கும் மனநிலைக்கும் உதவும்.\n"
            "- நினைவாற்றல் மாற்றங்கள் அன்றாட வாழ்க்கையை பாதிக்கின்றன என்றால், சுகாதார நிபுணரிடம் பேசுங்கள்.\n\n"
            "*(ஆதாரம்: WHO டிமென்ஷியா உண்மைத்தாள்)*"
        ),
    },
    # Short fallback — does NOT repeat the full topic list
    "general": {
        "en": (
            "🤝 **I'm here to help.** *(local assistance — not AI-generated)*\n\n"
            "Could you tell me a little more about what you need? "
            "For example, are you looking for help with a daily task, a medicine reminder, "
            "or do you just want to talk?"
        ),
        "ta": (
            "🤝 **நான் உதவ இங்கே இருக்கிறேன்.** *(உள்ளூர் உதவி — AI உருவாக்கியது அல்ல)*\n\n"
            "உங்களுக்கு என்ன தேவை என்று கொஞ்சம் சொல்ல முடியுமா? "
            "உதாரணமாக, அன்றாட வேலைகளுக்கு உதவி வேண்டுமா, மருந்து நினைவூட்டல் வேண்டுமா, "
            "அல்லது பேசவா விரும்புகிறீர்கள்?"
        ),
    },
}

# Errors that signal AWS is unavailable rather than a logic bug.
_AWS_UNAVAILABLE_ERRORS = (
    "ValidationException",
    "AccessDeniedException",
    "UnauthorizedException",
    "Operation not allowed",
    "credential",
    "token",
    "expired",
    "Bedrock",
    "bedrock",
    "AuthorizationError",
    "not authorized",
    "NoCredentialsError",
    "EndpointConnectionError",
    "ConnectTimeoutError",
)


def _local_response(message: str, language: str) -> str:
    """Return a response matched by keyword after normalising the message."""
    normalised = _normalise(message)
    lang_code = "ta" if language == "தமிழ்" else "en"
    for keywords, key in _KEYWORD_RULES:
        if any(_kw_match(normalised, kw) for kw in keywords):
            return LOCAL_RESPONSES[key][lang_code]
    return LOCAL_RESPONSES["general"][lang_code]


def _is_aws_unavailable(exc: Exception) -> bool:
    """Return True when the exception indicates AWS/Bedrock is unreachable or access is denied."""
    msg = str(exc)
    return any(marker in msg for marker in _AWS_UNAVAILABLE_ERRORS)


# ==================================================
# STRANDS AGENT RESPONSE FUNCTION
# ==================================================

def get_response(message, language):
    lang_code = "ta" if language == "தமிழ்" else "en"

    # --- Try the Strands agent (requires AWS Bedrock) ---
    try:
        result = run_strands_agent({"text": message, "lang": lang_code})
        answer = result.get("plan", {}).get("answer", "")
        if answer:
            return answer
        # Agent returned nothing — fall through to local
    except Exception as exc:
        if not _is_aws_unavailable(exc):
            # Unexpected error: surface a safe message without leaking details
            return (
                "மன்னிக்கவும், ஒரு எதிர்பாராத பிழை ஏற்பட்டது. மீண்டும் முயற்சிக்கவும்."
                if language == "தமிழ்"
                else "Sorry, an unexpected error occurred. Please try again."
            )
        # AWS unavailable — fall through to local fallback

    # --- Local fallback (no AWS needed) ---
    return _local_response(message, language)


# ==================================================
# CHAT PAGE
# ==================================================

st.title(t["title"])
st.caption(t["subtitle"])
st.divider()
st.subheader(t["chat"])

# Show welcome and suggestions before the first message
if not st.session_state.messages:
    st.info(t["welcome"])
    st.write(f"**{t['suggestions']}**")

    col1, col2, col3 = st.columns(3)

    selected_question = None

    with col1:
        if st.button("💡 " + t["suggestion1"], use_container_width=True):
            selected_question = t["suggestion1"]

    with col2:
        if st.button("💊 " + t["suggestion2"], use_container_width=True):
            selected_question = t["suggestion2"]

    with col3:
        if st.button("🩺 " + t["suggestion3"], use_container_width=True):
            selected_question = t["suggestion3"]

    # IMPORTANT: Generate the answer before rerunning
    if selected_question:
        response = get_response(selected_question, language)

        st.session_state.messages.append({
            "role": "user",
            "content": selected_question
        })

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

        st.rerun()

# Display all saved messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept typed messages
user_input = st.chat_input(t["placeholder"])

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    response = get_response(user_input, language)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    st.rerun()

# Safety notice
st.divider()
st.caption(t["safety"])