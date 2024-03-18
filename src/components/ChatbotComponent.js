import config from './ChatbotDeps/config.js';
import MessageParser from './ChatbotDeps/MessageParser.js';
import ActionProvider from './ChatbotDeps/ActionProvider.js';
import './ChatbotComponent.css'
import Chatbot from 'react-chatbot-kit'


const ChatbotComponent = () => {
  return (
      <Chatbot
        config={config}
        messageParser={MessageParser}
        actionProvider={ActionProvider}
      />
  );
};

export default ChatbotComponent
