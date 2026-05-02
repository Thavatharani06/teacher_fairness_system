import { BarElement, CategoryScale, Chart as ChartJS, Legend, LinearScale, Tooltip } from "chart.js";
import { Bar } from "react-chartjs-2";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

export default function TeacherFairnessChart({ teacherStats }) {
  const data = {
    labels: teacherStats.map((item) => item.teacher),
    datasets: [
      {
        label: "Avg Fairness Score",
        data: teacherStats.map((item) => item.average_fairness_score),
        backgroundColor: teacherStats.map((item) => (item.is_bias_flagged ? "#dc2626" : "#16a34a")),
      },
    ],
  };
  return (
    <div className="card chart-card">
      <h3>Teacher-wise Fairness Score</h3>
      <Bar data={data} />
    </div>
  );
}
