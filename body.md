# Ninaivu Thunai — AI-Based Memory and Daily Assistance for Elderly People

> **"Ninaivu Thunai"** means *memory companion* in Tamil.
> Built for the AWS Strands SDK: Workshop to Ship hackathon — Health category.

---

## The Problem

Memory loss is one of the most common challenges that elderly people and their families face.
Even before a formal diagnosis, an older person may start forgetting daily tasks, medicines,
or important appointments. This creates stress for the person and for everyone who looks after them.

In Tamil-speaking households across India, including in the North Eastern Region (NER) where
many families live far from specialist medical services, the challenge is even harder.
Most digital tools for memory support are in English. A caregiver who speaks Tamil, or an elderly
person who is more comfortable in their native language, often cannot use these tools effectively.

I built Ninaivu Thunai because I wanted to create something that could genuinely help in that situation:
a friendly assistant that speaks the user's language, provides honest and clear guidance, and
knows when to step back and direct someone to a qualified person.

---

## Who It Is For

- **Elderly adults** who need gentle reminders for daily routines, medicines, and activities.
- **Family caregivers** who want to support a parent or grandparent and need practical guidance
  on communication, activities, and home safety.
- **Tamil-speaking users** who prefer to interact in Tamil rather than English.

This application is not a medical device. It does not diagnose conditions, prescribe medicines,
or replace a doctor or caregiver. It provides general support and escalates to a qualified person
when the situation requires it.

---

## What Ninaivu Thunai Does

### Daily Routines and Task Reminders

The assistant helps users think about their day: writing tasks down, keeping a fixed schedule,
placing important items in the same spot, and using simple checklists. These strategies are
drawn from WHO caregiver guidance on supporting people with dementia.

### Medicine Reminder Guidance

The assistant reminds users to take medicines as prescribed and to use a pill organiser or
phone alarm. It is clear about what it cannot do: it does not suggest doses, recommend
changing a prescription, or advise on missed doses without directing the user to their
pharmacist or doctor first. If a user asks whether to double a dose or has already taken too
much, a hard safety gate cancels the agent entirely and returns a fixed hand-off message.
This behaviour is in code, not decided by the language model at runtime.

### Memory Exercises and Activities

The assistant suggests familiar activities that may support wellbeing and engagement: listening
to music, light gardening, short walks, puzzles, and looking through family photos. These are
drawn from NIA guidance on activities for people with Alzheimer's disease.

### Emotional Support

When a user says they feel confused, sad, or lonely, the assistant responds gently and with
warmth. It does not diagnose or prescribe. It acknowledges the feeling, offers a practical
suggestion, and encourages the user to reach out to a trusted family member or caregiver.

### Family Contacts and Emergency Assistance

The assistant reminds users to keep written contact lists near the phone and to call local
emergency services in a medical emergency. The application itself does not store or dial contacts.

### English and Tamil Language Support

The user can switch between English and Tamil at any time using a language selector in the
sidebar. All guidance responses, safety messages, and hand-off messages are written in both
languages. Language detection is also applied automatically based on the script of the input.

---

## Architecture

```
User (Streamlit UI)
        │
        ▼
  get_response()  ──── try Strands Agent ──── Amazon Bedrock (Nova 2 Lite)
        │                                              │
        │              planner Agent ◄──► critic Agent
        │              (GraphBuilder loop, max 2 passes)
        │                      │
        │              RedFlagGate (Hook)
        │              BeforeNodeCallEvent cancels on red-flag phrases
        │                      │
        │              lookup_guidance (tool)
        │              reads agent/data/guidance.json (curated, dated)
        │
        │  (if Bedrock unavailable)
        ▼
  _local_response()  ── keyword match ── canned responses (both languages)
```

### Streamlit Interface (`ui.py`)

The interface is a single-page chat application built with Streamlit. It has:
- A language selector (English / Tamil) and a dark/light appearance toggle in the sidebar.
- A chat history stored in Streamlit session state.
- Three suggestion buttons on the welcome screen for common questions.
- A safety notice at the bottom of the page.

When the user sends a message, `get_response()` is called. It first tries to call the
Strands Agent. If the agent returns an answer, that answer is displayed. If AWS Bedrock is
unavailable or access is denied, the function silently falls back to a local keyword-matched
response.

### Strands Agent (`agent/app.py`)

The Strands Agent uses the Strands Agents SDK with a planner → critic graph:

1. **Planner Agent** receives the user's message, calls `lookup_guidance` to retrieve
   relevant items from the curated guidance file, and produces a structured `Answer`
   (language, answer text, steps, escalation message, and citation IDs).
2. **Critic Agent** checks the planner's answer: wrong language, unsupported advice,
   uncited claims, or empty responses cause the critic to return `ok=false`, and the
   planner is called again. The loop runs at most twice.
3. **RedFlagGate Hook** is registered on `BeforeNodeCallEvent`. Before each node runs,
   it checks the user's message for dangerous phrases (dose doubling, overdose, chest pain,
   and Tamil equivalents). If any phrase matches, the hook cancels the node and the agent
   returns a fixed hand-off message written in code — not generated by the model.

### Curated Guidance (`agent/data/guidance.json`)

All factual content that the agent may cite comes from a curated JSON file. Each item has:
- A stable ID (for citation checking)
- A source (WHO or NIA document, with URL and review date)
- A paraphrased summary

The agent is instructed to cite only IDs returned by `lookup_guidance`. The critic checks
that no uncited IDs appear in the answer. This prevents the model from inventing guidance.

### Local Fallback (`ui.py`)

When AWS Bedrock returns a `ValidationException`, `AccessDeniedException`, or any
credential or network error, the application falls back to local keyword-matched responses.
These responses are plain strings written in the code — they are not generated by a language
model. The fallback covers:
- Greetings
- Confusion, sadness, and loneliness (emotional states)
- Forgetfulness
- Medicine reminders
- Daily routines
- Memory exercises
- Family contacts and emergencies
- A brief general fallback for unmatched messages

Every fallback response is labelled **"local assistance — not AI-generated"** so the user
is never misled about what they are receiving.

---

## Test Cases

The project includes 30 labelled test cases in `cases.jsonl`, covering six job categories
in both English and Tamil:

| Category           | Cases | Languages   |
|--------------------|-------|-------------|
| Daily reminders    | 6     | en + ta     |
| Memory support     | 6     | en + ta     |
| Home safety        | 6     | en + ta     |
| Medicine safety    | 6     | en + ta     |
| Caregiver support  | 4     | en + ta     |
| Healthcare support | 4     | en + ta     |

Medicine-safety cases and the chest-pain case are marked `"escalation": "emergency"`.
The scoring logic in `agent/score.py` checks whether these cases were handled by the
red-flag hook (hard hand-off) rather than answered by the model.

---

## Current Status and Limitations

**What works today:**

- The Streamlit interface, including language switching, dark mode, and chat history.
- The local fallback, which provides relevant keyword-matched responses in both languages.
- The safety gate logic and hand-off messages are implemented in code.
- The curated guidance file is complete with WHO and NIA sources.
- The test cases are written and signed.
- Python syntax is verified.

**What is not yet complete:**

- **AWS Bedrock access is blocked.** During testing, the configured model
  (`in.amazon.nova-2-lite-v1:0` in `ap-south-2`) returned a `ValidationException: Operation not allowed`
  error. The full planner → critic agent path has not been tested with a live model call.
  No AI-generated responses have been verified in production.

- **Measurement has not run.** The `ss measure` command compares the Strands Agent against
  a single-prompt baseline on the labelled cases. Because Bedrock access is blocked, this
  comparison has not been completed. No accuracy, recall, or safety scores are reported in
  this article.

- **The demo video has not been recorded.** The `ss video` command requires a working agent.

- **FAILURES.md has no entries yet.** At least one real failure must be found, fixed, and
  logged before the submission check passes.

---

## What I Learned

Building Ninaivu Thunai taught me several things.

**Separating safety from the model is not optional.** The most important decision I made was
to put the dangerous-phrase check in a Strands Hook rather than in the model's system prompt.
A system prompt can be overridden, misunderstood, or missed. A `BeforeNodeCallEvent` hook
that cancels the node and returns a fixed string is deterministic. The user always receives
the same hand-off message for a dangerous question, regardless of what the model might have
said.

**A local fallback is not a workaround — it is part of accessibility.** When I realised that
Bedrock access was blocked, I had a choice: show an error, or provide something genuinely
useful. I chose to write careful, specific responses for the situations an elderly user is
most likely to face. The result is that the application is usable today, even without a
working cloud model. For users in areas with unreliable internet, this matters.

**Language support requires more than translation.** Writing Tamil responses is not just
about translating English text. The tone, the level of formality, and the emotional register
all need to be right for the audience. I wrote the Tamil responses carefully and checked
that they convey the same warmth and clarity as the English versions.

**Honest error handling builds trust.** I chose not to hide errors or pretend that AI
responses were working when they were not. Every local fallback response is clearly labelled.
This is especially important in a health-adjacent application, where a user might otherwise
make decisions based on what they think is AI guidance.

---

## What I Plan to Improve

1. **Resolve Bedrock access** and run the full planner → critic agent path end to end.
2. **Run `ss measure`** and report honest accuracy and safety scores in this article.
3. **Record the demo video** showing both a normal question and a medicine-safety hand-off.
4. **Log at least one real failure** in FAILURES.md with before-and-after scores.
5. **Expand the guidance data** with more practical items for common caregiving scenarios
   in the Indian context.
6. **Improve Tamil coverage** in the test cases and the scoring logic.

---

## How to Run

```bash
# 1. Install Python 3.12 and clone the repository
# 2. Create a virtual environment
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate  # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure AWS credentials (in your own terminal — do not paste keys here)
aws configure
# or: aws sso login

# 5. Set the region and model (edit .env or set environment variables)
# AWS_REGION=ap-south-2
# SHIP_MODEL=in.amazon.nova-2-lite-v1:0

# 6. Run the Streamlit interface
streamlit run ui.py

# 7. Run the agent from the command line
python -m agent.app "How can I remember my daily tasks?"
```

AWS Bedrock model access must be enabled in the Bedrock console (Model access) for the
region you are using. The default model (`in.amazon.nova-2-lite-v1:0`) requires Amazon Nova
to be enabled in `ap-south-2`.

---

## Repository

[Link to be added — make the repo public inside the submission window]

## Demo Video

[Link to be added — upload to YouTube before submission]

---

## References

All guidance content is sourced from:

- World Health Organization. *Dementia: Information for caregivers.*
  https://www.who.int/news-room/questions-and-answers/item/dementia-information-for-caregivers
  (reviewed 2026-10-30)
- World Health Organization. *Dementia fact sheet.*
  https://www.who.int/news-room/fact-sheets/detail/dementia
  (reviewed 2026-10-30)
- National Institute on Aging. *Communicating With Someone Who Has Alzheimer's Disease.*
  https://www.nia.nih.gov/health/alzheimers-changes-behavior-and-communication/communicating-someone-who-has-alzheimers
  (reviewed 2026-10-30)
- National Institute on Aging. *Adapting Activities for People With Alzheimer's Disease.*
  https://www.nia.nih.gov/health/alzheimers-caregiving/activities-do-family-member-or-friend-who-has-alzheimers-disease
  (reviewed 2026-10-30)
- National Institute on Aging. *Alzheimer's Caregiving: Home Safety Tips.*
  https://www.nia.nih.gov/health/safety/home-safety-checklist-alzheimers-disease
  (reviewed 2026-10-30)
- National Institute on Aging. *Common Medical Problems in Alzheimer's Disease.*
  https://www.nia.nih.gov/health/alzheimers-caregiving/common-medical-problems-alzheimers-disease-information-caregivers
  (reviewed 2026-10-30)
