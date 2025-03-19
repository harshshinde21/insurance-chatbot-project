import React from "react";
import Chatbot from "./Chatbot";
import Header from "./Header";
import "./App.css";

const App = () => {
  return (
    <div className="app-container">
      <Header />
      <Chatbot />
    </div>
  );
};

export default App;
