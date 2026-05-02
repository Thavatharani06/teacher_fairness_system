import { useEffect, useState } from "react";

import {
  exportEvaluationsCsv,
  fetchDashboardStats,
  fetchEvaluations,
  fetchTeacherScores,
} from "./api/client";
import DashboardSummary from "./components/DashboardSummary";
import FairnessChart from "./components/FairnessChart";
import FiltersBar from "./components/FiltersBar";
import StudentTable from "./components/StudentTable";
import TeacherFairnessChart from "./components/TeacherFairnessChart";

const initialFilters = {
  search: "",
  teacher: "",
  fairness_result: "",
  sentiment_label: "",
};

export default function App() {
  const [stats, setStats] = useState({});
  const [teacherStats, setTeacherStats] = useState([]);
  const [rows, setRows] = useState([]);
  const [filters, setFilters] = useState(initialFilters);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try {
        const [dashboardData, teacherData, evaluationsData] = await Promise.all([
          fetchDashboardStats(),
          fetchTeacherScores(),
          fetchEvaluations(filters),
        ]);
        setStats(dashboardData);
        setTeacherStats(teacherData);
        setRows(evaluationsData);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [filters]);

  const handleFilterChange = (key, value) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  };

  const handleExport = async () => {
    const blob = await exportEvaluationsCsv(filters);
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", "evaluations.csv");
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  };

  return (
    <main className="container">
      <header className="header">
        <h1>Teacher Fairness & Academic Evaluation Dashboard</h1>
      </header>
      <DashboardSummary stats={stats} />
      <div className="charts-grid">
        <FairnessChart stats={stats} />
        <TeacherFairnessChart teacherStats={teacherStats} />
      </div>
      <FiltersBar filters={filters} onChange={handleFilterChange} onExport={handleExport} />
      {loading ? <p>Loading...</p> : <StudentTable rows={rows} />}
    </main>
  );
}
