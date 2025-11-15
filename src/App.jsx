import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./components/home.jsx";
import Stats from "./components/Stats.jsx";
import Recommendations from "./components/Recommendations.jsx";
import Favourites from "./components/Favourites.jsx";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home/>} />
        <Route path="/stats" element={<Stats/>} />
        <Route path="/recommendations" element={<Recommendations/>} />
        <Route path="/favourites" element={<Favourites/>} />
      </Routes>
    </Router>
  );
}

export default App;
