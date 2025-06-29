import { useState } from "react";

function JsonToPdf() {
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile && selectedFile.type === "application/json") {
      setFile(selectedFile);
      setError("");
    } else {
      setError("Please upload a valid JSON file");
      setFile(null);
    }
  };
  const convertToPDF = async () => {
    if (!file) return;
    setIsLoading(true);
    setError("");
    try {
      const formData = new FormData();
      formData.append("file", file);
      const response = await fetch("/api/convert/json-to-pdf", {
        method: "POST",
        body: formData,
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Error converting file");
      }
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = "converted.pdf";
      link.click();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError(err.message || "Error converting JSON to PDF");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };
  return (
    <div className="max-w-md mx-auto bg-white p-8 rounded-lg shadow-lg">
      <h1 className="text-2xl font-bold mb-6 text-center">
        JSON to PDF Converter
      </h1>
      <div className="mb-4">
        <label
          htmlFor="file-input"
          className="block text-sm font-medium text-gray-700"
        >
          File
        </label>
        <input
          id="file-input"
          type="file"
          accept=".json"
          onChange={handleFileChange}
          className="mt-1 w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
        />
      </div>
      {error && <p className="text-red-500 mb-4">{error}</p>}
      <button
        onClick={convertToPDF}
        disabled={!file || isLoading}
        className="w-full bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
      >
        {isLoading ? "Converting..." : "Convert to PDF"}
      </button>
    </div>
  );
}
export default JsonToPdf;
