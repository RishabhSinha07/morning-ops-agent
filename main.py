from dotenv import load_dotenv

from tools.location import get_location
load_dotenv()

from agents import agent



def run():
    prompt = (
        f"Create my morning commute briefing for the city based on user location. "
        "Include weather, what to wear, and any commute disruptions."
    )

    _agent = agent.get_agent()

    response = _agent.invoke({"input": prompt})
    print(response["messages"][-1].content)



if __name__ == "__main__":
    run()