import { AnalysisResult } from "../api";
import MetricsCards from "../components/MetricsCards";
import ResultsTable from "../components/ResultsTable";
import StressStrainChart from "../components/StressStrainChart";

type Props = {
  results: AnalysisResult[];
};

export default function DashboardPage({ results }: Props) {
  if (!results.length) {
    return (
      <section className="panel">
        <h2>Dashboard preview</h2>
        <p>Upload files to generate stress-strain charts, metrics, warnings, and saved analysis records.</p>
      </section>
    );
  }

  return (
    <>
      <MetricsCards results={results} />

      <section className="panel">
        <h2>Stress-strain analysis</h2>
        <StressStrainChart results={results} />
      </section>

      <section className="panel">
        <h2>Material property summary</h2>
        <ResultsTable results={results} />
      </section>

      <section className="panel">
        <h2>Cleaning notes</h2>
        {results.map((result) => (
          <div key={result.id}>
            <strong>{result.filename}</strong>
            <ul>
              {result.warnings.slice(0, 8).map((warning) => (
                <li key={warning}>{warning}</li>
              ))}
            </ul>
          </div>
        ))}
      </section>
    </>
  );
}
