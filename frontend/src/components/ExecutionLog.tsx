/**
 * Execution Log - Shows real-time agent execution progress.
 */
import React from 'react';
import type { WebSocketUpdate } from '../types';

interface ExecutionLogProps {
  updates: WebSocketUpdate[];
}

export const ExecutionLog: React.FC<ExecutionLogProps> = ({ updates }) => {
  return (
    <div className="bg-gray-900 text-green-400 font-mono text-sm p-4 rounded-lg h-80 overflow-y-auto">
      <div className="mb-2 text-gray-500">--- Execution Log ---</div>
      {updates.map((update, idx) => {
        const time = new Date(update.timestamp * 1000).toLocaleTimeString();
        return (
          <div key={idx} className="mb-3">
            <div className="flex gap-2">
              <span className="text-blue-400">[{time}]</span>
              <span className="text-yellow-400">{update.agent}:</span>
              <span className="text-gray-300">{update.status.toUpperCase()}</span>
            </div>
            {update.data?.result && (
              <div className="ml-4 text-gray-500 text-xs mt-1">
                → Cost: ${update.data.result.cost_usd?.toFixed(6)} | Latency: {update.data.result.latency_ms}ms | Confidence: {(update.data.result.confidence * 100).toFixed(0)}%
              </div>
            )}
          </div>
        );
      })}
      {updates.length === 0 && (
        <div className="text-gray-600 italic">Waiting for workflow execution...</div>
      )}
    </div>
  );
};
