import os
from dotenv import load_dotenv
load_dotenv()

from agents import agent
from notion_client import Client



def run(city):
    prompt = f"I am in city : {city}, can you provide me todays analysis?"

    _agent = agent.get_agent()

    response = _agent.invoke({"input": prompt})
    return response["messages"][-1].content



if __name__ == "__main__":
    response = run("Quincy, MA")
    print("Adding to notion: ", response)

    notion = Client(auth=os.getenv("NOTION_TOKEN"))
    page_id = os.getenv("NOTION_PAGE_ID")

    # Append a divider
    notion.blocks.children.append(
        block_id=page_id,
        children=[
            {
                "object": "block",
                "type": "divider",
                "divider": {}
            }
        ]
    )
    
    notion.blocks.children.append(
        block_id=page_id,
        children=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": response}
                        }
                    ]
                },
            }
        ],
    )

    # Append a divider
    notion.blocks.children.append(
        block_id=page_id,
        children=[
            {
                "object": "block",
                "type": "divider",
                "divider": {}
            }
        ]
    )