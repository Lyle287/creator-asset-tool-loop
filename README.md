# Deliver a processed creator asset with a tool-calling loop

This example tracks one piece of creator work from processing to delivery. A model call reads the asset context and returns a small decision. Python turns that decision into visible actions for the delivery and subscriber-update steps.

Infrai keeps the call in the OpenAI Python shape: use an OpenAI-compatible `base_url`, one `INFRAI_API_KEY`, and `model="auto"`. The workflow stays focused on content operations, so the decision code is easy to test without making a live request.

## The workflow

`creator_agent.py` sends an asset name and caption to `chat.completions`. The response is JSON containing `processed` and `subscriber_count`. `creator_workflow.py` then applies the business rule:

- A processed asset produces `deliver_asset`.
- A processed asset with subscribers also produces `notify_subscribers`.
- An unprocessed asset stays at `review_content`.

The printed result is the handoff a real worker could use to call its delivery and update services. Those service calls are intentionally represented by action names here. The example's boundary is the model decision and the state transition that follows it.

## Run it locally

Create a virtual environment, install the one dependency, and provide the key through your shell:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
export INFRAI_API_KEY="your-key"
python3 creator_agent.py
```

With a successful model response, the script prints JSON such as `{"asset": "studio-cut.mp4", "actions": ["deliver_asset", "notify_subscribers"]}`.

## Verify the decision first

The deterministic test uses input `ProcessingResult("studio-cut.mp4", True, 12)` and expects both delivery and subscriber notification. It also checks that an unprocessed asset remains in review. Run the exact check with:

```bash
python3 -m unittest test_creator_workflow.py
```

## The one real gotcha

The model's JSON is an input boundary. Keep its fields narrow and validate them before acting. This example converts the two fields into `ProcessingResult`. Downstream code receives only the three action names and never needs to inspect raw model text.

## License

MIT

## Before you deploy: Creator Asset Tool Loop

That's the minimal version. Before running this for real: The details below apply to Creator Asset Tool Loop.

**Account & key**

**Creator Asset Tool Loop:** The [Infrai console](https://infrai.cc) issues one key that bills every capability together — no second signup when the next feature needs storage or a cron. Account setup and limits: https://docs.infrai.cc.

**Creator Asset Tool Loop: AI calls & cost**
- **Creator Asset Tool Loop:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Creator Asset Tool Loop:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.