const fairnessClass = {
  fair: "status-fair",
  undervalued: "status-under",
  overvalued: "status-over",
};

export default function StudentTable({ rows }) {
  return (
    <div className="card table-wrap">
      <h3>Evaluations</h3>
      <table>
        <thead>
          <tr>
            <th>Student</th>
            <th>Teacher</th>
            <th>Expected</th>
            <th>Teacher Score</th>
            <th>Fairness</th>
            <th>Sentiment</th>
            <th>Risk</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row._id || `${row.student_id}-${row.teacher}`}>
              <td>{row.student_name}</td>
              <td>{row.teacher}</td>
              <td>{row.expected_score}</td>
              <td>{row.teacher_score}</td>
              <td className={fairnessClass[row.fairness_result]}>{row.fairness_result}</td>
              <td>{row.sentiment_label}</td>
              <td>{row.is_anomaly || row.fairness_result === "undervalued" ? "High" : "Low"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
