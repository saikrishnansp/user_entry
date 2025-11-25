import { api } from "@/api/api.ts";
import { validatePassword } from "@/utils/validation";
import React, { useState } from "react"; // Import React and useState hook
import { useNavigate } from "react-router-dom"; // For programmatic navigation

const Login = () => {
  const [username, setUsername] = useState(""); // State to store username input
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState(""); // State to store password input
  const navigate = useNavigate(); // Hook to navigate to other routes

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    
    const errors = validatePassword(password);
    if (errors.length > 0) {
      alert(errors.join("\n")); // ✅ show all missing rules clearly
      return;
    }

    try {
      // POST request to FastAPI backend
      const response = await api.post("/users/", {
        username,
        email,
        password,
      });
      // If login succeeds, navigate to home
      if (response.status === 200) {
        console.log("User created:", response.data);
        alert("Login successful!");
        navigate("/home"); // Redirect to home page
      }
      alert("User registered successfully!");
    } catch (error: unknown) {
      // the error should be any, but any will cause error, so trust me and let it be unknown!!!
      if (error.response) {
        console.error("Backend error:", error.response.data);
        alert(
          `Failed to register user: ${JSON.stringify(error.response.data)}`
        );
      } else {
        console.error("Unexpected error:", error);
        alert("Unexpected error occurred");
      }
      console.error("Error: ", error);
      alert("Failed to register user");
    }
  };

  return (
    <form onSubmit={handleRegister}>
      <h2>Register</h2>
      <input
        type='text'
        placeholder='Username'
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <br />
      <input
        type='email'
        placeholder='Email'
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <br />
      <input
        type='password'
        placeholder='Password'
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <br />
      <button type='submit'>Register</button>
    </form>
  );
};

export default Login;
