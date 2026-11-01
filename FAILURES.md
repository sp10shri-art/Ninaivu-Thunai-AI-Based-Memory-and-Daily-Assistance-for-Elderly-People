# Failures we found and fixed

Judges trust a project that shows what broke. Add one `## ` entry per real failure, newest first.
`ss ship` needs at least one. Keep the numbers from `results/MEASURE.md`, before and after.

<!-- Copy this block for each failure:

## <short name> (<date>)
- What broke: <the case id and what the plan said>
- How we found it: <ss measure / a tester / red-team case>
- What we changed: <file and change>
- After: <the re-measured number>

-->

## All 32 cases crash: Bedrock ConverseStream blocked (2026-11-01)

- **What broke:** Every agent and baseline call failed with
  `ValidationException: An error occurred (ValidationException) when calling the ConverseStream
  operation: Operation not allowed`.
  30 out of 32 agent cases and all 32 baseline cases crashed. The 2 agent cases that did not
  crash (`medicine-en-02`, `health-en-02`) produced partial results only because their emergency
  hand-off was triggered by the `RedFlagGate` hook before any Bedrock call was made, not because
  the model responded successfully.

- **How we found it:** Running `python -m ship_kit measure` on 2026-11-01. The full gate result:
  - Emergency recall: 25% (target 100%) — FAIL
  - Unsafe plans (counted as crashes): 30 agent, 32 baseline — FAIL
  - Key facts present: 6% — FAIL
  - Citation faithfulness: 0% — FAIL
  - Plan completeness: 4% — FAIL
  - Goal success: 0.0 agent, 0.0 baseline — FAIL
  - Crashes: 30 agent, 32 baseline — FAIL
  - Gate overall: NOT PASSED

- **Root cause analysis:**
  There are two compounding issues:

  1. **Wrong model ID in `.env`.** The `.env` file was updated earlier to set
     `AWS_REGION=ap-south-2` and `SHIP_MODEL=in.amazon.nova-2-lite-v1:0` for the India
     cross-region inference profile. However the `.env` file currently contains the original
     US values (`AWS_REGION=us-east-1`, `SHIP_MODEL=us.amazon.nova-2-lite-v1:0`). This means
     `load_dotenv()` in `agent/app.py` loads the wrong region and model ID.

  2. **Bedrock model access not enabled.** Even with the correct region, `ss bedrock` previously
     returned `ValidationException: Operation not allowed`, which means the Amazon Nova model
     has not been enabled in the Bedrock console (Model access) for the configured account and
     region. `ConverseStream` is the streaming inference API called by the Strands SDK; this
     error is Bedrock's way of saying the model is not authorized for this account, not a
     credential expiry.

- **What has been changed so far:**
  - `ship_kit/cli.py`: Fixed the Markdown code-fence syntax error that prevented `ss ship`
    from running at all (2026-11-01).
  - `ui.py`: Added a local keyword-matched fallback so the Streamlit interface remains usable
    while Bedrock access is blocked (2026-10-31).
  - `agent/app.py`: Added `load_dotenv()` before `MODEL_ID`/`REGION` so `.env` values are
    loaded at import time (2026-10-31).
  - **No measurement code, threshold, or raw result has been edited.**

- **What has NOT been changed:**
  - `.env` — the credential values and model ID have not been changed here because fixing
    them requires re-authenticating (`aws sso login` / `aws configure`) and enabling Nova in
    the Bedrock console — actions that must be done by the account owner in their own terminal.
  - `results/MEASURE.md` and `results/measure.json` — these reflect the actual failed run
    and have not been edited.

- **Gate status:** STILL FAILING. The gate cannot pass until Bedrock model access is
  authorized and `ss measure` completes with all cases returning actual model responses.

- **After (re-measured):** Not yet available. Re-run `ss measure` after completing the
  steps in "Next step" below.

- **Next step — required before re-measuring:**
  1. In your own terminal, run `aws sso login` (or `aws configure`) to refresh credentials.
  2. Go to the AWS Bedrock console → **Model access** for your region.
     Enable **Amazon Nova Lite** (model ID `amazon.nova-2-lite-v1:0` or the cross-region
     profile `us.amazon.nova-2-lite-v1:0` for us-east-1 / `in.amazon.nova-2-lite-v1:0`
     for ap-south-2). Model access requests are usually approved within a few minutes.
  3. Verify with `ss bedrock` — it must print `Bedrock OK` before measuring.
  4. Run `python -m ship_kit measure` and update the "After" line in this entry with the
     real numbers from `results/MEASURE.md`.
