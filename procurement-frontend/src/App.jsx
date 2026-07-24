import { useState } from "react";
import FileUpload from "./components/FileUpload";
import Result from "./components/Result";
import "./App.css";

function App() {
  const [result, setResult] = useState(null);

  return (
    <div className="app">
      {/* ── Header ── */}
      <header className="app-header">
        <div className="header-left">
          <div className="logo-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path d="M12 2L2 7l10 5 10-5-10-5z" fill="currentColor" opacity="0.8"/>
              <path d="M2 17l10 5 10-5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M2 12l10 5 10-5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </div>
          <span className="logo-text">AI Procurement Agent</span>
        </div>
        <nav className="header-nav">
          <a href="#" className="nav-link active">Upload PDFs</a>
          <a href="#" className="nav-link">Dashboard</a>
        </nav>
      </header>

      {/* ── Main Content ── */}
      <main className="app-main">
        <FileUpload setResult={setResult} />
        <Result result={result} />
      </main>
    </div>
  );
}

export default App;
