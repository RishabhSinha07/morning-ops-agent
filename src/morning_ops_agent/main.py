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
    """Parse inline **bold** markdown into Notion rich_text annotations."""
    parts = re.split(r"(\*\*.*?\*\*)", text)
    rich_text = []
    for part in parts:
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            rich_text.append({
                "type": "text",
                "text": {"content": part[2:-2]},
                "annotations": {"bold": True},
            })
        else:
            rich_text.append({"type": "text", "text": {"content": part}})
    return rich_text


def markdown_to_notion_blocks(text):
    """Convert markdown-formatted text into Notion block objects."""
    blocks = []
    for line in text.split("\n"):
        stripped = line.strip()

        if not stripped:
            continue

        # Heading lines: ### heading
        if stripped.startswith("### "):
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
