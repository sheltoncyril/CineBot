from collections import defaultdict

from fastapi import HTTPException
from models.models import Chat, Message, MessageRequest, Role
from utils.id_generators import generate_id_with_prefix
from utils.utils import remove_date_from_movie

from .base_service import BaseService


class ChatApplicationService(BaseService):
    def init(self, service_registry):
        self.service_registry = service_registry

    def create_chat(self, session):
        chat = Chat(id=generate_id_with_prefix("chat"))
        session.add(chat)
        session.commit()
        session.refresh(chat)
        return chat

    def get_chat(self, session, chat_id: str):
        chat = session.get(Chat, chat_id)
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")
        return chat

    def _get_recommendations_for_chat(self, chat):
        r1, c1 = self.service_registry.get_service("similarity_recommender_service").recommend(self._get_context_query(chat.messages), k=7)
        r2, c2 = self.service_registry.get_service("tfidf_recommender_service").recommend(self._get_context_query(chat.messages, user_only=True), k=7)
        L = []
        for m, c in zip(r1, c1):
            a = remove_date_from_movie(m)
            L.append((a, c))
        score = defaultdict(lambda: 0)
        total = 0
        max_c1 = max(c1)
        for movie in L:
            score[movie[0]] = movie[1] / max_c1
        for movie, score2 in zip(r2, c2):
            score[movie] += score2 * 3
        sorted_score = sorted(score.items(), key=lambda x: x[1], reverse=True)
        k = 3
        movies = []
        confidence = 0
        for m in sorted_score[:k]:
            movies.append(m[0])
            confidence += m[1]
        return movies, confidence / k

    def _get_context_query(self, messages, user_only=False):
        query = ""
        for message in messages:
            if message.role == Role.user or (message.role == Role.assistant and not user_only):
                query += message.message + " "
        return query

    def _get_system_prompt(self, seq_no, recommendations, confidence, threshold, current_query):
        prompts = [
            f"""
        Imagine you are a movie recommendation chatbot called Cinebot. 
        Greet the user if if the user has greeted you.
        Ask the user about their past preference of movie genre and names of movies they liked.
        Do not recommend any movies to the user.
        """,
            f"""
        Ask the user on what they like and dislike in past movies they watched.
        Do not recommend any movies to the user.
        
        """,
            f"""
        Ask the more about genre, directors, actors in past movies they watched.
        Do not recommend any movies to the user.
        
        """,
            f"""
        You can now recommend these movies to the user: {", ".join(recommendations)}.
        Do not recommend any other movies than {", ".join(recommendations)}
        
        """,
            f"""
        If user does not ask for recommendation then make normal conversation
        otherwise  greet the user without any suggestion and let user lead to their {current_query}.
        else if the user is asking for a recommendation them recommend this {recommendations}.
        Do not recommend any movie if the user is not asking for it.
        Do not recommend other than {recommendations}.
        """,
        ]

        if seq_no == 2:
            return prompts[0]
        if seq_no == 5:
            return prompts[1]
        elif seq_no < 8 and confidence < threshold:
            return prompts[2]
        elif confidence > threshold:
            return prompts[3]

    def process_message(self, session, chat_id: str, message_request: MessageRequest):
        threshold = 0.7
        chat = self.get_chat(session, chat_id)
        chatgpt_service = self.service_registry.get_service("chatgpt_service")
        if chat.messages:
            msg_seq_no = chat.messages[-1].seq_no + 1
        else:
            msg_seq_no = 1
        message_request = Message.model_validate(message_request)
        message_request.seq_no = msg_seq_no
        message_request.chat_id = chat_id
        chat.messages.append(message_request)
        msg_seq_no += 1
        recommendations, confidence = self._get_recommendations_for_chat(chat)
        system_prompt = self._get_system_prompt(msg_seq_no, recommendations, confidence, threshold, message_request.message)
        if system_prompt:
            system_message = Message(message=system_prompt, role="system", chat_id=chat_id, seq_no=msg_seq_no)
            chat.messages.append(system_message)
            msg_seq_no += 1
        assistant_response = chatgpt_service.get_completion_from_messages(chat.get_messages())
        message_response = Message(message=assistant_response, role="assistant", chat_id=chat_id, seq_no=msg_seq_no)
        chat.messages.append(message_response)
        chat.updated_time = message_response.creation_time
        session.add(chat)
        session.commit()
        session.refresh(message_response)
        return message_response
