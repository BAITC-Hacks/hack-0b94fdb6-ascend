import { Bell, ChevronDown, Download, Search, ShieldCheck } from 'lucide-react'

interface HeaderProps {
  query: string
  onQueryChange: (value: string) => void
  onSubmit: () => void
  searchError: boolean
  onDownload: (type: 'nodes' | 'clusters' | 'top') => void
}

export function Header({ query, onQueryChange, onSubmit, searchError, onDownload }: HeaderProps) {
  return (
    <header className="app-header">
      <div className="brand-lockup">
        <div className="brand-mark"><ShieldCheck size={18} strokeWidth={2.5} /></div>
        <div><div className="brand-name">Freedom Graph</div><div className="brand-subtitle">AML INTELLIGENCE · FREEDOM BANK</div></div>
      </div>
      <form className="search-wrap" onSubmit={(event) => { event.preventDefault(); onSubmit() }}>
        <Search size={17} />
        <input value={query} onChange={(event) => onQueryChange(event.target.value)} placeholder="Найти GID…" aria-label="Поиск по GID" />
        <kbd>⌘ K</kbd>
      </form>
      {searchError && <span className="search-error" role="status">GID не найден</span>}
      <div className="header-stats">
        <div className="header-stat"><span className="stat-label">УЗЛОВ</span><strong>2 248</strong></div>
        <div className="header-stat"><span className="stat-label">РЁБЕР</span><strong>3 119</strong></div>
        <div className="header-stat"><span className="stat-label">SEED</span><strong>81</strong></div>
        <div className="header-stat"><span className="stat-label">КЛАСТЕРОВ</span><strong>18</strong></div>
        <div className="header-stat"><span className="stat-label">ОБОРОТ</span><strong>₸365.9M</strong></div>
      </div>
      <div className="run-snapshot"><span>СНИМОК FGI-2026-07</span><strong>01–31 ИЮЛ 2026</strong></div>
      <div className="header-actions"><details className="export-menu"><summary className="icon-button" aria-label="Скачать CSV"><Download size={16} /></summary><div className="export-menu__list"><span>Текущий snapshot</span><button onClick={() => onDownload('nodes')}>nodes_roles.csv</button><button onClick={() => onDownload('clusters')}>clusters.csv</button><button onClick={() => onDownload('top')}>top_nodes.csv</button></div></details><button className="icon-button" aria-label="Уведомления"><Bell size={17} /></button><div className="avatar">AK</div><ChevronDown size={15} className="muted-icon" /></div>
    </header>
  )
}
