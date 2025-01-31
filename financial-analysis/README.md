# Financial Analysis Multi-Agent System

This repository contains an implementation of a multi-agent system for financial analysis using LLMs. The project is based on the original work by Viktoria Semaan, available at [multi-agent financial analysis](https://github.com/viktoriasemaan/multi-agent/tree/main/financial-analysis).

## Overview

This system utilizes multiple AI agents to analyze financial markets, develop trading strategies, assess risks, and provide trading execution recommendations. The agents leverage OpenAI and Anthropic's Claude models along with various tools to scrape and analyze data.

## Features

- **Data Analysis Agent**: Monitors and analyzes market data in real-time to identify trends and predict market movements.
- **Trading Strategy Developer**: Develops and tests various trading strategies based on insights from the data analyst.
- **Trade Advisor**: Suggests optimal trade execution strategies.
- **Risk Advisor**: Evaluates and provides insights on the risks associated with potential trading activities.

## Cloning the Repository

To get started, clone the main repository:

```sh
git clone https://github.com/drhitchen/multi-agent.git
cd multi-agent/financial-analysis
```

## Installation

To use this project, first create a virtual environment and install the dependencies:

```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

Ensure you have the necessary environment variables set up in a `.env` file:

```sh
# You must provide either an OpenAI API key or an Anthropic API key
OPENAI_API_KEY=your_openai_api_key  # Required if using OpenAI models
ANTHROPIC_API_KEY=your_anthropic_api_key  # Required if using Anthropic models

# A SERPER API key is required regardless of the model used
SERPER_API_KEY=your_serper_api_key
```

## Usage

Run the script with the appropriate model:

```sh
python Collaboration_Financial_Analysis_wOpenAI.py
# OR
python Collaboration_Financial_Analysis_wClaude.py
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Credits

Original concept and repository by [Viktoria Semaan](https://github.com/viktoriasemaan/multi-agent/tree/main/financial-analysis). This implementation is adapted and maintained by Doug Hitchen.
