import React from "react";

const ActionProvider = ({ createChatBotMessage, setState, children }) => {
  const handleQuery = (message) => {
    fetch("/query", {
      method: "POST",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ data: { message: message } }),
    }).then((res) =>
      res.json().then((data) => {
        const botMessage = createChatBotMessage(data.response);
        setState((prev) => ({
          ...prev,
          messages: [...prev.messages, botMessage],
        }));
      })
    );
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
