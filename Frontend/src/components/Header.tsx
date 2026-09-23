import { Bell, ChevronDown, Search, ShieldCheck } from 'lucide-react'

interface HeaderProps {
  query: string
  onQueryChange: (value: string) => void
  onSubmit: () => void
}

export function Header({ query, onQueryChange, onSubmit }: HeaderProps) {
  return (
    <header className="app-header">
      <div className="brand-lockup">
        <div className="brand-mark"><ShieldCheck size={18} strokeWidth={2.5} /></div>
        <div><div className="brand-name">MoneyGraph</div><div className="brand-subtitle">AML NETWORK ANALYTICS</div></div>
      </div>
      <form className="search-wrap" onSubmit={(event) => { event.preventDefault(); onSubmit() }}>
        <Search size={17} />
        <input value={query} onChange={(event) => onQueryChange(event.target.value)} placeholder="Search by GID…" aria-label="Search by GID" />
        <kbd>⌘ K</kbd>
      </form>
      <div className="header-stats">
        <div className="header-stat"><span className="stat-label">NODES</span><strong>2,248</strong></div>
        <div className="header-stat"><span className="stat-label">CONNECTIONS</span><strong>3,119</strong></div>
        <div className="header-stat"><span className="stat-label">CLUSTERS</span><strong>18</strong></div>
      </div>
      <div className="header-actions"><button className="icon-button" aria-label="Notifications"><Bell size={17} /></button><div className="avatar">AK</div><ChevronDown size={15} className="muted-icon" /></div>
    </header>
  )
}
