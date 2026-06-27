import React, { useEffect, useMemo, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../api/client";
import "./MyOrders.css";

function money(value) {
  const number = Number(value || 0);
  return `₹${number.toFixed(2)}`;
}

function formatDate(value) {
  if (!value) return "";

  try {
    return new Date(value).toLocaleString("en-IN", {
      day: "2-digit",
      month: "short",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  } catch {
    return value;
  }
}

function normalizeOrders(data) {
  if (Array.isArray(data)) return data;
  if (Array.isArray(data?.results)) return data.results;
  if (Array.isArray(data?.orders)) return data.orders;
  return [];
}

function statusLabel(value) {
  return String(value || "pending")
    .replaceAll("_", " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

export default function MyOrders() {
  const navigate = useNavigate();
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const token = useMemo(() => localStorage.getItem("access_token"), []);

  useEffect(() => {
    if (!token) {
      setLoading(false);
      return;
    }

    const loadOrders = async () => {
      try {
        setLoading(true);
        setError("");
        const res = await api.get("/orders/");
        setOrders(normalizeOrders(res.data));
      } catch (err) {
        if (err?.response?.status === 401) {
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
          localStorage.removeItem("user");
          window.dispatchEvent(new Event("authChanged"));
          navigate("/login");
          return;
        }

        setError("Unable to load your orders. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    loadOrders();
  }, [navigate, token]);

  if (!token) {
    return (
      <main className="vf-orders-page">
        <section className="vf-orders-hero">
          <h1>My Orders</h1>
          <p>Login to see the products you have purchased.</p>
        </section>

        <section className="vf-orders-empty">
          <h2>Please login first</h2>
          <p>Your order history is available only after login.</p>
          <Link to="/login">Login</Link>
        </section>
      </main>
    );
  }

  return (
    <main className="vf-orders-page">
      <section className="vf-orders-hero">
        <h1>My Orders</h1>
        <p>All products purchased from your logged-in account will appear here.</p>
      </section>

      <section className="vf-orders-wrap">
        {loading ? (
          <div className="vf-orders-empty">
            <h2>Loading your orders...</h2>
          </div>
        ) : error ? (
          <div className="vf-orders-empty vf-orders-error">
            <h2>{error}</h2>
            <button type="button" onClick={() => window.location.reload()}>
              Reload
            </button>
          </div>
        ) : orders.length === 0 ? (
          <div className="vf-orders-empty">
            <h2>No orders yet</h2>
            <p>After you buy products, your order details will show on this page.</p>
            <Link to="/shop">Shop Now</Link>
          </div>
        ) : (
          <div className="vf-orders-list">
            {orders.map((order) => (
              <article className="vf-order-card" key={order.id || order.order_number}>
                <div className="vf-order-card-head">
                  <div>
                    <h2>{order.order_number || `Order #${order.id}`}</h2>
                    <p>Placed on {formatDate(order.created_at)}</p>
                  </div>

                  <div className="vf-order-status-wrap">
                    <span className="vf-order-status">{statusLabel(order.status)}</span>
                    <strong>{money(order.total_amount)}</strong>
                  </div>
                </div>

                <div className="vf-order-meta">
                  <span>Payment: <b>{order.payment_method}</b></span>
                  <span>Payment Status: <b>{statusLabel(order.payment_status)}</b></span>
                  {Number(order.discount_amount || 0) > 0 && (
                    <span>Discount: <b>{money(order.discount_amount)}</b></span>
                  )}
                </div>

                <div className="vf-order-products">
                  {(order.items || []).map((item) => (
                    <div className="vf-order-product" key={item.id}>
                      <div className="vf-order-product-img">
                        {item.product_image ? (
                          <img src={item.product_image} alt={item.product_name || "Product"} />
                        ) : (
                          <span>🌿</span>
                        )}
                      </div>

                      <div className="vf-order-product-info">
                        <h3>{item.product_name || "Product"}</h3>
                        <p>Qty: {item.quantity} × {money(item.price)}</p>
                      </div>

                      <strong>{money(item.item_total || Number(item.price || 0) * Number(item.quantity || 0))}</strong>
                    </div>
                  ))}
                </div>

                <div className="vf-order-address">
                  <h3>Delivery Address</h3>
                  <p>
                    {order.full_name}, {order.phone}<br />
                    {order.address}, {order.city}, {order.state} - {order.pincode}
                  </p>
                </div>

                <div className="vf-order-actions">
                  <Link to={`/track-order/${order.order_number || order.id}`}>Track Order</Link>
                </div>
              </article>
            ))}
          </div>
        )}
      </section>
    </main>
  );
}
