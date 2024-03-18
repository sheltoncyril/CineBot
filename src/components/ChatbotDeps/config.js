import { createChatBotMessage } from 'react-chatbot-kit';

const botName = 'Cinebot';

const config = {
  initialMessages: [createChatBotMessage(`Hi! I'm ${botName}, here for all your movie needs. Boyfriend can't pick a movie? Don't you worry! Just tell me what you like and I will do much better than him!`)],
  botName: botName,
};

export default config;