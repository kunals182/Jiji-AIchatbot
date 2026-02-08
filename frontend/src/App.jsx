import { useState } from 'react'
import { Send, FileText, Video, Sparkles } from 'lucide-react'
import './App.css'

function App() {
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [response, setResponse] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!query.trim()) return

    setLoading(true)
    setResponse(null)
    
    // Simulate a slight delay for "thinking" effect if backend is too fast
    // await new Promise(r => setTimeout(r, 800))

    try {
      const res = await fetch('http://127.0.0.1:8000/ask-jiji', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      })
      
      if (!res.ok) throw new Error('Failed to fetch')
      
      const data = await res.json()
      setResponse(data)
    } catch (err) {
      console.error(err)
      setResponse({ 
        answer: "I'm having trouble connecting to my brain (the backend). Please make sure the Python server is running!", 
        resources: [] 
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <div className="card-main">
        {/* Header */}
        <div className="header">
          <h1>Jiji</h1>
          <p>Your AI Friend</p>
          <div className="avatar-container">
            <img 
              src="https://img.freepik.com/free-photo/view-3d-woman-using-laptop_23-2150709818.jpg?t=st=1707989000~exp=1707992600~hmac=..." 
              alt="Jiji Avatar" 
              className="avatar-img"
              onError={(e) => {e.target.src = 'https://api.dicebear.com/7.x/avataaars/svg?seed=Jiji'}}
            />
          </div>
        </div>

        {/* Search Input */}
        <form onSubmit={handleSubmit} className="search-box">
          <Sparkles className="icon-search" size={20} />
          <input 
            type="text" 
            placeholder="Explain RAG" 
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={loading}
          />
          <button type="submit" disabled={loading || !query.trim()}>
            {loading ? <div className="spinner"></div> : <Send size={20} />}
          </button>
        </form>

        {/* Response Area */}
        {(response || loading) && (
          <div className="response-area fade-in">
            <h3>Jiji says</h3>
            
            {loading ? (
              <p className="thinking-text">Thinking...</p>
            ) : (
              <div className="response-content">
                <p>{response.answer}</p>
                
                {response.resources && response.resources.length > 0 && (
                  <div className="resources-list">
                    {response.resources.map((res, idx) => (
                      <a 
                        key={idx} 
                        href={res.url} 
                        target="_blank" 
                        rel="noopener noreferrer" 
                        className="resource-card"
                      >
                        <div className={`icon-box ${res.type}`}>
                          {res.type === 'video' ? <Video size={24} /> : <FileText size={24} />}
                        </div>
                        <div className="resource-info">
                          <h4>{res.title}</h4>
                          <span>{res.type === 'video' ? 'Video' : 'Presentation'}</span>
                        </div>
                        <div className="action-btn">
                          {res.type === 'video' ? 'Watch' : 'Open'}
                        </div>
                      </a>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default App
