import os
import re
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

from morning_ops_agent.agents import agent
from notion_client import Client


def run(prompt):
    _agent = agent.get_agent()

    response = _agent.invoke({"messages": [{"role": "user", "content": prompt}]})
    return response["messages"][-1].content


def parse_rich_text(text):
    """Parse inline **bold** and [link](url) markdown into Notion rich_text."""
    # Split on bold and link patterns, preserving delimiters
    tokens = re.split(r"(\*\*.*?\*\*|\[.*?\]\(.*?\))", text)
    rich_text = []
    for token in tokens:
        if not token:
            continue
        if token.startswith("**") and token.endswith("**"):
            rich_text.append({
                "type": "text",
                "text": {"content": token[2:-2]},
                "annotations": {"bold": True},
            })
        else:
            link_match = re.match(r"^\[(.*?)\]\((.*?)\)$", token)
            if link_match:
                rich_text.append({
                    "type": "text",
                    "text": {"content": link_match.group(1), "link": {"url": link_match.group(2)}},
                })
            else:
                rich_text.append({"type": "text", "text": {"content": token}})
    return rich_text


def markdown_to_notion_blocks(text):
    """Convert markdown-formatted text into Notion block objects."""
    blocks = []
    for line in text.split("\n"):
        stripped = line.strip()

        if not stripped:
            continue

        # Blockquote → Notion callout (used for alerts/warnings)
        if stripped.startswith("> "):
            content = stripped[2:]
            # Pick the leading emoji (with optional variation selector) as callout icon
            emoji_match = re.match(r"^([\U0001f300-\U0001fad6\u2600-\u27bf\u2700-\u27bf]\ufe0f?)\s*", content)
            icon = "⚠️"
            if emoji_match:
                icon = emoji_match.group(1)
                content = content[emoji_match.end():]
            blocks.append({
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": parse_rich_text(content),
                    "icon": {"type": "emoji", "emoji": icon},
                    "color": "red_background",
                },
            })
        # Heading lines: ### heading
        elif stripped.startswith("### "):
            blocks.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {"rich_text": parse_rich_text(stripped[4:])},
            })
        elif stripped.startswith("## "):
            blocks.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {"rich_text": parse_rich_text(stripped[3:])},
            })
        # Bullet points: - item or * item
        elif stripped.startswith("- ") or stripped.startswith("* "):
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": parse_rich_text(stripped[2:])},
            })
        # Numbered list: 1. item
        elif re.match(r"^\d+\.\s", stripped):
            content = re.sub(r"^\d+\.\s", "", stripped)
            blocks.append({
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {"rich_text": parse_rich_text(content)},
            })
        # Standalone bold line (e.g. "**Hourly Breakdown:**") → heading_3
        elif re.match(r"^\*\*.+\*\*:?$", stripped):
            heading_text = stripped.strip("*").rstrip(":")
            blocks.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {"rich_text": [{"type": "text", "text": {"content": heading_text}}]},
            })
        # Regular paragraph
        else:
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": parse_rich_text(stripped)},
            })

    return blocks


if __name__ == "__main__":
    city = os.getenv("CITY", "Quincy, MA")
    response = run(f"Provide the analysis for {city}")
    print("Adding to notion: ", response)

    notion = Client(auth=os.getenv("NOTION_TOKEN"))
    page_id = os.getenv("NOTION_PAGE_ID")

    today = datetime.now().strftime("%A, %B %d, %Y")

    # Date header callout
    header_block = {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [{"type": "text", "text": {"content": f"Morning Briefing — {today}"}}],
            "icon": {"type": "emoji", "emoji": "🌅"},
        },
    }

    content_blocks = markdown_to_notion_blocks(response)

    divider = {"object": "block", "type": "divider", "divider": {}}

    children = [divider, header_block] + content_blocks + [divider]

    # Notion API allows max 100 blocks per append
    for i in range(0, len(children), 100):
        notion.blocks.children.append(block_id=page_id, children=children[i:i+100])
