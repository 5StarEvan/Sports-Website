import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./components/home.jsx";
import Stats from "./components/Stats.jsx";
import TrendingNow from "./components/TrendingNow.jsx";
import Recommendations from "./components/Recommendations.jsx";
import Favourites from "./components/Favourites.jsx";
import Login from "./components/Login.jsx";
import SignUp from "./components/SignUp.jsx";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home/>} />
        <Route path="/stats" element={<Stats/>} />
        <Route path="/trending" element={<TrendingNow/>} />
        <Route path="/recommendations" element={<Recommendations/>} />
        <Route path="/favourites" element={<Favourites/>} />
        <Route path="/login" element={<Login/>} />
        <Route path="/create-account" element={<SignUp/>} />
      </Routes>
    </Router>
  );
}

export default App;
