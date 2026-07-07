import Plot from "react-plotly.js";
import { AnalysisResult } from "../api";

type Props = {
  results: AnalysisResult[];
};

export default function StressStrainChart({ results }: Props) {
  const traces = results.map((result) => ({
    x: result.clean_data.map((row) => Number(row.Strain)),
    y: result.clean_data.map((row) => Number(row.Stress_MPa)),
    type: "scatter" as const,
    mode: result.data_type === "summary" ? "markers" : "lines",
    name: result.filename,
  }));

  return (
    <Plot
      data={traces}
      layout={{
        autosize: true,
        height: 560,
        paper_bgcolor: "#080a0f",
        plot_bgcolor: "#080a0f",
        font: { color: "#f5f3ee" },
        title: "Stress-Strain Curves",
        xaxis: { title: "Strain (mm/mm)", gridcolor: "rgba(255,255,255,0.08)" },
        yaxis: { title: "Stress (MPa)", gridcolor: "rgba(255,255,255,0.08)" },
        margin: { l: 55, r: 20, t: 60, b: 50 },
      }}
      useResizeHandler
      style={{ width: "100%" }}
    />
  );
}
