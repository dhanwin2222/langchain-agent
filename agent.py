"""
Agent with LangChain and  LLM integration
"""
# LangChain components
from langchain_groq import ChatGroq
from langchain_community.utilities import  WikipediaAPIWrapper
from langchain_community.tools import  WikipediaQueryRun
from langchain.agents import initialize_agent, AgentType
from langchain_community.utilities import ArxivAPIWrapper
from langchain_community.tools import ArxivQueryRun
from langchain.chains.conversation.memory import ConversationBufferMemory

# Standard libraries
import os
import warnings
# Deprecation warning handling
from langchain_core._api.deprecation import LangChainDeprecationWarning
warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)

# Environment variables
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()  

# Get API key from environment
api_key = os.getenv("GROQ_API_KEY")



# Initialize tools - Wikipedia and ArXiv

# - top_k_results=1: Retrieves only the most relevant  article
# - doc_content_chars_max=300: Limits the content length for concise responses

api_wrapper = WikipediaAPIWrapper(top_k_results=3, doc_content_chars_max=300)
wiki = WikipediaQueryRun(api_wrapper=api_wrapper)

arxiv_wrapper = ArxivAPIWrapper(top_k_results=3, doc_content_chars_max=300)
arxiv_tool = ArxivQueryRun(api_wrapper=arxiv_wrapper)


# LLM SETUP

# Initialize the Large Language Model (LLM) with Groq
# - model_name: Using llama-3.3-70b-versatile, an open-source model
# - streaming: Enables progressive response generation
# - max_tokens: Limits response length to 512 tokens
    

llm = ChatGroq(groq_api_key=api_key, model_name="llama-3.3-70b-versatile", streaming=True,max_tokens=512)

# Create tool list - contains Wikipedia and arxiv for this implementation

tools = [wiki,arxiv_tool]

# Setup conversation memory to maintain context across interactions
memory = ConversationBufferMemory(memory_key="chat_history")


#Initialize the agent with defined components
# - agent: CONVERSATIONAL_REACT_DESCRIPTION is suitable for tool-using conversations
# - max_iterations: Limits reasoning steps to prevent infinite loops
# - early_stopping_method: Stops reasoning when complete
# - handle_parsing_errors: Improves error handling during tool usage


conversational_agent = initialize_agent(
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,  # Changed to a valid AgentType
    tools=tools,
    llm=llm,
    verbose=False,
    max_iterations=3,
    early_stopping_method='generate',
    memory=memory,
    
    handle_parsing_errors=True
)

# PROMPT TEMPLATE
# This template guides how the agent thinks, when to use tools, and response formatting

conversational_agent.agent.llm_chain.prompt.template = '''
Purpose:
Assistant is a conversational bot designed to help users with a wide range of tasks, from answering simple questions to providing detailed explanations and engaging in meaningful discussions.

Context:
Assistant exists to support users by delivering information and engaging in natural conversations.

Objective:

Use tool arxiv, wikipedia when factual or historical,research paper lookup is required.

Use internal training knowledge to handle casual or personal interactions (e.g., greetings like “Had dinner?”).

Also, use internal training knowledge when asked to perform tasks outside the scope of available tools, such as generating a story, poem, or creative writing.






Style:
Conversational, clear, and informative.

Tone:
Friendly, supportive, and helpful.

Audience:
Anyone seeking information, help, or just a conversation.

TOOLS:
------

Assistant has access to the following tools:


> wikipedia: A wrapper around Wikipedia. Useful for when you need to answer general questions about people, places, companies, facts, historical events, or other subjects. Input should be a search query.
> arxiv: A wrapper around ArXiv. Useful for when you need to answer questions about research papers, scientific articles, or technical subjects. Input should be a search query.
To use a tool, please use the following format:

```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [arxiv, wikipedia]
Action Input: the input to the action
Observation: the result of the action
```

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

```
Thought: Do I need to use a tool? No
AI: [your response here]
```

Begin!

Previous conversation history:
{chat_history}

New input: {input}
{agent_scratchpad}


'''


