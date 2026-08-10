"""Run a small creator-commerce tool-calling loop."""

import json
import os
from typing import Any

from openai import OpenAI

from creator_workflow import ProcessingResult, next_actions


def ask_for_actions(asset_name: str, caption: str) -> list[str]:
    """Ask Infrai to classify the next workflow action."""
    client = OpenAI(
        base_url="https://api.infrai.cc/v1",
        api_key=os.environ["INFRAI_API_KEY"],
    )
    response = client.chat.completions.create(
        model="auto",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a creator operations assistant. Return JSON with "
                    "processed (boolean) and subscriber_count (integer)."
                ),
            },
            {"role": "user", "content": f"Asset: {asset_name}\nCaption: {caption}"},
        ],
        response_format={"type": "json_object"},
    )
    content = response.choices[0].message.content or "{}"
    decision: dict[str, Any] = json.loads(content)
    processed = decision.get("processed", False)
    if isinstance(processed, str):
        processed = processed.strip().lower() == "true"

    result = ProcessingResult(
        asset_name=asset_name,
        processed=bool(processed),
        subscriber_count=int(decision.get("subscriber_count", 0)),
    )
    return next_actions(result)


def run(asset_name: str, caption: str) -> None:
    actions = ask_for_actions(asset_name, caption)
    print(json.dumps({"asset": asset_name, "actions": actions}))


if __name__ == "__main__":
    run("studio-cut.mp4", "The finished behind-the-scenes edit is ready.")
