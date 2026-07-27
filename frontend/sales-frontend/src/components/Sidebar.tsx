import React from "react";
import "./Sidebar.css";

const items = [
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

export const Sidebar: React.FC = () => {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="team-name">cistekai-dev’s Team</div>
      </div>
      <nav>
        {items.map(item => (
          <div
            key={item}
            className={`sidebar-item ${item === "Usage" ? "active" : ""}`}
          >
            {item}
          </div>
        ))}
      </nav>
      <div className="sidebar-footer">
        <div className="user-email">cistekai-dev</div>
        <div className="user-email-sub">hi@cistekai.com</div>
      </div>
    </aside>
  );
};

