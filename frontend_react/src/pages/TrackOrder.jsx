import React, { useEffect, useMemo, useState } from "react";
import { Link, useNavigate, useParams, useSearchParams } from "react-router-dom";
import api from "../api/client";
import "./TrackOrder.css";

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

function getStepIndex(status) {
  const current = String(status || "pending").toLowerCase();

  if (["pending", "confirmed"].includes(current)) return 0;
  if (["packed", "shipped"].includes(current)) return 1;
  if (current === "out_for_delivery") return 2;
  if (current === "delivered") return 3;
  return 0;
}

function buildUpdates(order) {
  const status = String(order?.status || "pending").toLowerCase();
  const created = formatDate(order?.created_at);
  const updates = [
    {
      title: "Placed",
      text: "Order placed successfully",
      date: created,
      active: true,
    },
  ];

  if (["packed", "shipped", "out_for_delivery", "delivered"].includes(status)) {
    updates.push({
      title: "Packed",
      text: "Your items are packed and ready",
      date: created,
      active: true,
    });
  }

  if (["out_for_delivery", "delivered"].includes(status)) {
    updates.push({
      title: "Out for Delivery",
      text: "Delivery partner picked up your order",
      date: created,
      active: true,
    });
  }

  if (status === "delivered") {
    updates.push({
      title: "Delivered",
      text: "Order delivered successfully",
      date: formatDate(order?.delivered_at) || created,
      active: true,
    });
  }

  if (status === "cancelled") {
    updates.push({
      title: "Cancelled",
      text: "Order was cancelled",
      date: created,
      active: true,
    });
  }

  return updates;
}

function buildInvoiceHtml(order) {
  const rows = (order.items || [])
    .map((item) => {
      const itemTotal = Number(item.price || 0) * Number(item.quantity || 0);
      return `
        <tr>
          <td>${item.product_name || "Product"}</td>
          <td>${item.quantity}</td>
          <td>${money(item.price)}</td>
          <td>${money(itemTotal)}</td>
        </tr>`;
    })
    .join("");

  return `<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Invoice ${order.invoice_number || order.order_number}</title>
  <style>
    body{font-family:Arial,sans-serif;margin:40px;color:#111;background:#fff}
    .top{display:flex;justify-content:space-between;gap:30px;border-bottom:3px solid #00b207;padding-bottom:18px;margin-bottom:22px}
    h1{color:#007a05;margin:0;font-size:32px}.muted{color:#666;margin:5px 0}.box{margin:18px 0;padding:15px;border:1px solid #ddd;border-radius:10px}
    table{width:100%;border-collapse:collapse;margin-top:20px}th,td{border:1px solid #ddd;padding:10px;text-align:left}th{background:#f1fff1}.total{text-align:right;font-size:20px;font-weight:700;margin-top:18px;color:#003b05}
  </style>
</head>
<body>
  <div class="top">
    <div><h1>VetriFresh</h1><p class="muted">Fresh products delivered to your door.</p></div>
    <div><h2>Invoice</h2><p>${order.invoice_number || ""}</p></div>
  </div>
  <div class="box">
    <p><b>Order Number:</b> ${order.order_number || order.id}</p>
    <p><b>Customer:</b> ${order.full_name || ""}</p>
    <p><b>Phone:</b> ${order.phone || ""}</p>
    <p><b>Email:</b> ${order.email || ""}</p>
    <p><b>Address:</b> ${order.address || ""}, ${order.city || ""}, ${order.state || ""} - ${order.pincode || ""}</p>
    <p><b>Payment:</b> ${order.payment_method || ""} / ${order.payment_status || ""}</p>
  </div>
  <table>
    <thead><tr><th>Product</th><th>Qty</th><th>Price</th><th>Total</th></tr></thead>
    <tbody>${rows}</tbody>
  </table>
  <div class="total">Grand Total: ${money(order.total_amount)}</div>
  <script>window.print()</script>
</body>
</html>`;
}

function downloadInvoice(order) {
  const blob = new Blob([buildInvoiceHtml(order)], { type: "text/html" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = `${order.invoice_number || order.order_number || "invoice"}.html`;
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(url);
}

const steps = [
  { key: "placed", label: "Placed" },
  { key: "packed", label: "Packed" },
  { key: "out_for_delivery", label: "Out for Delivery" },
  { key: "delivered", label: "Delivered" },
];

export default function TrackOrder() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const [trackingCode, setTrackingCode] = useState(id || "");
  const [phone, setPhone] = useState("");
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const currentIndex = useMemo(() => getStepIndex(order?.status), [order?.status]);
  const updates = useMemo(() => buildUpdates(order), [order]);

  const loadOrder = async (identifier, phoneNumber = "") => {
    const code = String(identifier || "").trim();

    if (!code) {
      setError("Please enter your order tracking code.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const cashfreeOrderId = searchParams.get("cashfree_order_id");

      if (cashfreeOrderId) {
        await api.get(`/payments/cashfree/verify/${cashfreeOrderId}/`);
      }

      const params = phoneNumber ? { phone: phoneNumber } : {};
      const res = await api.get(`/track-order/${code}/`, { params });
      const loadedOrder = res.data?.order || null;
      setOrder(loadedOrder);

      if (!id && loadedOrder?.order_number) {
        navigate(`/track-order/${loadedOrder.order_number}`, { replace: true });
      }
    } catch (err) {
      setOrder(null);
      setError(err.response?.data?.detail || "Order not found. Please check your tracking code and phone number.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (id) {
      setTrackingCode(id);
      loadOrder(id);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  const handleSubmit = (event) => {
    event.preventDefault();
    loadOrder(trackingCode, phone);
  };

  return (
    <main className="vf-track-page2">
      <section className="vf-track-hero2">
        <h1>Order Tracking</h1>
      </section>

      <section className="vf-track-layout2">
        <aside className="vf-track-search-card2">
          <h2>Track your grocery order</h2>
          <form onSubmit={handleSubmit}>
            <label>
              Tracking Code
              <input
                type="text"
                value={trackingCode}
                onChange={(e) => setTrackingCode(e.target.value)}
                placeholder="Enter order number"
              />
            </label>

            <label>
              Phone
              <input
                type="text"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="Enter phone number"
              />
            </label>

            <button type="submit" disabled={loading}>
              {loading ? "Tracking..." : "Track Order"}
            </button>
          </form>
        </aside>

        <section className="vf-track-result-card2">
          {loading ? (
            <div className="vf-track-empty2">Loading order details...</div>
          ) : error ? (
            <div className="vf-track-error2">
              <h2>{error}</h2>
              <p>Use the order number generated after checkout.</p>
              <Link to="/shop">Continue Shopping</Link>
            </div>
          ) : order ? (
            <>
              <div className="vf-track-order-head2">
                <div>
                  <h2>{order.order_number}</h2>
                  <p>
                    Total: <strong>{money(order.total_amount)}</strong>
                    <span>|</span>
                    Delivery Slot: {formatDate(order.created_at)}
                  </p>
                </div>
                <button type="button" onClick={() => downloadInvoice(order)}>
                  Download Invoice
                </button>
              </div>

              <div className="vf-track-progress2">
                {steps.map((step, index) => (
                  <div
                    key={step.key}
                    className={`vf-track-step2 ${index <= currentIndex ? "active" : ""}`}
                  >
                    <span>{index + 1}</span>
                    <p>{step.label}</p>
                  </div>
                ))}
              </div>

              <div className="vf-track-updates2">
                <h3>Tracking Updates</h3>
                {updates.map((update) => (
                  <div className="vf-track-update-row2" key={`${update.title}-${update.date}`}>
                    <strong>{update.title}</strong>
                    <span>- {update.text}</span>
                    <small>{update.date}</small>
                  </div>
                ))}
              </div>

              <div className="vf-track-details2">
                <div>
                  <h3>Delivery Address</h3>
                  <p>{order.full_name}</p>
                  <p>{order.phone}</p>
                  <p>{order.address}, {order.city}, {order.state} - {order.pincode}</p>
                </div>

                <div>
                  <h3>Payment Details</h3>
                  <p>Method: {order.payment_method}</p>
                  <p>Status: <strong>{order.payment_status}</strong></p>
                  <p>Invoice: {order.invoice_number}</p>
                </div>
              </div>

              <div className="vf-track-items2">
                <h3>Order Items</h3>
                {(order.items || []).map((item) => (
                  <div className="vf-track-item2" key={item.id}>
                    <span>{item.product_name}</span>
                    <small>x{item.quantity}</small>
                    <strong>{money(Number(item.price || 0) * Number(item.quantity || 0))}</strong>
                  </div>
                ))}
              </div>
            </>
          ) : (
            <div className="vf-track-empty2">
              <h2>Enter your tracking code</h2>
              <p>Your order number is generated automatically after checkout.</p>
            </div>
          )}
        </section>
      </section>
    </main>
  );
}
