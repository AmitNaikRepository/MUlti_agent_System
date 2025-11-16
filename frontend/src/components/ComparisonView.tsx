/**
 * Comparison View - Multi-agent vs Single LLM comparison.
 */
import React from 'react';
import type { ComparisonMetrics } from '../types';

interface ComparisonViewProps {
  metrics: ComparisonMetrics | null;
}

const MetricRow: React.FC<{ label: string; value: string | number; trend?: 'up' | 'down' | 'neutral' }> = ({ label, value, trend }) => {
  const trendIcons = { up: '↗️', down: '↘️', neutral: '→' };
  return (
    <div className="flex justify-between py-2 border-b border-gray-200">
      <span className="font-semibold text-gray-700">{label}</span>
      <span className="flex items-center gap-2">
        {value}
        {trend && <span>{trendIcons[trend]}</span>}
      </span>
    </div>
  );
};

export const ComparisonView: React.FC<ComparisonViewProps> = ({ metrics }) => {
  if (!metrics) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-xl font-bold mb-4">Multi-Agent vs Single LLM</h2>
        <p className="text-gray-500">Loading comparison data...</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">Approach Comparison</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Multi-Agent System */}
        <div className="border-2 border-blue-500 rounded-lg p-4 bg-blue-50">
          <h3 className="font-bold text-blue-700 text-lg mb-4">Multi-Agent System ✨</h3>
          <div className="space-y-2">
            <MetricRow label="Accuracy" value={`${(metrics.multi_agent.avg_accuracy * 100).toFixed(0)}%`} trend="up" />
            <MetricRow label="Avg Cost" value={`$${metrics.multi_agent.avg_cost_usd.toFixed(6)}`} trend="down" />
            <MetricRow label="Avg Latency" value={`${(metrics.multi_agent.avg_latency_ms / 1000).toFixed(1)}s`} trend="neutral" />
            <div className="mt-4 text-sm space-y-1 pt-4 border-t border-blue-300">
              <div className="flex items-start gap-2">
                <span>✅</span>
                <span className="text-gray-700">Higher accuracy through specialized agents</span>
              </div>
              <div className="flex items-start gap-2">
                <span>✅</span>
                <span className="text-gray-700">{metrics.improvement.cost}</span>
              </div>
              <div className="flex items-start gap-2">
                <span>⚠️</span>
                <span className="text-gray-700">Slightly higher latency (acceptable)</span>
              </div>
            </div>
          </div>
        </div>

        {/* Single LLM */}
        <div className="border-2 border-gray-400 rounded-lg p-4 bg-gray-50">
          <h3 className="font-bold text-gray-700 text-lg mb-4">Single LLM (GPT-4)</h3>
          <div className="space-y-2">
            <MetricRow label="Accuracy" value={`${(metrics.single_llm.avg_accuracy * 100).toFixed(0)}%`} trend="neutral" />
            <MetricRow label="Avg Cost" value={`$${metrics.single_llm.avg_cost_usd.toFixed(6)}`} trend="neutral" />
            <MetricRow label="Avg Latency" value={`${(metrics.single_llm.avg_latency_ms / 1000).toFixed(1)}s`} trend="neutral" />
            <div className="mt-4 text-sm space-y-1 pt-4 border-t border-gray-300">
              <div className="flex items-start gap-2">
                <span>⚠️</span>
                <span className="text-gray-600">Lower accuracy on complex tasks</span>
              </div>
              <div className="flex items-start gap-2">
                <span>❌</span>
                <span className="text-gray-600">6.5x more expensive</span>
              </div>
              <div className="flex items-start gap-2">
                <span>✅</span>
                <span className="text-gray-600">Faster single response</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-6 p-4 bg-green-50 border border-green-300 rounded-lg">
        <p className="text-sm font-semibold text-green-800">
          💡 Recommendation: {metrics.recommendation}
        </p>
      </div>
    </div>
  );
};
