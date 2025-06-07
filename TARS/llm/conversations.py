from collections import deque
from langchain_core.messages import HumanMessage, SystemMessage


class ConversationState:
    def __init__(self, system_prompt, max_messages=30):
        self.system_message = SystemMessage(content=system_prompt)
        self.messages = deque(maxlen=max_messages)  # Auto-trim old messages
        self.max_context_tokens = 4000

    def add_user_message(self, content):
        self.messages.append(HumanMessage(content=content))

    def get_state(self):
        # Always include system message + recent messages
        all_messages = [self.system_message] + list(self.messages)

        # Check if we need to trim based on token count
        token_count = self.estimate_tokens(all_messages)

        if token_count > self.max_context_tokens:
            # Keep system + trim conversation history
            trimmed = self.smart_trim(list(self.messages))
            all_messages = [self.system_message] + trimmed

        return {"messages": all_messages}

    def smart_trim(self, messages):
        if len(messages) <= 10:
            return messages

        # Keep first 3 and last 7 messages
        return messages[:3] + messages[-7:]

    def estimate_tokens(self, messages):
        # Rough estimation - 4 chars per token
        return sum(len(str(msg.content)) for msg in messages) // 4
