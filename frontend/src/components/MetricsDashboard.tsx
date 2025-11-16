/**
 * Metrics Dashboard - Shows performance charts and statistics.
 */
import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import type { WorkflowResult } from '../types';

interface MetricsDashboardProps {
  result: WorkflowResult | null;
}

export const MetricsDashboard: React.FC<MetricsDashboardProps> = ({ result }) => {
  if (!result) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-xl font-bold mb-4">Metrics Dashboard</h2>
        <p className="text-gray-500">Execute a workflow to see metrics...</p>
      </div>
    );
  }

  const agentData = result.steps.map(step => ({
    name: step.agent,
    cost: step.cost_usd * 1000000, // Convert to cost per million tokens
    latency: step.latency_ms,
    confidence: step.confidence * 100,
  }));

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 space-y-6">
      <h2 className="text-2xl font-bold text-gray-800">Performance Metrics</h2>
      
      {/* Summary Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-blue-50 p-4 rounded-lg">
          <div className="text-sm text-gray-600">Total Cost</div>
          <div className="text-2xl font-bold text-blue-600">${result.metrics.total_cost_usd.toFixed(6)}</div>
        </div>
        <div className="bg-green-50 p-4 rounded-lg">
          <div className="text-sm text-gray-600">Total Latency</div>
          <div className="text-2xl font-bold text-green-600">{(result.metrics.total_latency_ms / 1000).toFixed(2)}s</div>
        </div>
        <div className="bg-purple-50 p-4 rounded-lg">
          <div className="text-sm text-gray-600">Avg Confidence</div>
          <div className="text-2xl font-bold text-purple-600">{(result.metrics.avg_confidence * 100).toFixed(0)}%</div>
        </div>
        <div className="bg-orange-50 p-4 rounded-lg">
          <div className="text-sm text-gray-600">Tokens Used</div>
          <div className="text-2xl font-bold text-orange-600">{result.metrics.total_tokens}</div>
        </div>
      </div>

      {/* Latency Chart */}
      <div>
        <h3 className="font-semibold mb-2 text-gray-700">Latency by Agent</h3>
        <ResponsiveContainer width="100%" height={200}>
          <BarChart data={agentData}>
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip formatter={(value: any) => `${value}ms`} />
            <Bar dataKey="latency">
              {agentData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
