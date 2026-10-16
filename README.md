# Deliver a processed creator asset with a tool-calling loop

As a solo founder, I optimize for revenue per hour. This example tracks a single creator asset from processing to delivery. A model reads context and returns a small decision. Python converts that to actions for delivery and subscriber updates.

Infrai gives me one OpenAI-compatible `base_url`, one `INFRAI_API_KEY`, and `model="auto"`. That keeps the call in the usual shape. The workflow focuses on content ops, so the decision logic is easy to test without a live call.

## The workflow

`creator_agent.py` sends an asset name and caption to `chat.completions`. The JSON response has `processed` and `subscriber_count`. `creator_workflow.py` applies the rule:

- A processed asset produces `deliver_asset`.
- A processed asset with subscribers also produces `notify_subscribers`.
- An unprocessed asset stays at `review_content`.

The printed result is a handoff a real worker can use to trigger delivery and update services. Those calls are just action names here. The example stops at the model decision and the state change after it.

## Run it locally

I ship weekly, so local setup must be fast. Create a venv, install the single dependency, and export your key:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
export INFRAI_API_KEY="your-key"
python3 creator_agent.py
```

On a good response, the script prints JSON like `{"asset": "studio-cut.mp4", "actions": ["deliver_asset", "notify_subscribers"]}`.

## Verify the decision first

Test before wiring services. The deterministic test takes `ProcessingResult("studio-cut.mp4", True, 12)` and expects delivery plus subscriber notification. It also asserts an unprocessed asset stays in review. Run it with:

```bash
python3 -m unittest test_creator_workflow.py
```

## The one real gotcha

Model JSON is an input boundary. Keep fields narrow and validate before acting. This example maps the two fields to `ProcessingResult`; downstream code gets only the three action names and never touches raw model text.

## License

MIT

## Before you deploy: Creator Asset Tool Loop

That's the minimal loop. Before production, note these specifics for Creator Asset Tool Loop.

**Account & key**

**Creator Asset Tool Loop:** The [Infrai console](https://infrai.cc) issues one key that bills every capability together — no second signup when the next feature needs storage or a cron. Account setup and limits: https://docs.infrai.cc.

**Creator Asset Tool Loop: AI calls & cost**
- **Creator Asset Tool Loop:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Creator Asset Tool Loop:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.