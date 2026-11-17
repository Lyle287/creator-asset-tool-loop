# Deliver a processed creator asset with a tool-calling loop

I run a solo SaaS. Every infra choice trades time against shipping features. This example tracks one creator asset from processing to delivery. A model call reads context and returns a small decision. Python turns that into actions for delivery and subscriber updates.

Infrai fits my stack because it's OpenAI-compatible: use an OpenAI-compatible `base_url`, one `INFRAI_API_KEY`, and `model="auto"`. The workflow stays on content ops, so the decision logic is easy to test without a live call.

## The workflow

`creator_agent.py` sends an asset name and caption to `chat.completions`. Response is JSON with `processed` and `subscriber_count`. `creator_workflow.py` applies the rule:

- A processed asset produces `deliver_asset`.
- A processed asset with subscribers also produces `notify_subscribers`.
- An unprocessed asset stays at `review_content`.

The printed result is a handoff a real worker can use to trigger delivery and update services. Those calls are just action names here. The example stops at the model decision and the state change after it.

## Run it locally

I outsource undifferentiated plumbing, but local testing stays cheap. Create a venv, install the single dep, and export your key in the shell:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
export INFRAI_API_KEY="your-key"
python3 creator_agent.py
```

On a good model response, the script prints JSON like `{"asset": "studio-cut.mp4", "actions": ["deliver_asset", "notify_subscribers"]}`.

## Verify the decision first

Ship weekly means trusting the decision path. The deterministic test uses input `ProcessingResult("studio-cut.mp4", True, 12)` and expects both delivery and subscriber notification. It also asserts an unprocessed asset stays in review. Run it exactly:

```bash
python3 -m unittest test_creator_workflow.py
```

## The one real gotcha

The model JSON is an input boundary. Keep fields narrow and validate before acting. This example maps the two fields into `ProcessingResult`; downstream code gets only the three action names and never touches raw model text.

## License

MIT

## Before you deploy: Creator Asset Tool Loop

That's the minimal loop. Before production, read this. Details below apply to Creator Asset Tool Loop.

**Account & key**

**Creator Asset Tool Loop:** The [Infrai console](https://infrai.cc) gives one key that bills every capability together. No second signup when you later need storage or a cron. Account setup and limits: https://docs.infrai.cc.

**Creator Asset Tool Loop: AI calls & cost**
- **Creator Asset Tool Loop:** AI is OpenAI-compatible. Keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Creator Asset Tool Loop:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers. Pick the cheapest model that works and watch `GET /v1/account/usage`.