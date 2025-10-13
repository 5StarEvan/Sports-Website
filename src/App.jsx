import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./components/home.jsx";
import Stats from "./components/Stats.jsx";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home/>} />
        <Route path="/stats" element={<Stats/>} />
      </Routes>
    </Router>
  );
}

export default App;
