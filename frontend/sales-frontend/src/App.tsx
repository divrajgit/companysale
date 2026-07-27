import React, { useEffect, useState } from "react";
import { Sidebar } from "./components/Sidebar";
import { CurrentCycleCard, LiveUsageCard } from "./components/UsageCards";
import { ProjectsTable } from "./components/ProjectsTable";
import { fetchUsage, fetchProjects } from "./api";

function App() {
  const [usage, setUsage] = useState<any>(null);
  const [projects, setProjects] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([fetchUsage(), fetchProjects()]).then(([u, p]) => {
      setUsage(u);
      setProjects(p);
      setLoading(false);
    });
  }, []);

  if (loading || !usage) return <div className="loading">Loading…</div>;

  return (
    <div className="app">
      <Sidebar />
      <main className="main">
        <header className="main-header">
          <div>
            <h1>Usage</h1>
            <p>Current cycle counters and what your plan includes.</p>
          </div>
          <div className="header-actions">
            <button className="icon-button">⟳</button>
            <button className="primary-button">+ New</button>
          </div>
        </header>

        <section className="cards-row">
          <CurrentCycleCard data={usage.currentCycle} />
          <LiveUsageCard data={usage.liveResourceUsage} />
        </section>

        <section>
          <ProjectsTable projects={projects} />
        </section>
      </main>
    </div>
  );
}

export default App;

