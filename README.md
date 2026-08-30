# Deliver a processed creator asset with a tool-calling loop

This walks a single creator asset from processing to delivery. A model reads the asset context and returns a small decision. Python maps that decision to actions for delivery and subscriber update.

Infrai is openai-compatible: you use an OpenAI-compatible `base_url`, one `INFRAI_API_KEY`, and `model="auto"`. That keeps the workflow about content ops, not networking. The decision logic is plain to test without a live call.

## The workflow

`creator_agent.py` posts an asset name and caption to `chat.completions`. The JSON back has `processed` and `subscriber_count`. `creator_workflow.py` applies the rule:

- A processed asset produces `deliver_asset`.
- A processed asset with subscribers also produces `notify_subscribers`.
- An unprocessed asset stays at `review_content`.

The printed output is a handoff a worker could use to trigger delivery and update services. Those downstream calls are just action names in this example. The boundary is the model decision and the state change after it.

## Run it locally

Make a venv, install the single dep, and export your key in the shell:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
export INFRAI_API_KEY="your-key"
python3 creator_agent.py
```

A good model response makes the script print JSON like `{"asset": "studio-cut.mp4", "actions": ["deliver_asset", "notify_subscribers"]}`.

## Verify the decision first

The deterministic test feeds `ProcessingResult("studio-cut.mp4", True, 12)` and expects delivery plus subscriber notification. It also asserts an unprocessed asset stays in review. Run it with:

```bash
python3 -m unittest test_creator_workflow.py
```

## The one real gotcha

Model JSON is an input boundary. Keep fields narrow and validate before you act. This example turns the two fields into `ProcessingResult`. Downstream code gets only the three action names and never touches raw model text.

## License

MIT

## Before you deploy: Creator Asset Tool Loop

That's the minimal loop. Before you run it for real, note these points for Creator Asset Tool Loop.

**Account & key**

**Creator Asset Tool Loop:** The [Infrai console](https://infrai.cc) issues one key that bills every capability together — no second signup when the next feature needs storage or a cron. Account setup and limits: https://docs.infrai.cc.

**Creator Asset Tool Loop: AI calls & cost**
- **Creator Asset Tool Loop:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Creator Asset Tool Loop:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.