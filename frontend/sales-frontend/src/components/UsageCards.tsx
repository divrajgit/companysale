import React from "react";

export const CurrentCycleCard = ({ data }: any) => (
  <div className="card">
    <div className="card-title">Current cycle</div>
    <div className="card-subtitle">
      Current cycle counters and what your plan includes
    </div>

    <div className="card-grid">
      <div>
        <div className="label">Projects (lifetime)</div>
        <div className="value">
          {data.projectsLifetime.used} / {data.projectsLifetime.limit ?? "Unlimited"}
        </div>
      </div>

      <div>
        <div className="label">Build minutes</div>
        <div className="value">
          {data.buildMinutes.used} / {data.buildMinutes.limit}
        </div>
      </div>

      <div>
        <div className="label">Bandwidth</div>
        <div className="value">
          {data.bandwidth.comingSoon ? "Coming soon" : "-"}
        </div>
      </div>

      <div>
        <div className="label">Custom domains</div>
        <div className="value">
          {data.customDomains.used} / {data.customDomains.limit ?? "Unlimited"}
        </div>
      </div>

      <div>
        <div className="label">Team members</div>
        <div className="value">
          {data.teamMembers.used} / {data.teamMembers.limit}
        </div>
      </div>

      <div>
        <div className="label">Reset date</div>
        <div className="value">{data.resetDate}</div>
      </div>

      <div>
        <div className="label">Plan type</div>
        <div className="value">{data.planType}</div>
      </div>
    </div>
  </div>
);

export const LiveUsageCard = ({ data }: any) => (
  <div className="card">
    <div className="card-title">Live resource usage</div>

    <div className="card-grid">
      <div>
        <div className="label">CPU</div>
        <div className="value">{data.cpuCores} cores</div>
      </div>

      <div>
        <div className="label">Memory</div>
        <div className="value">{data.memoryMiB} MiB</div>
      </div>

      <div>
        <div className="label">Containers</div>
        <div className="value">{data.containers}</div>
      </div>

      <div>
        <div className="label">Egress</div>
        <div className="value">{data.egressKibPerSec} KiB/s</div>
      </div>
    </div>
  </div>
);

