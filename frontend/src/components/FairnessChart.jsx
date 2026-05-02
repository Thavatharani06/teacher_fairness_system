import { ArcElement, Chart as ChartJS, Legend, Tooltip } from "chart.js";
import { Pie } from "react-chartjs-2";

ChartJS.register(ArcElement, Tooltip, Legend);

export default function FairnessChart({ stats }) {
  const data = {
    labels: ["Fair", "Undervalued", "Overvalued"],
    datasets: [
      {
        data: [stats.fair_count ?? 0, stats.undervalued_count ?? 0, stats.overvalued_count ?? 0],
        backgroundColor: ["#16a34a", "#dc2626", "#f97316"],
      },
    ],
  };
  return (
    <div className="card chart-card">
      <h3>Fair vs Under vs Over</h3>
      <Pie data={data} />
    </div>
  );
}
