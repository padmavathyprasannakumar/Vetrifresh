import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../api/client";
import "./Auth.css";

function Login() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    username: "",
    password: "",
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
      setError("Please enter username and password.");
      return;
    }

    try {
      setLoading(true);

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
      setError("Invalid username or password.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="vf-auth-page">
      <section className="vf-auth-card">
        <div className="vf-auth-logo">🌱</div>

        <h1>Welcome Back</h1>
        <p className="vf-auth-subtitle">
          Login to continue shopping fresh products.
        </p>

        {error && <div className="vf-auth-error">{error}</div>}

        <form className="vf-auth-form" onSubmit={handleSubmit}>
          <div className="vf-auth-group">
            <label>Username</label>
            <input
              type="text"
              name="username"
              placeholder="Enter your username"
              value={form.username}
              onChange={handleChange}
            />
          </div>

          <div className="vf-auth-group">
            <label>Password</label>
            <input
              type="password"
              name="password"
              placeholder="Enter your password"
              value={form.password}
              onChange={handleChange}
            />
          </div>

          <button type="submit" className="vf-auth-button" disabled={loading}>
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>

        <p className="vf-auth-bottom-text">
          New user? <Link to="/register">Create account</Link>
        </p>
      </section>
    </main>
  );
}

export default Login;
