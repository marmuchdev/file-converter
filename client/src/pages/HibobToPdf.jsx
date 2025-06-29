import { useState } from 'react';

function HibobToPdf() {
  const [file, setFile] = useState(null);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'application/json') {
      setFile(selectedFile);
      setError('');
    } else {
      setFile(null);
      setError('Please upload a valid JSON file');
    }
  };

  const handleConvert = async () => {
    if (!file) {
      setError('Please select a file');
      return;
    }

    setIsLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/api/convert/hibob-to-pdf', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Conversion failed');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'hibob_reviews.zip';
      a.click();
      window.URL.revokeObjectURL(url);
      setError('');
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-6 max-w-2xl">
      <h1 className="text-3xl font-bold text-gray-800 mb-4">HiBob JSON to PDF Converter</h1>
      <p className="text-gray-600 mb-6">Upload a HiBob JSON performance review file to convert it into a ZIP of PDFs, one for each reviewer.</p>
      <div className="mb-6">
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
      {error && <p className="text-red-500 mb-4 font-medium">{error}</p>}
      <button
        onClick={handleConvert}
        disabled={!file || isLoading}
        className="bg-blue-600 text-white py-2 px-6 rounded-lg font-semibold disabled:bg-gray-400 hover:bg-blue-700 transition-colors duration-200"
      >
        {isLoading ? 'Converting...' : 'Convert to PDF'}
      </button>
    </div>
  );
}

export default HibobToPdf;