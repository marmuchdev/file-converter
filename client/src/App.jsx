import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Home from "./pages/Home";
import Converters from "./pages/Converters";
import JsonToPdf from "./pages/JsonToPdf";
import "./index.css";

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <nav className="bg-blue-600 p-4 shadow-md">
          <div className="container mx-auto flex justify-between items-center">
            <Link to="/" className="text-white text-xl font-bold">
              Converter App
            </Link>
            <ul className="flex space-x-4">
              <li>
                <Link to="/" className="text-white hover:text-blue-200">
                  Home
                </Link>
              </li>
              <li>
                <Link
                  to="/converters"
                  className="text-white hover:text-blue-200"
                >
                  Converters
                </Link>
              </li>
            </ul>
          </div>
        </nav>
        <div className="container mx-auto p-4">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/converters" element={<Converters />} />
            <Route path="/converters/json-to-pdf" element={<JsonToPdf />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
