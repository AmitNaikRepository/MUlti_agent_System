/**
 * TypeScript type definitions for the Multi-Agent Orchestration System.
 */

export interface AgentStepResult {
  agent: string;
  output: string;
  reasoning: string;
  confidence: number;
  cost_usd: number;
  latency_ms: number;
  tokens_used: number;
}

export interface WorkflowMetrics {
  total_cost_usd: number;
  total_latency_ms: number;
  total_tokens: number;
  avg_confidence: number;
  agents_used: number;
  workflow_duration_ms: number;
}

export interface WorkflowResult {
  workflow_id: string;
  status: string;
  user_input: string;
  category?: string;
  urgency?: string;
  final_output: string;
  qa_review?: QAReview;
  steps: AgentStepResult[];
  metrics: WorkflowMetrics;
  timestamp: string;
}

export interface QAReview {
  accuracy_score: number;
  tone_score: number;
  completeness_score: number;
  clarity_score: number;
  overall_score: number;
  strengths: string[];
  improvements: string[];
  recommendation: 'APPROVE' | 'REVISE' | 'REJECT';
  reasoning: string;
  confidence: number;
}

export interface WebSocketUpdate {
  workflow_id: string;
  agent: string;
  status: 'running' | 'completed' | 'failed';
  data?: any;
  timestamp: number;
}

export interface AgentStatus {
  name: string;
  status: 'idle' | 'running' | 'completed' | 'failed';
  result?: AgentStepResult;
}

export interface ComparisonMetrics {
  multi_agent: {
    avg_accuracy: number;
    avg_cost_usd: number;
    avg_latency_ms: number;
    model: string;
  };
  single_llm: {
    avg_accuracy: number;
    avg_cost_usd: number;
    avg_latency_ms: number;
    model: string;
  };
  improvement: {
    accuracy: string;
    cost: string;
    latency: string;
  };
  recommendation: string;
}

export interface SampleTicket {
  id: string;
  message: string;
  expected_category: string;
  expected_outcome: string;
  expected_amount?: string;
  urgency?: string;
}

export interface MetricsSummary {
  total_workflows: number;
  avg_cost_usd: number;
  avg_latency_ms: number;
  avg_confidence: number;
  category_breakdown: Array<{
    category: string;
    count: number;
  }>;
  agent_performance: Array<{
    agent: string;
    avg_latency_ms: number;
    avg_cost_usd: number;
    avg_confidence: number;
  }>;
}
