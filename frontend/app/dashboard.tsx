'use client';
import React, { useState } from 'react';
import { Upload, File as FileIcon, Send, Trash2, Loader } from 'lucide-react';
import axios from 'axios';

type Message = {
  type: 'user' | 'ai';
  text: string;
  timestamp: string;
};

const Dashboard: React.FC = () => {
  const [pdfFile, setPdfFile] = useState<File | null>(null);
  const [question, setQuestion] = useState<string>('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  // Handle PDF file upload
  const handleFileUpload = async(e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files?.length) return;
    const file = e.target.files?.[0];
    setIsLoading(true);
    if (file && file.type === 'application/pdf') {
      setPdfFile(file);
      setMessages([]);
        
      // Here you would upload the file to your backend
      console.log('File uploaded:', file.name);
    } else {
      alert('Please upload a valid PDF file');
    }
       try{
        const formData = new FormData();
            formData.append("file", file);       
        const response = await axios.post('http://127.0.0.1:8000/upload-pdf', formData);
        
        console.log('Upload response:', response.data);

    }catch(e){
        console.log(e);
    }
    setIsLoading(false);
  };

  // Handle removing PDF
  const handleRemovePdf = () => {
    setPdfFile(null);
    setMessages([]);
    setQuestion('');
  };



  const handleSendQuestion = async () => {
    if (!question.trim() || !pdfFile) return;

    const userMessage: Message = {
      type: 'user',
      text: question,
      timestamp: new Date().toLocaleTimeString(),
    };

    setMessages([...messages, userMessage]);
    setQuestion('');
    setIsLoading(true);

    // Simulate API call to your AI model
    // Replace this with your actual API call
    try {
      // Example API call structure:
      const formData = new FormData();
      formData.append('question', question);
      const response = await axios.post('http://127.0.0.1:8000/ask',
        {
            "query":question

        });
      console.log('AI response:', response.data);

      // Simulated response for demo
      setTimeout(() => {
        const aiMessage: Message = {
          type: 'ai',
          text: response.data.answer,
          timestamp: new Date().toLocaleTimeString(),
        };
        setMessages(prev => [...prev, aiMessage]);
        setIsLoading(false);
      }, 1500);
    } catch (error) {
      console.error('Error:', error);
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendQuestion();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      {/* Full-screen loading overlay while isLoading is true */}
      {isLoading && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
          <div className="bg-white/95 dark:bg-gray-800/95 rounded-lg p-4 flex items-center space-x-3 shadow-lg">
            <Loader className="w-6 h-6 animate-spin text-gray-700 dark:text-gray-200" />
            <span className="text-gray-700 dark:text-gray-200">Loading...</span>
          </div>
        </div>
      )}

      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8 pt-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">PDF Question & Answer</h1>
          <p className="text-gray-600">Upload a PDF and ask questions about its content</p>
        </div>

        {/* Main Container */}
        <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
          
          {/* PDF Upload Section */}
          <div className="border-b border-gray-200 p-6 bg-gray-50">
            {!pdfFile ? (
              <label className="flex flex-col items-center justify-center w-full h-40 border-2 border-dashed border-gray-300 rounded-lg cursor-pointer hover:bg-gray-100 transition-colors">
                <div className="flex flex-col items-center justify-center pt-5 pb-6">
                  <Upload className="w-10 h-10 mb-3 text-gray-400" />
                  <p className="mb-2 text-sm text-gray-500">
                    <span className="font-semibold">Click to upload</span> or drag and drop
                  </p>
                  <p className="text-xs text-gray-500">PDF files only</p>
                </div>
                <input
                  type="file"
                  className="hidden"
                  accept="application/pdf"
                  onChange={handleFileUpload}
                />
              </label>
            ) : (
              <div className="flex items-center justify-between bg-white p-4 rounded-lg border border-gray-200">
                <div className="flex items-center space-x-3">
                  <div className="bg-red-100 p-2 rounded">
                    <FileIcon className="w-6 h-6 text-red-600" />
                  </div>
                  <div>
                    <p className="font-medium text-gray-800">{pdfFile.name}</p>
                    <p className="text-sm text-gray-500">
                      {(pdfFile.size / 1024).toFixed(2)} KB
                    </p>
                  </div>
                </div>
                <button
                  onClick={handleRemovePdf}
                  className="p-2 hover:bg-red-50 rounded-lg transition-colors"
                >
                  <Trash2 className="w-5 h-5 text-red-600" />
                </button>
              </div>
            )}
          </div>

          {/* Chat Messages Section */}
          <div className="h-96 overflow-y-auto p-6 space-y-4">
            {messages.length === 0 && pdfFile && (
              <div className="text-center text-gray-400 mt-20">
                <p>Ask a question about your PDF to get started</p>
              </div>
            )}
            
            {messages.length === 0 && !pdfFile && (
              <div className="text-center text-gray-400 mt-20">
                <p>Upload a PDF file to start asking questions</p>
              </div>
            )}

            {messages.map((message, index) => (
              <div
                key={index}
                className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-xs lg:max-w-md px-4 py-3 rounded-2xl ${
                    message.type === 'user'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-800'
                  }`}
                >
                  <p className="text-sm">{message.text}</p>
                  <p className={`text-xs mt-1 ${
                    message.type === 'user' ? 'text-blue-200' : 'text-gray-500'
                  }`}>
                    {message.timestamp}
                  </p>
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-gray-100 px-4 py-3 rounded-2xl">
                  <div className="flex items-center space-x-2">
                    <Loader className="w-4 h-4 animate-spin text-gray-600" />
                    <p className="text-sm text-gray-600">Thinking...</p>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Input Section */}
          <div className="border-t border-gray-200 p-4 bg-gray-50">
            <div className="flex space-x-2">
              <input
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder={pdfFile ? "Ask a question about your PDF..." : "Upload a PDF first..."}
                disabled={!pdfFile || isLoading}
                className="text-black flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
              />
              <button
                onClick={handleSendQuestion}
                disabled={!pdfFile || !question.trim() || isLoading}
                className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
              >
                <Send className="w-5 h-5" />
                <span>Send</span>
              </button>
            </div>
          </div>
        </div>

        {/* Instructions */}
        <div className="mt-6 bg-white rounded-lg p-4 shadow">
          <h3 className="font-semibold text-gray-800 mb-2">How to use:</h3>
          <ol className="list-decimal list-inside text-sm text-gray-600 space-y-1">
            <li>Upload a PDF file using the upload area</li>
            <li>Type your question in the input field</li>
            <li>Click Send to get AI-powered answers from your document</li>
          </ol>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
// ...existing code...