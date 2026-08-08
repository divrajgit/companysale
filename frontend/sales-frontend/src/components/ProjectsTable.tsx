import React from "react";

export const ProjectsTable = ({ items }: any) => (
  <div className="card">
    <div className="card-title">Discounted products</div>
    <div className="card-subtitle">Products found with a strong markdown</div>

    <table className="projects-table">
      <thead>
        <tr>
          <th>Product</th>
          <th>Old price</th>
          <th>New price</th>
          <th>Discount</th>
          <th>Site</th>
          <th>Link</th>
        </tr>
      </thead>

      <tbody>
        {items.map((item: any) => (
          <tr key={`${item.url}-${item.site_key || item.site_name || item.name}`}>
            <td>{item.name}</td>
            <td>${item.old_price.toFixed(2)}</td>
            <td>${item.new_price.toFixed(2)}</td>
            <td>{item.discount_percent}%</td>
            <td>{item.site_name || item.site_key || "Unknown"}</td>
            <td>
              <a href={item.url} target="_blank" rel="noreferrer">
                View
              </a>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
);
