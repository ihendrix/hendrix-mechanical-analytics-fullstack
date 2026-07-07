import { AnalysisResult } from "../api";

type Props = {
  results: AnalysisResult[];
};

function format(value: number | null | undefined, decimals = 3) {
  if (value === null || value === undefined || Number.isNaN(value)) return "—";
  return value.toFixed(decimals);
}

export default function MetricsCards({ results }: Props) {
  const rows = results.reduce((sum, result) => sum + result.metrics.rows, 0);
  const maxStress = Math.max(...results.map((result) => result.metrics.peak_stress_mpa || 0));
  const moduli = results
    .map((result) => result.metrics.youngs_modulus_mpa)
    .filter((value): value is number => typeof value === "number");
  const meanModulus = moduli.length ? moduli.reduce((sum, value) => sum + value, 0) / moduli.length : null;

  return (
    <section className="metrics-grid">
      <div className="metric-card">
        <div className="metric-label">Files analyzed</div>
        <div className="metric-value">{results.length}</div>
      </div>
      <div className="metric-card">
        <div className="metric-label">Clean rows</div>
        <div className="metric-value">{rows}</div>
      </div>
      <div className="metric-card">
        <div className="metric-label">Max stress</div>
        <div className="metric-value">{format(maxStress)} MPa</div>
      </div>
      <div className="metric-card">
        <div className="metric-label">Mean modulus</div>
        <div className="metric-value">{format(meanModulus)} MPa</div>
      </div>
    </section>
  );
}
