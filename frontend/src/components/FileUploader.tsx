type Props = {
  files: File[];
  onFiles: (files: File[]) => void;
};

export default function FileUploader({ files, onFiles }: Props) {
  return (
    <div className="file-drop">
      <label>
        Select files
        <input
          type="file"
          multiple
          accept=".csv,.xlsx,.xls,.txt,.dat,.tsv,.zip"
          onChange={(event) => onFiles(Array.from(event.target.files || []))}
        />
      </label>

      {files.length > 0 && (
        <div>
          <p>{files.length} file(s) selected</p>
          <ul>
            {files.map((file) => (
              <li key={`${file.name}-${file.size}`}>{file.name}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
