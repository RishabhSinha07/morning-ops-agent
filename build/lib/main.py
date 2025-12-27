from dotenv import load_dotenv
load_dotenv()

from agents import agent



def run(city):
    prompt = f"I am in city : {city}, can you provide me todays analysis?"

    _agent = agent.get_agent()

    response = _agent.invoke({"input": prompt})
    print(response["messages"][-1].content)



if __name__ == "__main__":
    run("Quincy, MA")