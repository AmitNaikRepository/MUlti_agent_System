/**
 * API client for communicating with the backend.
 */
import axios from 'axios';
import type { WorkflowResult, ComparisonMetrics, MetricsSummary } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const workflowApi = {
  /**
   * Execute a multi-agent workflow.
   */
  async executeWorkflow(userInput: string, workflowType: string = 'customer_support'): Promise<WorkflowResult> {
    const response = await api.post('/workflow/execute', {
      user_input: userInput,
      workflow_type: workflowType,
    });
    return response.data;
  },

  /**
   * Get workflow details by ID.
   */
  async getWorkflow(workflowId: string): Promise<WorkflowResult> {
    const response = await api.get(`/workflows/${workflowId}`);
    return response.data;
  },

  /**
   * List all workflows with optional filters.
   */
  async listWorkflows(params?: {
    limit?: number;
    offset?: number;
    category?: string;
    status?: string;
  }): Promise<{ total: number; workflows: any[] }> {
    const response = await api.get('/workflows', { params });
    return response.data;
  },

  /**
   * Get metrics summary.
   */
  async getMetricsSummary(): Promise<MetricsSummary> {
    const response = await api.get('/metrics/summary');
    return response.data;
  },

  /**
   * Get comparison metrics (multi-agent vs single LLM).
   */
  async getComparisonMetrics(): Promise<ComparisonMetrics> {
    const response = await api.get('/metrics/comparison');
    return response.data;
  },

  /**
   * Health check.
   */
  async healthCheck(): Promise<{ status: string; timestamp: string; version: string }> {
    const response = await api.get('/health');
    return response.data;
  },
};

/**
 * WebSocket connection for real-time updates.
 */
export class WorkflowWebSocket {
  private ws: WebSocket | null = null;
  private url: string;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;

  constructor(url?: string) {
    this.url = url || 'ws://localhost:8000/api/ws';
  }

  connect(onMessage: (data: any) => void, onError?: (error: Event) => void): void {
    try {
      this.ws = new WebSocket(this.url);

      this.ws.onopen = () => {
        console.log('✅ WebSocket connected');
        this.reconnectAttempts = 0;
      };

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          onMessage(data);
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error);
        }
      };

      this.ws.onerror = (error) => {
        console.error('❌ WebSocket error:', error);
        if (onError) {
          onError(error);
        }
      };

      this.ws.onclose = () => {
        console.log('👋 WebSocket disconnected');
        this.attemptReconnect(onMessage, onError);
      };
    } catch (error) {
      console.error('Failed to create WebSocket connection:', error);
    }
  }

  private attemptReconnect(onMessage: (data: any) => void, onError?: (error: Event) => void): void {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);
      
      setTimeout(() => {
        this.connect(onMessage, onError);
      }, this.reconnectDelay * this.reconnectAttempts);
    } else {
      console.error('Max reconnection attempts reached');
    }
  }

  disconnect(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  send(data: any): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    } else {
      console.warn('WebSocket is not connected');
    }
  }
}

export default api;
