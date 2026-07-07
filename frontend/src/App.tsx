import { useState } from "react";
import { AnalysisResult } from "./api";
import DashboardPage from "./pages/DashboardPage";
import UploadPage from "./pages/UploadPage";

export default function App() {
  const [results, setResults] = useState<AnalysisResult[]>([]);

  return (
    <main className="app-shell">
      <section className="hero">
        <p className="eyebrow">Full-Stack Research Software</p>
        <h1>Hendrix Mechanical Analytics</h1>
        <p>
          Upload mechanical-testing datasets, process stress-strain curves through a FastAPI backend,
          visualize material behavior, and store analysis runs for reproducible review.
        </p>
      </section>

      <UploadPage onResults={setResults} />
      <DashboardPage results={results} />
    </main>
  );
}
