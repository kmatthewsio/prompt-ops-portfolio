# memory/session_manager.py
from langchain_core.messages import HumanMessage, AIMessage


class SimpleSessionManager:
    def __init__(self):
        self.sessions = {}  # session_id -> list of messages

    def add_messages(self, session_id: str, user_msg: str, ai_msg: str):
        if session_id not in self.sessions:
            self.sessions[session_id] = []

        self.sessions[session_id].extend([
            HumanMessage(content=user_msg),
            AIMessage(content=ai_msg)
        ])

    def get_history(self, session_id: str):
        return self.sessions.get(session_id, [])


# Global instance
session_manager = SimpleSessionManager()
