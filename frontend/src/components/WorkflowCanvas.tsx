/**
 * Workflow Canvas - Visual representation of agent workflow using React Flow.
 */
import React from 'react';
import ReactFlow, { Node, Edge, Background, Controls, MarkerType } from 'reactflow';
import 'reactflow/dist/style.css';
import type { AgentStatus } from '../types';

interface WorkflowCanvasProps {
  agentStatuses: Record<string, AgentStatus>;
}

const CustomAgentNode = ({ data }: any) => {
  const statusColors = {
    idle: 'bg-gray-200 border-gray-400',
    running: 'bg-yellow-300 border-yellow-600 animate-pulse',
    completed: 'bg-green-300 border-green-600',
    failed: 'bg-red-300 border-red-600',
  };

  const statusIcons = {
    idle: '⏸️',
    running: '🔄',
    completed: '✅',
    failed: '❌',
  };

  const cost = data.result?.cost_usd || 0;
  const latency = data.result?.latency_ms || 0;
  const confidence = data.result?.confidence || 0;

  return (
    <div className={"px-6 py-4 rounded-lg border-2 shadow-lg min-w-[180px] " + statusColors[data.status]}>
      <div className="flex items-center justify-between mb-2">
        <div className="font-bold text-gray-800">{data.label}</div>
        <div className="text-xl">{statusIcons[data.status]}</div>
      </div>
      
      {data.result && (
        <div className="text-xs text-gray-700 space-y-1 border-t border-gray-400 pt-2 mt-2">
          <div className="flex justify-between">
            <span className="font-semibold">Cost:</span>
            <span>${cost.toFixed(6)}</span>
          </div>
          <div className="flex justify-between">
            <span className="font-semibold">Latency:</span>
            <span>{latency}ms</span>
          </div>
          <div className="flex justify-between">
            <span className="font-semibold">Confidence:</span>
            <span>{(confidence * 100).toFixed(0)}%</span>
          </div>
        </div>
      )}
    </div>
  );
};

const nodeTypes = { agentNode: CustomAgentNode };

export const WorkflowCanvas: React.FC<WorkflowCanvasProps> = ({ agentStatuses }) => {
  const nodes: Node[] = [
    { id: 'classifier', type: 'agentNode', position: { x: 400, y: 50 },
      data: { label: 'Classifier', status: agentStatuses.classifier?.status || 'idle', result: agentStatuses.classifier?.result } },
    { id: 'researcher', type: 'agentNode', position: { x: 200, y: 220 },
      data: { label: 'Research', status: agentStatuses.researcher?.status || 'idle', result: agentStatuses.researcher?.result } },
    { id: 'validator', type: 'agentNode', position: { x: 600, y: 220 },
      data: { label: 'Validator', status: agentStatuses.validator?.status || 'idle', result: agentStatuses.validator?.result } },
    { id: 'writer', type: 'agentNode', position: { x: 400, y: 390 },
      data: { label: 'Writer', status: agentStatuses.writer?.status || 'idle', result: agentStatuses.writer?.result } },
    { id: 'qa', type: 'agentNode', position: { x: 400, y: 560 },
      data: { label: 'QA', status: agentStatuses.qa?.status || 'idle', result: agentStatuses.qa?.result } },
  ];

  const edges: Edge[] = [
    { id: 'e1', source: 'classifier', target: 'researcher', animated: agentStatuses.classifier?.status === 'completed', markerEnd: { type: MarkerType.ArrowClosed } },
    { id: 'e2', source: 'classifier', target: 'validator', animated: agentStatuses.classifier?.status === 'completed', markerEnd: { type: MarkerType.ArrowClosed } },
    { id: 'e3', source: 'researcher', target: 'writer', animated: agentStatuses.researcher?.status === 'completed', markerEnd: { type: MarkerType.ArrowClosed } },
    { id: 'e4', source: 'validator', target: 'writer', animated: agentStatuses.validator?.status === 'completed', markerEnd: { type: MarkerType.ArrowClosed } },
    { id: 'e5', source: 'writer', target: 'qa', animated: agentStatuses.writer?.status === 'completed', markerEnd: { type: MarkerType.ArrowClosed } },
  ];

  return (
    <div className="h-full w-full bg-gray-50">
      <ReactFlow nodes={nodes} edges={edges} nodeTypes={nodeTypes} fitView attributionPosition="bottom-left">
        <Background color="#aaa" gap={16} />
        <Controls />
      </ReactFlow>
    </div>
  );
};
