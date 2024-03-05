import time

from openai import OpenAI
from openai.types.beta import Thread
from openai.types.beta.threads import Run

from Config import OpenAiConfig


class GPT:
    def __init__(self, openai_config: OpenAiConfig):
        self.gpt = OpenAI(api_key=openai_config.api_key)
        self.config = openai_config

    def __wait_for_query(self, run: Run, thread: Thread) -> str:
        """
        Wait for the query to complete and return the response
        """
        while run.status != "completed":
            run = self.gpt.beta.threads.runs.retrieve(
                thread_id=thread.id, run_id=run.id
            )
            time.sleep(1)
        else:
            message_response = self.gpt.beta.threads.messages.list(thread_id=thread.id)
            messages = message_response.data
            latest_message = messages[0]
            return latest_message.content[0].text.value

    def send_query(self, message: str) -> str:
        """
        Query GPT-4 and return the response
        """
        # create thread
        thread = self.gpt.beta.threads.create(
            messages=[{"role": "user", "content": message}]
        )

        # create run and wait for query to complete
        run = self.gpt.beta.threads.runs.create(
            thread_id=thread.id, assistant_id=self.config.assistant_id
        )

        # wait for query to complete
        return self.__wait_for_query(run, thread)
