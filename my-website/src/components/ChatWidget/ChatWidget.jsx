import React, { useState, useEffect, useRef } from 'react';
import { useLanguage } from '@site/src/contexts/LanguageContext';
import './ChatWidget.css';

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);
  const chatContainerRef = useRef(null);

  // Get language context
  const { language } = useLanguage();

  // API endpoint - adjust as needed for your deployment
  // For Docusaurus, we use a simple approach since process.env is not available in browser
  // This can be configured by setting a global variable CHATBOT_API_URL before the script loads
  const getApiBaseUrl = () => {
    if (typeof window !== 'undefined' && window.CHATBOT_API_URL) {
      return `${window.CHATBOT_API_URL}/api`;
    }
    // Check for REACT_APP_API_URL in browser environment (for builds)
    if (typeof process !== 'undefined' && process.env && process.env.REACT_APP_API_URL) {
      return `${process.env.REACT_APP_API_URL}/api`;
    }
    // Fallback to local backend during development
    return 'https://aaneeq-rag-chatbot.hf.space/api';
  };

  const API_BASE_URL = getApiBaseUrl();

  // Function to scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Function to detect text selection
  useEffect(() => {
    const handleSelection = () => {
      const selectedText = window.getSelection().toString().trim();
      if (selectedText) {
        setSelectedText(selectedText);
      } else {
        setSelectedText(null);
      }
    };

    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('keyup', handleSelection);

    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('keyup', handleSelection);
    };
  }, []);

  // Function to send message to backend
  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = { role: 'user', content: inputValue };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: inputValue,
          selected_text: selectedText,
          session_id: sessionId,
          language: language,  // Pass the current language to backend
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Update session ID if it was returned (first message)
      if (data.session_id && !sessionId) {
        setSessionId(data.session_id);
      }

      const assistantMessage = {
        role: 'assistant',
        content: data.answer,
        citations: data.citations || [],
        mode: data.mode,
      };

      setMessages([...newMessages, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        role: 'assistant',
        content: 'Sorry, I encountered an error while processing your request. Please try again.',
      };
      setMessages([...newMessages, errorMessage]);
    } finally {
      setIsLoading(false);
      setSelectedText(null); // Clear selected text after sending
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="chat-widget">
      {isOpen ? (
        <div className="chat-container" ref={chatContainerRef}>
          <div className="chat-header">
            <div className="chat-header-content">
              <h3>Humanoid Robotics Assistant</h3>
              {selectedText && (
                <div className="selected-text-indicator">
                  <span className="selected-text-badge">Selected Text Mode</span>
                </div>
              )}
            </div>
            <button className="chat-close-btn" onClick={toggleChat}>
              ×
            </button>
          </div>

          <div className="chat-messages">
            {messages.length === 0 ? (
              <div className="chat-welcome">
                <h4>Hello! I'm your Humanoid Robotics Assistant.</h4>
                <p>Ask me anything about humanoid robotics, or select text on the page to get specific answers.</p>
              </div>
            ) : (
              messages.map((message, index) => (
                <div
                  key={index}
                  className={`chat-message ${message.role === 'user' ? 'user-message' : 'assistant-message'}`}
                >
                  <div className="message-content">
                    <div className="message-text">
                      {message.content}
                    </div>
                    {message.citations && message.citations.length > 0 && (
                      <div className="message-citations">
                        <strong>Citations:</strong>
                        <ul>
                          {message.citations.map((citation, idx) => (
                            <li key={idx}>
                              Source: {citation.source_file} (Score: {citation.similarity_score.toFixed(2)})
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                    {message.mode && (
                      <div className="message-mode">
                        Mode: {message.mode === 'full_rag' ? 'Full Book RAG' : 'Selected Text'}
                      </div>
                    )}
                  </div>
                </div>
              ))
            )}
            {isLoading && (
              <div className="chat-message assistant-message">
                <div className="message-content">
                  <div className="message-text">
                    <div className="typing-indicator">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="chat-input-area">
            {selectedText && (
              <div className="current-selection-preview">
                <strong>Selected text:</strong> "{selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}"
              </div>
            )}
            <div className="chat-input-container">
              <textarea
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder={selectedText ? "Ask about selected text..." : "Ask about humanoid robotics..."}
                className="chat-input"
                rows="1"
              />
              <button
                onClick={sendMessage}
                disabled={isLoading || !inputValue.trim()}
                className="chat-send-btn"
              >
                Send
              </button>
            </div>
          </div>
        </div>
      ) : (
        <button className="chat-toggle-btn" onClick={toggleChat}>
          <span className="chat-icon">🤖</span>
          <span>Chat</span>
        </button>
      )}
    </div>
  );
};

export default ChatWidget;