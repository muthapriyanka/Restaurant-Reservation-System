import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginUser } from "./api/auth";

const LoginPage = () => {
  const [form, setForm] = useState({
    username: "",
    password: "",
    role: "CUSTOMER",
  });
  const [errors, setErrors] = useState({ username: "", password: "" });
  const [generalError, setGeneralError] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setErrors({ ...errors, [e.target.name]: "" });
    setGeneralError("");
  };

  const validateForm = () => {
    const newErrors = { username: "", password: "" };
    let valid = true;

    if (!form.username.trim()) {
      // !"" evaluates to true because "" is falsy.
      newErrors.username = "Email is required";
      valid = false;
    } else if (!/\S+@\S+\.\S+/.test(form.username)) {
      newErrors.username = "Enter a valid email";
      valid = false;
    }

    if (!form.password.trim()) {
      newErrors.password = "Password is required";
      valid = false;
    } else if (form.password.length < 8) {
      newErrors.password = "Password must be at least 8 characters";
      valid = false;
    }

    setErrors(newErrors);
    return valid;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) return;
    try {
      const res = await loginUser(new URLSearchParams(form)); //This sends a login request to the backend.
      if (res.access_token) {
        localStorage.setItem("accessToken", res.access_token);
        localStorage.setItem("role", form.role);
      }

      if (form.role === "CUSTOMER") {
        navigate("/custDashboard");
      } else if (form.role === "RESTAURANT_MANAGER") {
        navigate("/managerDashboard");
      } else if (form.role === "ADMIN") {
        navigate("/adminDashboard");
      } else {
        navigate("/welcome");
      }
    } catch (err) {
      setGeneralError("Invalid email or password");
    }
  };

  return (
    <div className="login-bg">
      <div className="login-overlay">
        <div className="auth-container glass-box">
          <h2>Login</h2>
          <form onSubmit={handleSubmit} noValidate>
            <input
              className="inputCreateRestaurant"
              name="username"
              type="email"
              placeholder="Email"
              value={form.username}
              onChange={handleChange}
            />
            {errors.username && <p className="error-text">{errors.username}</p>}

            <input
              className="inputCreateRestaurant"
              name="password"
              type="password"
              placeholder="Password"
              value={form.password}
              onChange={handleChange}
            />
            {errors.password && <p className="error-text">{errors.password}</p>}

            <select
              name="role"
              value={form.role}
              onChange={handleChange}
              className="inputCreateRestaurant"
            >
              <option value="CUSTOMER">Customer</option>
              <option value="RESTAURANT_MANAGER">Restaurant Manager</option>
              <option value="ADMIN">Admin</option>
            </select>

            <button type="submit">Login</button>
            {generalError && <p className="error-text">{generalError}</p>}
          </form>
          <p>
            Don't have an account? <a href="/register">Register here</a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
