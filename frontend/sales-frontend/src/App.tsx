import React, { useEffect, useState } from "react";
import { Sidebar } from "./components/Sidebar";
import { ProjectsTable } from "./components/ProjectsTable";
import { fetchSaleItems } from "./api";

const navItems = [
  "Projects (10)",
  "Activity (15)",
  "Observability",
  "Domains",
  "Integrations",
  "Security",
  "Usage",
  "Organization",
  "Settings",
  "Support",
];

function App() {
  const [items, setItems] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeSection, setActiveSection] = useState(navItems[1]);
  const [selectedSite, setSelectedSite] = useState("All sites");

  useEffect(() => {
    fetchSaleItems()
      .then((data) => {
        setItems(data);
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="loading">Loading…</div>;

  const siteNames = Array.from(
    new Set(items.map((item) => item.site_name || item.site || "Unknown"))
  );
  const siteCount = siteNames.length;
  const siteOptions = ["All sites", ...siteNames];
  const filteredItems =
    selectedSite === "All sites"
      ? items
      : items.filter((item) => (item.site_name || item.site || "Unknown") === selectedSite);

  const sectionContent = () => {
    if (activeSection === "Projects (10)") {
      return <ProjectsTable items={items} />;
    }

    if (activeSection === "Activity (15)") {
      return (
        <div className="card">
          <div className="card-title">Recent activity</div>
          <div className="card-subtitle">
            Latest discounted products found across monitored sites.
          </div>
          {items.length ? (
            <ul>
              {items.slice(0, 5).map((item) => (
                <li key={item.url}>
                  <strong>{item.name}</strong> — {item.discount_percent}% off
                </li>
              ))}
            </ul>
          ) : (
            <p>No sale activity is available yet.</p>
          )}
        </div>
      );
    }

    return (
      <div className="card">
        <div className="card-title">{activeSection}</div>
        <div className="card-subtitle">Select a sidebar section to view details here.</div>
        <p>
          This dashboard monitors sales and strong markdowns from the configured sites.
        </p>
      </div>
    );
  };

  return (
    <div className="app">
      <Sidebar activeItem={activeSection} onSelect={setActiveSection} />
      <main className="main">
        <header className="main-header">
          <div>
            <h1>CompanySale Discount Dashboard</h1>
            <p>Live snapshot of discounted products scraped from multiple configured sites.</p>
          </div>
          <div className="header-actions">
            <button className="icon-button">?</button>
          </div>
        </header>

        <section className="cards-row">
          <div className="card">
            <div className="card-title">Sale items across sites</div>
            <div className="card-subtitle">
              {filteredItems.length} items with 30%+ discount or strong markdowns across {siteCount} sites
            </div>
          </div>
          <div className="card">
            <div className="card-title">Filter by site</div>
            <div className="card-subtitle">Choose one site to filter dashboard results.</div>
            <select
              className="site-filter"
              value={selectedSite}
              onChange={(event) => setSelectedSite(event.target.value)}
            >
              {siteOptions.map((site) => (
                <option key={site} value={site}>
                  {site}
                </option>
              ))}
            </select>
          </div>
        </section>

        <section>{sectionContent()}</section>
      </main>
    </div>
  );
}

export default App;
