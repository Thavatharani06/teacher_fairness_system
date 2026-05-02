export default function FiltersBar({ filters, onChange, onExport }) {
  return (
    <div className="card filters-row">
      <input
        placeholder="Search student or teacher..."
        value={filters.search}
        onChange={(e) => onChange("search", e.target.value)}
      />
      <input
        placeholder="Teacher"
        value={filters.teacher}
        onChange={(e) => onChange("teacher", e.target.value)}
      />
      <select value={filters.fairness_result} onChange={(e) => onChange("fairness_result", e.target.value)}>
        <option value="">All Fairness</option>
        <option value="fair">Fair</option>
        <option value="undervalued">Undervalued</option>
        <option value="overvalued">Overvalued</option>
      </select>
      <select value={filters.sentiment_label} onChange={(e) => onChange("sentiment_label", e.target.value)}>
        <option value="">All Sentiments</option>
        <option value="positive">Positive</option>
        <option value="neutral">Neutral</option>
        <option value="negative">Negative</option>
      </select>
      <button type="button" onClick={onExport}>
        Export CSV
      </button>
    </div>
  );
}
