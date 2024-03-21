import React from "react";
import { createChat, getChat, sendQuery } from "../../api-core/core";

const ActionProvider = ({ createChatBotMessage, setState, children }) => {

  const handleQuery = (message) => {
    let chatID = localStorage.getItem('chatID')
    if (!chatID) {
      createChat().then((res) => {
        console.log('Res',res)
      })
      .catch((err) => console.log(err))
    }
    else{
      sendQuery(message, chatID)
      .then((res) =>
        res.json().then((data) => {
          const botMessage = createChatBotMessage(data.response);
          setState((prev) => ({
            ...prev,
            messages: [...prev.messages, botMessage],
          }));
        })
      );
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
