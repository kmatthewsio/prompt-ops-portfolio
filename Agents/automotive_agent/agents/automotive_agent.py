from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from config.settings import OPENAI_API_KEY, MODEL
from tools import ALL_TOOLS

class AutomotiveAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model=MODEL, api_key = OPENAI_API_KEY)
        self.tools = ALL_TOOLS,
        self.agent = self._create_agent()

    def _create_agent(self):
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful automotive sales assistant. Use tools to help customers with vehicle pricing and payments."),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}")
        ]
        )

        agent = create_tool_calling_agent(self.llm, self.tools, prompt)
        return AgentExecutor(agent=agent, tools=self.tools, verbose=True)
    def chat(self, message: str, chat_history=None):
        return self.agent.invoke({
            "input": message,
            "chat_history": chat_history or []
        })
automotive_agent = AutomotiveAgent()









