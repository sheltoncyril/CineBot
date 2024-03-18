from dotenv import find_dotenv, load_dotenv
from openai import OpenAI

# import logging
OPENAI_API_KEY = "..."
_ = load_dotenv(find_dotenv())
client = OpenAI(api_key=OPENAI_API_KEY)


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model,
    )
    return chat_completion.choices[0].message.content


def format_ai_response(raw_response):
    lines = raw_response.split("\n")
    ai_responses = [line for line in lines if line.startswith("CineBot:")]
    formatted_responses = [
        line.replace("CineBot:", "").strip() for line in ai_responses
    ]
    final_response = " ".join(formatted_responses)
    return final_response


def collect_user_queries(query, movie, context):
    prompt = f"Based on the following query: '{query}', considering the movie: '{movie}', and considering the context: '{context}', just construct conversation all sentences."
    context.append({"role": "user", "content": prompt})
    try:
        response = get_completion_from_messages(context)
        return response
    except Exception as e:
        # Handle possible exceptions such as API errors or network issues
        print(f"Error generating response: {e}")
        return "There was an error generating the content. Please try again."
