import { AnalysisResult } from "../api";

type Props = {
  results: AnalysisResult[];
};

function format(value: number | null | undefined, decimals = 5) {
  if (value === null || value === undefined || Number.isNaN(value)) return "—";
  return value.toFixed(decimals);
}

export default function ResultsTable({ results }: Props) {
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>File</th>
            <th>Status</th>
            <th>Peak Stress MPa</th>
            <th>Strain at Peak</th>
            <th>Young's Modulus MPa</th>
            <th>Modulus R²</th>
            <th>Area Under Curve</th>
            <th>Rows</th>
          </tr>
        </thead>
        <tbody>
          {results.map((result) => (
            <tr key={result.id}>
              <td>{result.filename}</td>
              <td><span className="status">{result.status}</span></td>
              <td>{format(result.metrics.peak_stress_mpa)}</td>
              <td>{format(result.metrics.strain_at_peak)}</td>
              <td>{format(result.metrics.youngs_modulus_mpa)}</td>
              <td>{format(result.metrics.modulus_r2)}</td>
              <td>{format(result.metrics.area_under_curve)}</td>
              <td>{result.metrics.rows}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
