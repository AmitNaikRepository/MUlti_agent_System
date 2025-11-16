/**
 * Chat Interface - User input for customer support queries.
 */
import React, { useState } from 'react';

interface ChatInterfaceProps {
  onSubmit: (message: string) => void;
  isProcessing: boolean;
  sampleTickets?: Array<{ id: string; message: string }>;
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({ onSubmit, isProcessing, sampleTickets = [] }) => {
  const [input, setInput] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !isProcessing) {
      onSubmit(input);
      setInput('');
    }
  };

  const useSampleTicket = (message: string) => {
    setInput(message);
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">Customer Support Query</h2>
      
      <form onSubmit={handleSubmit} className="mb-4">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter a customer support query (e.g., 'I want a refund for order #12345')"
          className="w-full p-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none min-h-[100px]"
          disabled={isProcessing}
        />
        
        <button
          type="submit"
          disabled={isProcessing || !input.trim()}
          className="mt-3 w-full bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          {isProcessing ? 'Processing...' : 'Execute Workflow'}
        </button>
      </form>

      {sampleTickets.length > 0 && (
        <div className="border-t pt-4">
          <h3 className="font-semibold text-gray-700 mb-2">Sample Tickets:</h3>
          <div className="space-y-2">
            {sampleTickets.slice(0, 3).map((ticket) => (
              <button
                key={ticket.id}
                onClick={() => useSampleTicket(ticket.message)}
                className="w-full text-left p-2 text-sm bg-gray-100 hover:bg-gray-200 rounded border border-gray-300 transition-colors"
                disabled={isProcessing}
              >
                {ticket.message}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
