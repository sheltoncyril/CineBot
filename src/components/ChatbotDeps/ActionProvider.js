import React from "react";
import { createChat, getChat, sendQuery } from "../../api-core/core";

const ActionProvider = ({ createChatBotMessage, setState, children }) => {

  const sendTheQuery = (message, chatID) => {
    sendQuery(message, chatID)
      .then((res) => {
        console.log(res)
        let botMessage = createChatBotMessage();
        if (res && res.detail && res.detail == 'Chat not found') {
          localStorage.clear()
          botMessage = createChatBotMessage(res.detail)
        }
        if (res && res.message) {
          botMessage = createChatBotMessage(res.message);
          setState((prev) => ({
            ...prev,
            messages: [...prev.messages, botMessage],
          }));
        }
      });
  }
  const handleQuery = (message) => {
    let chatID = localStorage.getItem('chatID')
    console.log('cha', chatID)
    if (!chatID) {
      createChat().then((res) => {
        console.log('Res', res)
        if (res && res.id) {
          localStorage.setItem('chatID', res.id)
          sendTheQuery(message, res.id
          )
        }

      })
        .catch((err) => console.log(err))
    }
    else {
      sendTheQuery(message, chatID)
    }

  };
  return (
    <div>
      {React.Children.map(children, (child) => {
        return React.cloneElement(child, {
          actions: {
            handleQuery,
          },
        });
      })}
    </div>
  );
};

export default ActionProvider;
