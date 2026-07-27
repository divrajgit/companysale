import React from "react";

export const ProjectsTable = ({ projects }: any) => (
  <div className="card">
    <div className="card-title">Breakdown by project</div>
    <div className="card-subtitle">{projects.length} projects active</div>

    <table className="projects-table">
      <thead>
        <tr>
          <th>Project</th>
          <th>CPU</th>
          <th>Memory</th>
          <th>Egress</th>
        </tr>
      </thead>

      <tbody>
        {projects.map((p: any) => (
          <tr key={p.name}>
            <td>{p.name}</td>
            <td>{p.cpuCores} cores</td>
            <td>{p.memoryMiB} MiB</td>
            <td>{p.egressKibPerSec} KiB/s</td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
);

