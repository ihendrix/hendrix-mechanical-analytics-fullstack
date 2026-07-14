import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export type MetricSummary = {
  maximum_load_n: number | null;
  peak_stress_mpa: number | null;
  strain_at_peak: number | null;
  youngs_modulus_mpa: number | null;
  modulus_r2: number | null;
  modulus_fit: string | null;
  area_under_curve: number | null;
  rows: number;
};

export type AnalysisResult = {
  id: number;
  filename: string;
  sample: string | null;
  detected_strain_column: string | null;
  detected_stress_column: string | null;
  data_type: string;
  status: string;
  warnings: string[];
  metrics: MetricSummary;
  clean_data: Array<Record<string, string | number | null>>;
};

export async function uploadAnalyses(files: File[], settings: Record<string, string | number | boolean>) {
  const formData = new FormData();

  files.forEach((file) => formData.append("files", file));

  Object.entries(settings).forEach(([key, value]) => {
    formData.append(key, String(value));
  });

  const response = await axios.post(
  `${API_BASE_URL}/api/analyses/upload`,
  formData
);

  return response.data.results as AnalysisResult[];
}

export async function listAnalyses() {
  const response = await axios.get(`${API_BASE_URL}/api/analyses/`);
  return response.data;
}
