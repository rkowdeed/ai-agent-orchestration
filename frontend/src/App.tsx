import React, {useEffect, useState} from 'react'

type Agent = {
  agent_id: string
  config: Record<string, any>
}

type Message = {
  id: number
  agent_id: string | null
  sender: string
  role: string
  channel: string
  text: string
  created_at: string
}

export default function App() {
  const [status, setStatus] = useState<string>('loading')
  const [agents, setAgents] = useState<Agent[]>([])
  const [messages, setMessages] = useState<Message[]>([])
  const [newAgentId, setNewAgentId] = useState<string>('')
  const [newAgentName, setNewAgentName] = useState<string>('')
  const [newAgentChannel, setNewAgentChannel] = useState<string>('default')
  const [selectedAgent, setSelectedAgent] = useState<string>('')
  const [runPrompt, setRunPrompt] = useState<string>('Hello from the frontend')
  const [runResult, setRunResult] = useState<string>('')

  const loadStatus = async () => {
    try {
      const resp = await fetch('/api/v1/health')
      const data = await resp.json()
      setStatus(data.status)
    } catch {
      setStatus('offline')
    }
  }

  const loadAgents = async () => {
    try {
      const resp = await fetch('/api/v1/agents')
      const data = await resp.json()
      setAgents(data.agents || [])
      if (data.agents?.length && !selectedAgent) {
        setSelectedAgent(data.agents[0])
      }
    } catch {
      setAgents([])
    }
  }

  const loadMessages = async () => {
    try {
      const resp = await fetch('/api/v1/messages')
      const data = await resp.json()
      setMessages(data)
    } catch {
      setMessages([])
    }
  }

  useEffect(() => {
    loadStatus()
    loadAgents()
    loadMessages()
  }, [])

  const createAgent = async () => {
    if (!newAgentId) return
    const config = {
      name: newAgentName || newAgentId,
      channels: [newAgentChannel],
      system_prompt: `You are ${newAgentName || newAgentId}.`,
      model: 'gpt-4o-mini',
    }
    const resp = await fetch('/api/v1/agents', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ agent_id: newAgentId, config }),
    })
    if (resp.ok) {
      setNewAgentId('')
      setNewAgentName('')
      setRunResult('Agent created successfully')
      await loadAgents()
    } else {
      const data = await resp.json()
      setRunResult(`Error: ${data.detail || resp.statusText}`)
    }
  }

  const runWorkflow = async (template?: string) => {
    if (!selectedAgent) return
    const payload: Record<string, any> = {
      channel: newAgentChannel,
      text: runPrompt,
      runtime: 'openai',
    }
    if (template) {
      payload.template = template
    }
    const resp = await fetch(`/api/v1/agents/${selectedAgent}/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
    const data = await resp.json()
    if (resp.ok) {
      setRunResult(JSON.stringify(data, null, 2))
      await loadMessages()
    } else {
      setRunResult(`Error: ${data.detail || resp.statusText}`)
    }
  }

  return (
    <div style={{ fontFamily: 'system-ui, sans-serif', padding: 24, maxWidth: 960, margin: '0 auto' }}>
      <h1>AI Agent Orchestration</h1>
      <p>Backend status: <strong>{status}</strong></p>

      <section style={{ marginBottom: 24 }}>
        <h2>Create an Agent</h2>
        <div style={{ display: 'grid', gap: 12, maxWidth: 600 }}>
          <input
            value={newAgentId}
            onChange={(event) => setNewAgentId(event.target.value)}
            placeholder="Agent ID"
          />
          <input
            value={newAgentName}
            onChange={(event) => setNewAgentName(event.target.value)}
            placeholder="Agent name"
          />
          <input
            value={newAgentChannel}
            onChange={(event) => setNewAgentChannel(event.target.value)}
            placeholder="Channel (default or slack:#general)"
          />
          <button onClick={createAgent}>Create agent</button>
        </div>
      </section>

      <section style={{ marginBottom: 24 }}>
        <h2>Agents</h2>
        {agents.length ? (
          <div>
            <select value={selectedAgent} onChange={(event) => setSelectedAgent(event.target.value)}>
              {agents.map((agent) => (
                <option key={agent.agent_id} value={agent.agent_id}>
                  {agent.agent_id}
                </option>
              ))}
            </select>
          </div>
        ) : (
          <p>No agents found yet.</p>
        )}
      </section>

      <section style={{ marginBottom: 24 }}>
        <h2>Run Workflow</h2>
        <textarea
          rows={3}
          style={{ width: '100%', marginBottom: 12 }}
          value={runPrompt}
          onChange={(event) => setRunPrompt(event.target.value)}
        />
        <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
          <button onClick={() => runWorkflow()}>Run openai workflow</button>
          <button onClick={() => runWorkflow('two-agent-conversation')}>
            Run two-agent conversation template
          </button>
          <button onClick={() => runWorkflow('slack-broadcast')}>Run Slack broadcast template</button>
        </div>
        <pre style={{ background: '#f6f6f6', padding: 16, marginTop: 12, whiteSpace: 'pre-wrap' }}>{runResult}</pre>
      </section>

      <section>
        <h2>Message History</h2>
        {messages.length ? (
          <div style={{ display: 'grid', gap: 12 }}>
            {messages.map((message) => (
              <div key={message.id} style={{ padding: 12, border: '1px solid #ddd', borderRadius: 8 }}>
                <div style={{ fontSize: 12, color: '#666' }}>
                  <strong>{message.sender}</strong> ({message.role}) - <em>{message.channel}</em> - {new Date(message.created_at).toLocaleString()}
                </div>
                <div style={{ marginTop: 8 }}>{message.text}</div>
              </div>
            ))}
          </div>
        ) : (
          <p>No messages persisted yet.</p>
        )}
      </section>
    </div>
  )
}
