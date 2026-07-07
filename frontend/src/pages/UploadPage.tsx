import { useState } from "react";
import { AnalysisResult, uploadAnalyses } from "../api";
import FileUploader from "../components/FileUploader";

type Props = {
  onResults: (results: AnalysisResult[]) => void;
};

export default function UploadPage({ onResults }: Props) {
  const [files, setFiles] = useState<File[]>([]);
  const [smoothing, setSmoothing] = useState("Savitzky-Golay");
  const [smoothWindow, setSmoothWindow] = useState(17);
  const [removeOutliers, setRemoveOutliers] = useState(true);
  const [cropFailure, setCropFailure] = useState(true);
  const [modulusMin, setModulusMin] = useState(0.005);
  const [modulusMax, setModulusMax] = useState(0.08);
  const [loading, setLoading] = useState(false);

  async function handleUpload() {
    setLoading(true);

    try {
      const results = await uploadAnalyses(files, {
        smoothing,
        smooth_window: smoothWindow,
        remove_outliers: removeOutliers,
        crop_failure: cropFailure,
        modulus_min: modulusMin,
        modulus_max: modulusMax,
      });
      onResults(results);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="panel upload-grid">
      <div>
        <h2>Upload mechanical-testing data</h2>
        <p>
          Supports CSV, TXT, DAT, TSV, XLSX, XLS, and ZIP batches exported from mechanical-testing workflows.
        </p>
        <FileUploader files={files} onFiles={setFiles} />
        <button className="primary-button" disabled={!files.length || loading} onClick={handleUpload}>
          {loading ? "Analyzing..." : "Analyze files"}
        </button>
      </div>

      <div>
        <h2>Analysis settings</h2>
        <div className="settings-grid">
          <label>
            Smoothing
            <select value={smoothing} onChange={(event) => setSmoothing(event.target.value)}>
              <option>Savitzky-Golay</option>
              <option>Moving average</option>
              <option>None</option>
            </select>
          </label>

          <label>
            Smoothing window
            <input
              type="number"
              min={5}
              step={2}
              value={smoothWindow}
              onChange={(event) => setSmoothWindow(Number(event.target.value))}
            />
          </label>

          <label>
            Modulus start strain
            <input
              type="number"
              step={0.005}
              value={modulusMin}
              onChange={(event) => setModulusMin(Number(event.target.value))}
            />
          </label>

          <label>
            Modulus end strain
            <input
              type="number"
              step={0.005}
              value={modulusMax}
              onChange={(event) => setModulusMax(Number(event.target.value))}
            />
          </label>

          <label className="checkbox-label">
            <input
              type="checkbox"
              checked={removeOutliers}
              onChange={(event) => setRemoveOutliers(event.target.checked)}
            />
            Remove spike outliers
          </label>

          <label className="checkbox-label">
            <input
              type="checkbox"
              checked={cropFailure}
              onChange={(event) => setCropFailure(event.target.checked)}
            />
            Crop after confirmed failure
          </label>
        </div>
      </div>
    </section>
  );
}
