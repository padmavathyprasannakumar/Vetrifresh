import React, { useState } from "react";
import "./ChatBot.css";

function ChatBot() {
  const [open, setOpen] = useState(false);
  const [message, setMessage] = useState("");

  const [messages, setMessages] = useState([
    {
      id: 1,
      type: "bot",
      text: "Here are the latest Sale offers",
      time: "12:23 PM",
    },
  ]);

  const quickReplies = [
    "Issue with my Order",
    "Issue with cancellation fee",
    "Latest sale offers",
    "Something else",
  ];

  const getTime = () => {
    return new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const getBotReply = (text) => {
    const lowerText = text.toLowerCase();

    if (lowerText.includes("order")) {
      return "Please login and open My Orders to check your order status.";
    }

    if (lowerText.includes("cancel")) {
      return "Cancellation is available before your order is packed.";
    }

    if (lowerText.includes("sale") || lowerText.includes("offer")) {
      return "Today offers: Fresh Fruits up to 64% OFF and Vegetables up to 30% OFF.";
    }

    return "Thank you. Our support team will help you shortly.";
  };

  const sendMessage = (quickText) => {
    const finalText = quickText || message;

    if (!finalText.trim()) return;

    const userMessage = {
      id: Date.now(),
      type: "user",
      text: finalText,
      time: getTime(),
    };

    setMessages((oldMessages) => [...oldMessages, userMessage]);
    setMessage("");

    setTimeout(() => {
      const botMessage = {
        id: Date.now() + 1,
        type: "bot",
        text: getBotReply(finalText),
        time: getTime(),
      };

      setMessages((oldMessages) => [...oldMessages, botMessage]);
    }, 600);
  };

  return (
    <>
      {!open && (
        <button
          type="button"
          className="vf-help-chat-button"
          onClick={() => setOpen(true)}
          aria-label="Open chatbot"
        >
          🤖
        </button>
      )}

      {open && (
        <div className="vf-help-chat-panel">
          <div className="vf-help-chat-header">
            <button
              type="button"
              className="vf-help-chat-back"
              onClick={() => setOpen(false)}
              aria-label="Back"
              title="Back"
            >
              ←
            </button>

            <h3>Help</h3>

            <button
              type="button"
              className="vf-help-chat-close"
              onClick={() => setOpen(false)}
              aria-label="Close chatbot"
              title="Close"
            >
              ×
            </button>
          </div>

          <div className="vf-help-chat-body">
            <div className="vf-help-chat-date">Tue, 24 Sep</div>

            <div className="vf-help-chat-offer">
              <div>
                <small>SUMMER SALE</small>
                <h4>75% OFF</h4>
                <p>Only Fruit & Vegetable</p>
                <button type="button">Shop Now →</button>
              </div>

              <span>🤖</span>
            </div>

            <div className="vf-help-chat-audio">
              ▶ <span>0:25</span>
            </div>

            {messages.map((item) => (
              <div
                key={item.id}
                className={
                  item.type === "bot"
                    ? "vf-help-message bot"
                    : "vf-help-message user"
                }
              >
                {item.type === "bot" && (
                  <div className="vf-help-avatar">🤖</div>
                )}

                <div className="vf-help-bubble">
                  <strong>{item.type === "bot" ? "Chatbot" : "You"}</strong>
                  <p>{item.text}</p>
                  <small>{item.time}</small>
                </div>
              </div>
            ))}

            <div className="vf-help-quick">
              {quickReplies.map((reply) => (
                <button
                  type="button"
                  key={reply}
                  onClick={() => sendMessage(reply)}
                >
                  {reply}
                </button>
              ))}
            </div>
          </div>

          <form
            className="vf-help-chat-input"
            onSubmit={(event) => {
              event.preventDefault();
              sendMessage();
            }}
          >
            <input
              type="text"
              placeholder="Enter your message"
              value={message}
              onChange={(event) => setMessage(event.target.value)}
            />

            <button type="submit" aria-label="Send message">
              ➤
            </button>
          </form>
        </div>
      )}
    </>
  );
}

export default ChatBot;
