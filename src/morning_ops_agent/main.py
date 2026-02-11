import os
from dotenv import load_dotenv
load_dotenv()

from morning_ops_agent.agents import agent
from notion_client import Client



def run(prompt):
    _agent = agent.get_agent()

    response = _agent.invoke({"messages": [{"role": "user", "content": prompt}]})
    return response["messages"][-1].content



if __name__ == "__main__":
    city = os.getenv("CITY", "Quincy, MA")
    response = run(f"Provide the analysis for {city}")
    print("Adding to notion: ", response)

    notion = Client(auth=os.getenv("NOTION_TOKEN"))
    page_id = os.getenv("NOTION_PAGE_ID")

    # Chunk response text at 2000 chars for Notion rich text limit
    chunks = [response[i:i+2000] for i in range(0, len(response), 2000)]
    rich_text_blocks = [
        {"type": "text", "text": {"content": chunk}}
        for chunk in chunks
    ]

    notion.blocks.children.append(
        block_id=page_id,
        children=[
            {
                "object": "block",
                "type": "divider",
                "divider": {}
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": rich_text_blocks
                },
            },
            {
                "object": "block",
                "type": "divider",
                "divider": {}
            },
        ],
    )
