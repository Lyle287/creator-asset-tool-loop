"""Business decisions for delivering a creator's processed asset."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ProcessingResult:
    asset_name: str
    processed: bool
    subscriber_count: int


def next_actions(result: ProcessingResult) -> list[str]:
    """Return observable actions after content processing."""
    if not result.processed:
        return ["review_content"]
    actions = ["deliver_asset"]
    if result.subscriber_count > 0:
        actions.append("notify_subscribers")
    return actions

