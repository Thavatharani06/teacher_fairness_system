function StatCard({ title, value }) {
  return (
    <div className="card stat-card">
      <h3>{title}</h3>
      <p>{value}</p>
    </div>
  );
}

export default function DashboardSummary({ stats }) {
  return (
    <div className="stats-grid">
      <StatCard title="Total Evaluations" value={stats.total_evaluations ?? 0} />
      <StatCard title="Fair" value={stats.fair_count ?? 0} />
      <StatCard title="Undervalued" value={stats.undervalued_count ?? 0} />
      <StatCard title="Overvalued" value={stats.overvalued_count ?? 0} />
      <StatCard title="Anomalies" value={stats.anomalies_count ?? 0} />
    </div>
  );
}
