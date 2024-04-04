## Langchain CustomAgent - with FASTAPI Integration

# overview

This project creates custom agent in langchain using custom tools. The agent is deployed as an API using FASTAPI and Langserve.

# Features

1) **Tools** : Tools to demonstrate agent workflow. Created custom tools for adding and multiply operations and used built in tavily search tool in langchain for real time context search. 
2) **Agent** : The Agent created using Langchain expression language and openai's gpt-3.5 turbo. The model can precisely output the arguments for the required tool based on the users natural language query.
3) **Request** : Agent was deployed as an API using FASTAPI. Includes an endpoint that leverages Langchain for response generation.

# Configuration

This requires environment variables such as OPENAI_API_KEY, TAVILY_API_KEY and LANGCHAIN_API_KEY (helpful for debugging in langsmith. This is optional) 
