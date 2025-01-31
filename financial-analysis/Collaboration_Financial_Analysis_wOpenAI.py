# Install necessary libraries
# pip install crewai
# pip install litellm
# pip install openai

# Import necessary libraries
from crewai import Agent, Task, Crew, LLM, Process
import os
from dotenv import load_dotenv
import litellm
from crewai import Agent, Task, Crew, LLM
import litellm
from litellm import OpenAIChatCompletion

# Warning control
import warnings
warnings.filterwarnings('ignore')

# Load environment variables for API key(s)
load_dotenv()

# Retrieve OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in your environment or .env file.")

# Set the OpenAI API key for litellm
os.environ["OPENAI_API_KEY"] = openai_api_key
litellm.api_key = openai_api_key

# Retrieve Serper API key
serper_api_key = os.getenv("SERPER_API_KEY")
if not serper_api_key:
    raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in your environment or .env file.")

# Configure the OpenAI LLM
llm = LLM(
    model="gpt-4o",
    temperature=0.7,
    max_tokens=1000,
    api_key=openai_api_key
)

from crewai_tools import ScrapeWebsiteTool, SerperDevTool

scrape_tool = ScrapeWebsiteTool()

search_tool = SerperDevTool(
    name="search",
    func="Perform a web search",
    description="Fetches search results from the web",
    n_results=10  # Set the number of results to fetch
)

data_analyst_agent = Agent(
    role="Data Analyst",
    goal="Monitor and analyze market data in real-time "
         "to identify trends and predict market movements.",
    backstory="Specializing in financial markets, this agent "
              "uses statistical modeling and machine learning "
              "to provide crucial insights. With a knack for data, "
              "the Data Analyst Agent is the cornerstone for "
              "informing trading decisions.",
    verbose=True,
    allow_delegation=True,
    llm=llm,
    tools = [scrape_tool, search_tool]
)

trading_strategy_agent = Agent(
    role="Trading Strategy Developer",
    goal="Develop and test various trading strategies based "
         "on insights from the Data Analyst Agent.",
    backstory="Equipped with a deep understanding of financial "
              "markets and quantitative analysis, this agent "
              "devises and refines trading strategies. It evaluates "
              "the performance of different approaches to determine "
              "the most profitable and risk-averse options.",
    verbose=True,
    allow_delegation=True,
    llm=llm,
    tools = [scrape_tool, search_tool]
)

execution_agent = Agent(
    role="Trade Advisor",
    goal="Suggest optimal trade execution strategies "
         "based on approved trading strategies.",
    backstory="This agent specializes in analyzing the timing, price, "
              "and logistical details of potential trades. By evaluating "
              "these factors, it provides well-founded suggestions for "
              "when and how trades should be executed to maximize "
              "efficiency and adherence to strategy.",
    verbose=True,
    allow_delegation=True,
    llm=llm,
    tools = [scrape_tool, search_tool]
)

risk_management_agent = Agent(
    role="Risk Advisor",
    goal="Evaluate and provide insights on the risks "
         "associated with potential trading activities.",
    backstory="Armed with a deep understanding of risk assessment models "
              "and market dynamics, this agent scrutinizes the potential "
              "risks of proposed trades. It offers a detailed analysis of "
              "risk exposure and suggests safeguards to ensure that "
              "trading activities align with the firm’s risk tolerance.",
    verbose=True,
    allow_delegation=True,
    llm=llm,
    tools = [scrape_tool, search_tool]
)

# Task for Data Analyst Agent: Analyze Market Data
data_analysis_task = Task(
    description=(
        "Continuously monitor and analyze market data for "
        "the selected stock ({stock_selection}). "
        "Use statistical modeling and machine learning to "
        "identify trends and predict market movements."
    ),
    expected_output=(
        "Insights and alerts about significant market "
        "opportunities or threats for {stock_selection}."
    ),
    agent=data_analyst_agent,
)

# Task for Trading Strategy Agent: Develop Trading Strategies
strategy_development_task = Task(
    description=(
        "Develop and refine trading strategies based on "
        "the insights from the Data Analyst and "
        "user-defined risk tolerance ({risk_tolerance}). "
        "Consider trading preferences ({trading_strategy_preference})."
    ),
    expected_output=(
        "A set of potential trading strategies for {stock_selection} "
        "that align with the user's risk tolerance."
    ),
    agent=trading_strategy_agent,
)

# Task for Trade Advisor Agent: Plan Trade Execution
execution_planning_task = Task(
    description=(
        "Analyze approved trading strategies to determine the "
        "best execution methods for {stock_selection}, "
        "considering current market conditions and optimal pricing."
    ),
    expected_output=(
        "Detailed execution plans suggesting how and when to "
        "execute trades for {stock_selection}."
    ),
    agent=execution_agent,
)

# Task for Risk Advisor Agent: Assess Trading Risks
risk_assessment_task = Task(
    description=(
        "Evaluate the risks associated with the proposed trading "
        "strategies and execution plans for {stock_selection}. "
        "Provide a detailed analysis of potential risks "
        "and suggest mitigation strategies."
    ),
    expected_output=(
        "A comprehensive risk analysis report detailing potential "
        "risks and mitigation recommendations for {stock_selection}."
    ),
    agent=risk_management_agent,
)

manager_llm = LLM(
    model = "gpt-4o-mini",
    temperature = 0.7,
    max_tokens = 500,
    api_key = openai_api_key
)

from crewai import Crew, Process

# Define the crew with agents and tasks
financial_trading_crew = Crew(
    agents=[data_analyst_agent,
            trading_strategy_agent,
            execution_agent,
            risk_management_agent],

    tasks=[data_analysis_task,
           strategy_development_task,
           execution_planning_task,
           risk_assessment_task],

    manager_llm=manager_llm,
    process=Process.hierarchical,
    verbose=True
)

# Example data for kicking off the process
financial_trading_inputs = {
    'stock_selection': 'NVDA',
    'initial_capital': '100000',
    'risk_tolerance': 'Medium',
    'trading_strategy_preference': '1 year',
    'news_impact_consideration': True
}

### this execution will take some time to run
result = financial_trading_crew.kickoff(inputs=financial_trading_inputs)
