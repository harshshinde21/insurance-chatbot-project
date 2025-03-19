import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import "./Chatbot.css";
import { FaPaperPlane } from "react-icons/fa";
import { motion } from "framer-motion";

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const chatBoxRef = useRef(null);

  useEffect(() => {
    chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "user", text: input };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInput("");

    let endpoint = "http://localhost:5000/chat";
    let requestData = { user_input: input };

    if (input.toLowerCase().includes("policy")) {
        const policyNumberMatch = input.match(/POL\d{5}/);  // Extracts policy number (e.g., POL12345)
        if (policyNumberMatch) {
            const policyNumber = policyNumberMatch[0];
            endpoint = "http://localhost:5000/policy_status";
            requestData = JSON.stringify({ policy_number: policyNumber }); // Convert to JSON string
        } else {
            setMessages((prevMessages) => [
                ...prevMessages,
                { sender: "bot", text: "Please provide a valid policy number (e.g., POL12345)." }
            ]);
            return;
        }
    }

    try {
        const response = await axios.post(endpoint, requestData, {
            headers: { "Content-Type": "application/json" }  // Ensure JSON format
        });

        const botMessage = { sender: "bot", text: response.data.response };
        setMessages((prevMessages) => [...prevMessages, botMessage]);
    } catch (error) {
        console.error("API Error:", error.response ? error.response.data : error.message);
        setMessages((prevMessages) => [
            ...prevMessages,
            { sender: "bot", text: "Error processing request. Please try again later." }
        ]);
    }
};
  return (
    <motion.div className="chat-container" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5 }}>
      <h2 className="chat-header">Insurance Chatbot</h2>
      <div className="chat-box" ref={chatBoxRef}>
        {messages.map((msg, index) => (
          <motion.div
            key={index}
            className={`message ${msg.sender}`}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            {msg.text}
          </motion.div>
        ))}
      </div>
      <div className="input-container">
        <motion.input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your query..."
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          whileFocus={{ scale: 1.05 }}
        />
        <motion.button onClick={sendMessage} className="send-button" whileHover={{ scale: 1.1 }}>
          <FaPaperPlane />
        </motion.button>
      </div>
    </motion.div>
  );
};

export default Chatbot;
