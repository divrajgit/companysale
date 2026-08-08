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

interface SidebarProps {
  activeItem: string;
  onSelect: (item: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeItem, onSelect }) => (
  <aside className="sidebar">
    <div className="sidebar-header">
      <div className="team-name">CompanySale Team</div>
    </div>
    <nav>
      {items.map((item) => (
        <button
          key={item}
          type="button"
          className={`sidebar-item ${item === activeItem ? "active" : ""}`}
          onClick={() => onSelect(item)}
          aria-current={item === activeItem ? "page" : undefined}
        >
          {item}
        </button>
      ))}
    </nav>
    <div className="sidebar-footer">
      <div className="user-email">support@companysale.com</div>
      <div className="user-email-sub">CompanySale dashboard</div>
    </div>
  </aside>
);
