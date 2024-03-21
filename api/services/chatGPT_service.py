from dotenv import find_dotenv, load_dotenv
from openai import OpenAI
from base_service import BaseService

class CineBot(BaseService):
    def init(self):
        self.api_key = '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'
        self.client = OpenAI(api_key=self.api_key)
    

    def get_completion_from_messages(self, messages, model="gpt-3.5-turbo", temperature=0):
        chat_completion = self.client.chat.completions.create(
            messages=messages,
            model=model
        )
        return chat_completion.choices[0].message.content

    def format_ai_response(self, raw_response):
        lines = raw_response.split("\n")
        ai_responses = [line for line in lines if line.startswith("CineBot:")]
        formatted_responses = [
            line.replace("CineBot:", "").strip() for line in ai_responses
        ]
        final_response = " ".join(formatted_responses)
        return final_response

    def collect_user_queries(self, query, movie, context):
        prompt = fprompt = f"""
        If user does not ask for recommendation and make a normal conversation
        otherwise  greet the user without any suggestion and let user lead to their {query}.
        else if the user is asking for a recommendation them recommend this {movie}.
        Do not recommend any movie if the user is not asking for it.
        Do not recommend other than {movie}.
        """
        context.append({"role": "user", "content": prompt})
        try:
            response = self.get_completion_from_messages(context)
            return response
        except Exception as e:
            # Handle possible exceptions such as API errors or network issues
            print(f"Error generating response: {e}")
            return "There was an error generating the content. Please try again."