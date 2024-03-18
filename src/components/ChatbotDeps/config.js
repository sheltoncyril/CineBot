import { createChatBotMessage } from 'react-chatbot-kit';
import CinebotImage from '../../images/robot.png'
const botName = 'Cinebot';

const config = {
  initialMessages: [createChatBotMessage(`Hi! I'm ${botName}, here for all your movie needs.  Can't pick a movie? Don't you worry! Just tell me what you like and I will do my best!`)],
  botName: botName,
  customComponents:{
    botAvatar:(props)=><img src={CinebotImage} width={'50em'} height={'50em'} style={{marginRight:'0.5em'}}/>
  }
  
};

export default config;