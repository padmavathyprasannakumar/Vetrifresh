import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../api/client";
import "./Auth.css";

function Register() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    username: "",
    email: "",
    phone: "",
    address: "",
    password: "",
    confirmPassword: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!form.username.trim() || !form.password.trim()) {
      setError("Username and password are required.");
      return;
    }

    if (form.password.length < 6) {
      setError("Password must be at least 6 characters.");
      return;
    }

    if (form.password !== form.confirmPassword) {
      setError("Password and confirm password do not match.");
      return;
    }

    try {
      setLoading(true);

      await api.post("/auth/register/", {
        username: form.username,
        email: form.email,
        phone: form.phone,
        address: form.address,
        password: form.password,
      });

      const tokenRes = await api.post("/auth/token/", {
        username: form.username,
        password: form.password,
      });

      localStorage.setItem("access_token", tokenRes.data.access);
      localStorage.setItem("refresh_token", tokenRes.data.refresh);

      const userRes = await api.get("/auth/me/");
      localStorage.setItem("user", JSON.stringify(userRes.data));

      window.dispatchEvent(new Event("authChanged"));
      navigate("/");
    } catch (err) {
      const data = err?.response?.data;

      if (data?.username) {
        setError("This username already exists.");
      } else if (data?.email) {
        setError("Please enter a valid email address.");
      } else {
        setError("Registration failed. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="vf-auth-page">
      <section className="vf-auth-card vf-auth-card-large">
        <div className="vf-auth-logo">🌱</div>

        <h1>Create Account</h1>
        <p className="vf-auth-subtitle">
          Join VetriFresh and order fresh products easily.
        </p>

        {error && <div className="vf-auth-error">{error}</div>}

        <form className="vf-auth-form" onSubmit={handleSubmit}>
          <div className="vf-auth-row">
            <div className="vf-auth-group">
              <label>Username</label>
              <input
                type="text"
                name="username"
                placeholder="Enter username"
                value={form.username}
                onChange={handleChange}
              />
            </div>

            <div className="vf-auth-group">
              <label>Email</label>
              <input
                type="email"
                name="email"
                placeholder="Enter email"
                value={form.email}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className="vf-auth-group">
            <label>Phone</label>
            <input
              type="text"
              name="phone"
              placeholder="Enter phone number"
              value={form.phone}
              onChange={handleChange}
            />
          </div>

          <div className="vf-auth-group">
            <label>Address</label>
            <textarea
              name="address"
              placeholder="Enter address"
              value={form.address}
              onChange={handleChange}
              rows="3"
            />
          </div>

          <div className="vf-auth-row">
            <div className="vf-auth-group">
              <label>Password</label>
              <input
                type="password"
                name="password"
                placeholder="Enter password"
                value={form.password}
                onChange={handleChange}
              />
            </div>

            <div className="vf-auth-group">
              <label>Confirm Password</label>
              <input
                type="password"
                name="confirmPassword"
                placeholder="Confirm password"
                value={form.confirmPassword}
                onChange={handleChange}
              />
            </div>
          </div>

          <button type="submit" className="vf-auth-button" disabled={loading}>
            {loading ? "Creating account..." : "Create Account"}
          </button>
        </form>

        <p className="vf-auth-bottom-text">
          Already have an account? <Link to="/login">Login</Link>
        </p>
      </section>
    </main>
  );
}

export default Register;
