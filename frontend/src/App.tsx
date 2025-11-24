import { Route, BrowserRouter as Router, Routes } from "react-router-dom"; // Routing tools
import Home from "@/components/home";
import Login from "@/components/login";

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
