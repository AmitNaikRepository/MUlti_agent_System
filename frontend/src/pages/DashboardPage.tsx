import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Home } from 'lucide-react';
import { WorkflowCanvas } from '../components/WorkflowCanvas';
import { ChatInterface } from '../components/ChatInterface';
import { ExecutionLog } from '../components/ExecutionLog';
import { MetricsDashboard } from '../components/MetricsDashboard';
import { ComparisonView } from '../components/ComparisonView';
import { workflowApi, WorkflowWebSocket } from '../services/api';
import type { WorkflowResult, WebSocketUpdate, AgentStatus, ComparisonMetrics } from '../types';
import sampleTicketsData from '../../data/sample_tickets.json';

export default function DashboardPage() {
  const navigate = useNavigate();
  const [agentStatuses, setAgentStatuses] = useState<Record<string, AgentStatus>>({
    classifier: { name: 'Classifier', status: 'idle' },
    researcher: { name: 'Researcher', status: 'idle' },
    validator: { name: 'Validator', status: 'idle' },
    writer: { name: 'Writer', status: 'idle' },
    qa: { name: 'QA', status: 'idle' },
  });
  
  const [updates, setUpdates] = useState<WebSocketUpdate[]>([]);
  const [currentResult, setCurrentResult] = useState<WorkflowResult | null>(null);
  const [comparisonMetrics, setComparisonMetrics] = useState<ComparisonMetrics | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [ws] = useState(() => new WorkflowWebSocket());

  useEffect(() => {
    // Load comparison metrics
    workflowApi.getComparisonMetrics().then(setComparisonMetrics).catch(console.error);

    // Setup WebSocket
    ws.connect((update: WebSocketUpdate) => {
      console.log('WebSocket update:', update);
      setUpdates(prev => [...prev, update]);

      // Update agent status
      if (update.agent !== 'workflow') {
        setAgentStatuses(prev => ({
          ...prev,
          [update.agent.toLowerCase()]: {
            name: update.agent,
            status: update.status,
            result: update.data?.result,
          },
        }));
      }
    });

    return () => ws.disconnect();
  }, []);

  const handleSubmit = async (message: string) => {
    setIsProcessing(true);
    setUpdates([]);
    setCurrentResult(null);

    // Reset all agent statuses
    setAgentStatuses({
      classifier: { name: 'Classifier', status: 'idle' },
      researcher: { name: 'Researcher', status: 'idle' },
      validator: { name: 'Validator', status: 'idle' },
      writer: { name: 'Writer', status: 'idle' },
      qa: { name: 'QA', status: 'idle' },
    });

    try {
      const result = await workflowApi.executeWorkflow(message);
      setCurrentResult(result);
    } catch (error) {
      console.error('Workflow execution error:', error);
      alert('Error executing workflow. Please check console for details.');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header with Back Button */}
      <header className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                🤖 Multi-Agent Orchestration System
              </h1>
              <p className="text-gray-600 mt-1">
                Enterprise Customer Support Automation with Specialized AI Agents
              </p>
            </div>
            <button
              onClick={() => navigate('/')}
              className="flex items-center gap-2 px-4 py-2 text-gray-700 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors font-medium"
            >
              <Home className="w-5 h-5" />
              <span className="hidden sm:inline">Back to Home</span>
            </button>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Main Grid Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Input and Workflow */}
          <div className="lg:col-span-2 space-y-6">
            {/* Chat Interface */}
            <ChatInterface 
              onSubmit={handleSubmit}
              isProcessing={isProcessing}
              sampleTickets={sampleTicketsData.slice(0, 3)}
            />

            {/* Workflow Visualization */}
            <div className="bg-white rounded-lg shadow-lg p-4">
              <h2 className="text-xl font-bold mb-4 text-gray-800">Agent Workflow</h2>
              <div style={{ height: '700px' }}>
                <WorkflowCanvas agentStatuses={agentStatuses} />
              </div>
            </div>

            {/* Metrics Dashboard */}
            <MetricsDashboard result={currentResult} />
          </div>

          {/* Right Column - Logs and Results */}
          <div className="space-y-6">
            {/* Execution Log */}
            <div className="bg-white rounded-lg shadow-lg p-4">
              <h2 className="text-xl font-bold mb-4 text-gray-800">Execution Log</h2>
              <ExecutionLog updates={updates} />
            </div>

            {/* Final Output */}
            {currentResult && (
              <div className="bg-white rounded-lg shadow-lg p-4">
                <h2 className="text-xl font-bold mb-4 text-gray-800">Generated Response</h2>
                <div className="bg-gray-50 p-4 rounded border border-gray-300">
                  <pre className="whitespace-pre-wrap text-sm text-gray-800">
                    {currentResult.final_output}
                  </pre>
                </div>
                
                {currentResult.qa_review && (
                  <div className="mt-4">
                    <h3 className="font-semibold mb-2">QA Review</h3>
                    <div className="text-sm space-y-1">
                      <div>Overall Score: {currentResult.qa_review.overall_score}/10</div>
                      <div>Recommendation: 
                        <span className={currentResult.qa_review.recommendation === 'APPROVE' ? 'text-green-600 font-bold' : 'text-orange-600 font-bold'}>
                          {' '}{currentResult.qa_review.recommendation}
                        </span>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Comparison View */}
            <ComparisonView metrics={comparisonMetrics} />
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-white shadow-md mt-12">
        <div className="max-w-7xl mx-auto px-4 py-4 text-center text-gray-600 text-sm">
          Multi-Agent Orchestration System v1.0.0 | Built with FastAPI, React, Groq AI
        </div>
      </footer>
    </div>
  );
}
