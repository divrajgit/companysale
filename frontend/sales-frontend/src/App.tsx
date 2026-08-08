import React, { useEffect, useState } from "react";
import { Sidebar } from "./components/Sidebar";
import { ProjectsTable } from "./components/ProjectsTable";
import { fetchSaleItems } from "./api";

function App() {
  const [items, setItems] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSaleItems()
      .then((data) => {
        setItems(data);
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="loading">Loading…</div>;

  return (
    <div className="app">
      <Sidebar />
      <main className="main">
        <header className="main-header">
          <div>
            <h1>The Body Shop Sale Dashboard</h1>
            <p>Live snapshot of discounted products scraped from the site.</p>
          </div>
          <div className="header-actions">
            <button className="icon-button">?</button>
          </div>
        </header>

        <section className="cards-row">
          <div className="card">
            <div className="card-title">Sale items</div>
            <div className="card-subtitle">{items.length} items with 50%+ discount</div>
          </div>
        </section>

        <section>
          <ProjectsTable items={items} />
        </section>
      </main>
    </div>
  );
}

export default App;
