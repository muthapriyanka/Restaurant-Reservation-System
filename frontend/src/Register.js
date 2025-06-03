import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { registerUser } from "./api/auth";
import "./AuthForm.css";

const RegisterPage = () => {
  const [form, setForm] = useState({
    email: "",
    password: "",
    phone_number: "",
    first_name: "",
    last_name: "",
    role: "customer",
  });

  const [errors, setErrors] = useState({});
  const [generalError, setGeneralError] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setErrors({ ...errors, [e.target.name]: "" });
    setGeneralError("");
  };

  const validateForm = () => {
    const newErrors = {};
    let valid = true;

    if (!form.first_name.trim()) {
      newErrors.first_name = "First name is required";
      valid = false;
    }

    if (!form.last_name.trim()) {
      newErrors.last_name = "Last name is required";
      valid = false;
    }

    if (!form.phone_number.trim()) {
      newErrors.phone_number = "Phone number is required";
      valid = false;
    } else if (!/^\d{10}$/.test(form.phone_number)) {
      newErrors.phone_number = "Phone number must be 10 digits";
      valid = false;
    }

    if (!form.email.trim()) {
      newErrors.email = "Email is required";
      valid = false;
    } else if (!/\S+@\S+\.\S+/.test(form.email)) {
      newErrors.email = "Enter a valid email";
      valid = false;
    }

    if (!form.password) {
      newErrors.password = "Password is required";
      valid = false;
    } else if (form.password.length < 9) {
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
      await registerUser(form);
      navigate("/login");
    } catch (err) {
      setGeneralError("Email already registered or something went wrong");
    }
  };

  return (
    <div className="register-bg">
      <div className="register-overlay">
        <div className="auth-container glass-box">
          <h2>Register</h2>
          <form onSubmit={handleSubmit} noValidate>
            <input
              name="first_name"
              placeholder="First Name"
              value={form.first_name}
              onChange={handleChange}
              className="inputCreateRestaurant"
            />
            {errors.first_name && (
              <p className="error-text">{errors.first_name}</p>
            )}

            <input
              name="last_name"
              placeholder="Last Name"
              value={form.last_name}
              onChange={handleChange}
              className="inputCreateRestaurant"
            />
            {errors.last_name && (
              <p className="error-text">{errors.last_name}</p>
            )}

            <input
              name="phone_number"
              placeholder="Phone Number"
              value={form.phone_number}
              onChange={handleChange}
              className="inputCreateRestaurant"
            />
            {errors.phone_number && (
              <p className="error-text">{errors.phone_number}</p>
            )}

            <input
              name="email"
              type="email"
              placeholder="Email"
              value={form.email}
              onChange={handleChange}
              className="inputCreateRestaurant"
            />
            {errors.email && <p className="error-text">{errors.email}</p>}

            <input
              name="password"
              type="password"
              placeholder="Password"
              value={form.password}
              onChange={handleChange}
              className="inputCreateRestaurant"
            />
            {errors.password && <p className="error-text">{errors.password}</p>}

            <select
              name="role"
              value={form.role}
              onChange={handleChange}
              className="inputCreateRestaurant"
            >
              <option value="customer">Customer</option>
              <option value="restaurant_manager">Restaurant Manager</option>
              <option value="admin">Admin</option>
            </select>

            <button type="submit">Register</button>
            {generalError && <p className="error-text">{generalError}</p>}
          </form>
          <p>
            Already have an account? <a href="/login">Login here</a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;
