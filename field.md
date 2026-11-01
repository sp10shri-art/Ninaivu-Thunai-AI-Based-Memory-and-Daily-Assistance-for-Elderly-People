# Builder Center Article — Field Values
# Ninaivu Thunai: AI-Based Cognitive Gaming and Memory Assistance Platform

These are the metadata fields to fill in on the AWS Builder Center article submission form.
Do not change the values below without re-checking them against the live project.

---

## Title
Ninaivu Thunai — AI-Based Memory and Daily Assistance for Elderly People

## Subtitle / Tagline
A Tamil-first memory companion that provides gentle daily reminders and guidance
for older adults and their caregivers, with a safe local fallback when AI is unavailable.

## Category
Health

## Tags
- strands-agents
- social-good
- tamil
- elderly-care
- dementia
- memory-assistance
- accessibility

## Domain / Focus Area
Health

## Social-Good Population Served
Elderly adults experiencing memory difficulties, and their family caregivers,
particularly in Tamil-speaking communities in India.

## Programming Language(s)
Python

## AWS Services Used
- Amazon Bedrock (intended model: Amazon Nova 2 Lite via India cross-region inference profile)
- Amazon Translate (tested; used for language detection fallback)
- AWS SDK for Python (boto3)

## Strands SDK Blocks Used
- tools         (lookup_guidance — read-only curated guidance)
- graph         (planner → critic graph with loop-breaking condition)
- hooks         (RedFlagGate: BeforeNodeCallEvent cancels agents on dangerous phrases)
- structured_output (Answer and Critique Pydantic models)

## Repository Link
[To be added — make the repo public inside the submission window]

## Demo Video Link
[To be added — record with `ss video` and upload to YouTube]

## Article Status
Draft — review before publishing on Builder Center

## Submission Deadline
4 Nov 2026 11:59 PM PST (5 Nov 2026 1:29 PM IST)

---

## Notes for the Submitter
- Replace all [To be added] lines above before publishing.
- Do not paste AWS account IDs, access keys, or region-specific ARNs into the article.
- The repo must be public at the time of submission but was kept private during development.
- Measurement results are not yet available (AWS Bedrock access was blocked during testing).
  Do not include performance numbers until `ss measure` completes successfully.
