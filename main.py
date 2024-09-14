from flask import Flask, jsonify, request
from langchain.agents import create_react_agent
from langchain.agents import AgentExecutor
from src.llm import openai_llm
from src.prompt import prompt_template
from src.logger import logging
from dotenv import load_dotenv
import os
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import load_tools
from datetime import datetime
from langchain.tools import Tool
from langchain_community.agent_toolkits.polygon.toolkit import PolygonToolkit
from langchain_community.utilities.polygon import PolygonAPIWrapper
from langchain.agents import load_tools


app = Flask(__name__)

os.environ["OPENWEATHERMAP_API_KEY"] = os.getenv('OPENWEATHERMAP_API_KEY')
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
os.environ["POLYGON_API_KEY"] = os.getenv('POLYGON_API_KEY')

llm = openai_llm()
logging.info("Load LLM")

prompt = prompt_template()

datetime_tool = Tool(
    name="Datetime",
    func=lambda x: datetime.now().isoformat(),
    description="Returns the current datetime",
)
logging.info("Initialized datetime tool")

search_tool = DuckDuckGoSearchRun()
logging.info("Initialized search tool")

# weather_tool = load_tools(["openweathermap-api"], llm)[0]
# logging.info("Initialized weather tool")

polygon = PolygonAPIWrapper()
toolkit = PolygonToolkit.from_polygon_api_wrapper(polygon)
logging.info("Initialized stock market tool")


@app.route("/api/test", methods=['GET'])
def test_api():
    return "Working..."


@app.route("/api/chatbot", methods=['POST'])
def article_generator():
    try:
        data = request.get_json()

        query = data["query"]
        logging.info(f"User input: {query}")

        tools = [search_tool, datetime_tool, toolkit.get_tools()[0], toolkit.get_tools()[
            1]]

        agent = create_react_agent(tools=tools, llm=llm, prompt=prompt)
        logging.info("Initialized agent")

        agent_executor = AgentExecutor(
            agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
        logging.info("Create agent executor object")

        response = agent_executor.invoke({"input": query})
        logging.info(f"Response: {response}")

        return {
            "result": response['output'],
            "status": "success"
        }
    except Exception as e:
        return {
            "result": str(e),
            "status": "failed"
        }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
