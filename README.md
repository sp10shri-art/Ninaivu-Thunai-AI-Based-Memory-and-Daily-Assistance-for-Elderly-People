# Ninaivu Thunai 🧠

**A Tamil-first memory and daily-reminder assistant for older adults and their caregivers.**

## Problem

Older adults experiencing memory difficulties may need help remembering daily routines, following reminders, staying safe at home, and communicating with caregivers. Language barriers can make existing digital tools harder to use.

## Our Solution

Ninaivu Thunai is an AI-agent project designed to provide simple, accessible memory-support guidance in English and Tamil.

The project focuses on:
- Daily routines and reminders
- Memory-support strategies
- Home-safety guidance
- Medication-reminder safety
- Caregiver support
- Healthcare guidance and escalation when professional help is needed

## Who It Helps

- Older adults who need support with everyday routines
- Family members and caregivers
- People who prefer communicating in Tamil

**Important:** Ninaivu Thunai is not a medical device and does not diagnose conditions or prescribe, change, or recommend medication doses. It is intended to provide general support and direct users to qualified people when appropriate.

## Technology

- Python
- Strands Agents SDK
- Amazon Bedrock
- Structured guidance data
- English and Tamil language handling
- Safety checks and answer-scoring logic

## Project Structure

```text
ninaivu-thunai/
├── agent/
│   ├── app.py
│   ├── baseline.py
│   ├── plan.py
│   ├── score.py
│   ├── tools.py
│   └── data/
│       └── guidance.json
├── ship_kit/
├── results/
├── cases.jsonl
├── requirements.txt
├── FAILURES.md
├── SUBMISSION.md
└── README.md
```

## Setup

1. Install Python 3.12.
2. Clone this repository.
3. Create and activate a Python virtual environment.
4. Install the dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

5. Configure AWS credentials and an AWS Region supported by your selected Amazon Bedrock model.
6. Configure the model settings required by the project.
7. Run the project using the commands documented by the Strands Ship Kit.

AWS Bedrock model access must be enabled for the account and model being used. Successful AWS authentication alone does not guarantee model invocation permission.

## Testing and Evaluation

The project includes labelled test cases for English and Tamil, covering daily routines, memory support, home safety, medication safety, caregiver support, and healthcare escalation.

Local checks have been performed for Python syntax and Tamil emergency hand-off scoring.

**Full evaluation results:** Not yet available. The configured Amazon Bedrock model returned an authorization error during testing, so a complete agent-versus-baseline measurement has not been completed.

No performance scores are claimed until the evaluation can run successfully.

## Safety

- Emergency cases should be directed to appropriate human or emergency assistance.
- The assistant must not invent medication doses.
- Diagnosis and treatment decisions should be handled by qualified healthcare professionals.
- Guidance should be simple, accessible, and appropriate to the user's language.

## Hackathon

Built for the Strands SDK: Workshop to Ship hackathon, with a focus on Tamil-language accessibility and social impact.

## Licence

See the `LICENSE` file for licence terms.