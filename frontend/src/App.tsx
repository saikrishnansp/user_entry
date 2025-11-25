import { Route, BrowserRouter as Router, Routes } from "react-router-dom"; // Routing tools
import Home from "@/pages/home";
import Login from "@/pages/login";

const App = () => {
  return (
    <>
      <Router>
        <Routes>
          <Route path='/' element={<Login />} /> {/* Default route */}
          <Route path='/home' element={<Home />} /> {/* Home route */}
        </Routes>
      </Router>
    </>
  );
};

export default App;
