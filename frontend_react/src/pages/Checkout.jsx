import React, { useEffect, useMemo, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../api/client";
import ProductCard from "../components/ProductCard";
import "./Checkout.css";

const APPLIED_COUPON_KEY = "vf_applied_coupon";

function money(value) {
  const number = Number(value || 0);
  return `₹${number.toFixed(2)}`;
}

function getProductImage(product) {
  return product?.image_url || product?.image || "";
}

function loadCashfreeSdk() {
  return new Promise((resolve, reject) => {
    if (window.Cashfree) {
      resolve(window.Cashfree);
      return;
    }

    const old = document.querySelector("script[data-cashfree-sdk]");
    if (old) {
      old.addEventListener("load", () => resolve(window.Cashfree));
      old.addEventListener("error", reject);
      return;
    }

    const script = document.createElement("script");
    script.src = "https://sdk.cashfree.com/js/v3/cashfree.js";
    script.async = true;
    script.dataset.cashfreeSdk = "true";
    script.onload = () => resolve(window.Cashfree);
    script.onerror = () => reject(new Error("Unable to load Cashfree SDK."));
    document.body.appendChild(script);
  });
}

function buildInvoiceHtml(order) {
  const rows = (order.items || [])
    .map((item) => {
      const total = Number(item.price || 0) * Number(item.quantity || 0);
      return `
        <tr>
          <td>${item.product_name || "Product"}</td>
          <td>${item.quantity}</td>
          <td>${money(item.price)}</td>
          <td>${money(total)}</td>
        </tr>`;
    })
    .join("");

  return `<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Invoice ${order.invoice_number || order.order_number}</title>
  <style>
    body{font-family:Arial,sans-serif;color:#111;margin:40px;}
    .top{display:flex;justify-content:space-between;align-items:flex-start;border-bottom:2px solid #00b207;padding-bottom:18px;margin-bottom:22px;}
    h1{color:#00b207;margin:0;} h2{margin:0 0 8px;} p{margin:4px 0;color:#444;}
    table{width:100%;border-collapse:collapse;margin-top:20px;} th,td{border:1px solid #ddd;padding:10px;text-align:left;} th{background:#f1fff1;}
    .total{text-align:right;margin-top:18px;font-size:20px;font-weight:700;} .badge{display:inline-block;background:#e9ffe9;color:#008806;padding:8px 12px;border-radius:20px;font-weight:700;}
  </style>
</head>
<body>
  <div class="top">
    <div><h1>VetriFresh</h1><p>Fresh products delivered to your door.</p></div>
    <div><h2>Invoice</h2><p>${order.invoice_number || ""}</p><span class="badge">${order.payment_status || "pending"}</span></div>
  </div>
  <p><b>Order:</b> ${order.order_number || order.id}</p>
  <p><b>Date:</b> ${new Date(order.created_at || Date.now()).toLocaleString()}</p>
  <p><b>Customer:</b> ${order.full_name || ""}</p>
  <p><b>Phone:</b> ${order.phone || ""}</p>
  <p><b>Email:</b> ${order.email || ""}</p>
  <p><b>Address:</b> ${order.address || ""}, ${order.city || ""}, ${order.state || ""} - ${order.pincode || ""}</p>
  <table><thead><tr><th>Product</th><th>Qty</th><th>Price</th><th>Total</th></tr></thead><tbody>${rows}</tbody></table>
  <div class="total">Grand Total: ${money(order.total_amount)}</div>
  <script>window.print()</script>
</body>
</html>`;
}

function downloadInvoice(order) {
  const html = buildInvoiceHtml(order);
  const blob = new Blob([html], { type: "text/html" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `${order.invoice_number || order.order_number || "invoice"}.html`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

export default function Checkout() {
  const navigate = useNavigate();

  const [cartItems, setCartItems] = useState([]);
  const [pageData, setPageData] = useState({ banner: null, related_products: [] });
  const [paymentMethods, setPaymentMethods] = useState([]);
  const [loading, setLoading] = useState(true);
  const [placingOrder, setPlacingOrder] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [successOrder, setSuccessOrder] = useState(null);
  const [appliedCoupon, setAppliedCoupon] = useState(null);
  const [couponWarning, setCouponWarning] = useState("");

  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    company_name: "",
    address: "",
    country: "India",
    state: "Tamil Nadu",
    city: "",
    pincode: "",
    email: "",
    phone: "",
    payment_method: "Cash on Delivery",
    order_note: "",
    different_address: false,
  });

  const updateForm = (name, value) => {
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const loadCart = async () => {
    const res = await api.get("/cart/");
    const data = Array.isArray(res.data) ? res.data : res.data.results || [];
    setCartItems(data);
    return data;
  };

  const loadCartPage = async () => {
    try {
      const res = await api.get("/cart-page/");
      setPageData({
        banner: res.data?.banner || null,
        related_products: res.data?.related_products || [],
      });
    } catch (err) {
      setPageData({ banner: null, related_products: [] });
    }
  };

  const loadCheckoutPage = async () => {
    try {
      const res = await api.get("/checkout-page/");
      const methods = res.data?.payment_methods || [];
      setPaymentMethods(methods);
      if (methods.length && !methods.some((m) => m.method_type === form.payment_method)) {
        updateForm("payment_method", methods[0].method_type);
      }
    } catch (err) {
      setPaymentMethods([
        { title: "Cash on Delivery", method_type: "Cash on Delivery" },
        { title: "Cashfree Online Payment", method_type: "Cashfree" },
      ]);
    }
  };

  const restoreAppliedCoupon = async (loadedItems) => {
    const saved = localStorage.getItem(APPLIED_COUPON_KEY);

    if (!saved || !loadedItems.length) {
      localStorage.removeItem(APPLIED_COUPON_KEY);
      setAppliedCoupon(null);
      return;
    }

    try {
      const parsed = JSON.parse(saved);
      const code = String(parsed?.code || "").trim();

      if (!code) {
        localStorage.removeItem(APPLIED_COUPON_KEY);
        setAppliedCoupon(null);
        return;
      }

      const res = await api.post("/coupon/apply/", { code });
      const freshCoupon = {
        ...res.data,
        code: res.data?.code || code,
      };

      setAppliedCoupon(freshCoupon);
      setCouponWarning("");
      localStorage.setItem(APPLIED_COUPON_KEY, JSON.stringify(freshCoupon));
    } catch (err) {
      localStorage.removeItem(APPLIED_COUPON_KEY);
      setAppliedCoupon(null);
      setCouponWarning(err.response?.data?.detail || "Saved coupon is no longer valid.");
    }
  };

  useEffect(() => {
    const loadAll = async () => {
      setLoading(true);
      setError("");

      try {
        const loadedItems = await loadCart();
        await Promise.all([loadCartPage(), loadCheckoutPage()]);
        await restoreAppliedCoupon(loadedItems);
      } catch (err) {
        navigate("/login");
      } finally {
        setLoading(false);
      }
    };

    loadAll();
  }, [navigate]);

  const subtotal = useMemo(() => {
    return cartItems.reduce((sum, item) => sum + Number(item.item_total || 0), 0);
  }, [cartItems]);

  const discountAmount = Number(appliedCoupon?.discount_amount || 0);
  const total = Math.max(subtotal - discountAmount, 0);
  const banner = pageData.banner;
  const relatedProducts = pageData.related_products || [];

  const buildPayload = () => {
    const fullName = `${form.first_name} ${form.last_name}`.trim();
    return {
      full_name: fullName,
      phone: form.phone,
      email: form.email,
      address: form.address,
      city: form.city || form.country || "Not specified",
      state: form.state,
      pincode: form.pincode,
      payment_method: form.payment_method,
      coupon_code: appliedCoupon?.code || "",
      order_note: form.order_note,
    };
  };

  const validatePayload = (payload) => {
    if (!payload.full_name || !payload.phone || !payload.address || !payload.city || !payload.pincode) {
      setError("Please fill first name, last name, address, city, pincode and phone number.");
      return false;
    }
    return true;
  };

  const placeCashfreeOrder = async (payload) => {
    const createRes = await api.post("/payments/cashfree/create/", payload);
    const paymentSessionId = createRes.data?.payment_session_id;
    const cashfreeOrderId = createRes.data?.cashfree_order_id;
    const mode = createRes.data?.cashfree_mode === "production" ? "production" : "sandbox";

    if (!paymentSessionId) {
      throw new Error("Cashfree payment session id not received.");
    }

    const Cashfree = await loadCashfreeSdk();
    const cashfree = Cashfree({ mode });

    await cashfree.checkout({
      paymentSessionId,
      redirectTarget: "_modal",
    });

    const verifyRes = await api.get(`/payments/cashfree/verify/${cashfreeOrderId}/`);
    const order = verifyRes.data?.order;

    if (order?.payment_status === "paid") {
      localStorage.removeItem(APPLIED_COUPON_KEY);
      setAppliedCoupon(null);
      setSuccessOrder(order);
      setMessage("Payment successful! Order placed successfully.");
      await loadCart();
      return;
    }

    setSuccessOrder(order || createRes.data?.order);
    setError("Payment was not completed. Please try again or choose Cash on Delivery.");
  };

  const placeOrder = async (event) => {
    event.preventDefault();
    setMessage("");
    setError("");

    if (cartItems.length === 0) {
      setError("Your cart is empty.");
      return;
    }

    const payload = buildPayload();
    if (!validatePayload(payload)) return;

    try {
      setPlacingOrder(true);

      if (form.payment_method === "Cashfree") {
        await placeCashfreeOrder(payload);
      } else {
        const res = await api.post("/orders/", payload);
        localStorage.removeItem(APPLIED_COUPON_KEY);
        setAppliedCoupon(null);
        setSuccessOrder(res.data);
        setMessage("Order placed successfully!");
        await loadCart();
      }
    } catch (err) {
      const data = err.response?.data;
      const detail = data?.detail || data?.non_field_errors?.[0] || err.message || "Unable to place order. Please check your details.";
      setError(detail);
    } finally {
      setPlacingOrder(false);
    }
  };

  return (
    <main className="vf-checkout2-page">
      <section
        className="vf-checkout2-hero"
        style={
          banner?.background_image_url
            ? {
                backgroundImage: `linear-gradient(90deg, rgba(0,0,0,.74), rgba(0,0,0,.22)), url(${banner.background_image_url})`,
              }
            : undefined
        }
      >
        <div className="vf-checkout2-container">
          <div className="vf-checkout2-breadcrumb">
            <Link to="/">⌂ Home</Link>
            <span>›</span>
            <Link to="/shop">Category</Link>
            <span>›</span>
            <Link to="/cart">Shopping cart</Link>
            <span>›</span>
            <span>Checkout</span>
          </div>
        </div>
      </section>

      <section className="vf-checkout2-main vf-checkout2-container">
        {loading ? (
          <div className="vf-checkout2-empty">Loading checkout...</div>
        ) : cartItems.length === 0 && !successOrder ? (
          <div className="vf-checkout2-empty">
            <h2>Your cart is empty.</h2>
            <p>Please add products before checkout.</p>
            <Link to="/shop">Continue Shopping</Link>
          </div>
        ) : (
          <form className="vf-checkout2-layout" onSubmit={placeOrder}>
            <div className="vf-checkout2-left">
              <h1>Billing Information</h1>

              <div className="vf-checkout2-grid three">
                <label>
                  <span>First name</span>
                  <input type="text" placeholder="Your first name" value={form.first_name} onChange={(e) => updateForm("first_name", e.target.value)} required />
                </label>
                <label>
                  <span>Last name</span>
                  <input type="text" placeholder="Your last name" value={form.last_name} onChange={(e) => updateForm("last_name", e.target.value)} required />
                </label>
                <label>
                  <span>Company Name <em>(optional)</em></span>
                  <input type="text" placeholder="Company name" value={form.company_name} onChange={(e) => updateForm("company_name", e.target.value)} />
                </label>
              </div>

              <label className="vf-checkout2-field">
                <span>Street Address</span>
                <input type="text" placeholder="Address" value={form.address} onChange={(e) => updateForm("address", e.target.value)} required />
              </label>

              <div className="vf-checkout2-grid three small-cols">
                <label>
                  <span>Country / Region</span>
                  <select value={form.country} onChange={(e) => updateForm("country", e.target.value)}>
                    <option value="India">India</option>
                    <option value="Tamil Nadu">Tamil Nadu</option>
                    <option value="Kerala">Kerala</option>
                    <option value="Karnataka">Karnataka</option>
                  </select>
                </label>
                <label>
                  <span>States</span>
                  <select value={form.state} onChange={(e) => updateForm("state", e.target.value)}>
                    <option value="Tamil Nadu">Tamil Nadu</option>
                    <option value="Kerala">Kerala</option>
                    <option value="Karnataka">Karnataka</option>
                    <option value="Andhra Pradesh">Andhra Pradesh</option>
                  </select>
                </label>
                <label>
                  <span>City / Pincode</span>
                  <div className="vf-checkout2-double">
                    <input type="text" placeholder="City" value={form.city} onChange={(e) => updateForm("city", e.target.value)} required />
                    <input type="text" placeholder="Pincode" value={form.pincode} onChange={(e) => updateForm("pincode", e.target.value)} required />
                  </div>
                </label>
              </div>

              <div className="vf-checkout2-grid two">
                <label>
                  <span>Email</span>
                  <input type="email" placeholder="Email Address" value={form.email} onChange={(e) => updateForm("email", e.target.value)} />
                </label>
                <label>
                  <span>Phone</span>
                  <input type="tel" placeholder="Phone number" value={form.phone} onChange={(e) => updateForm("phone", e.target.value)} required />
                </label>
              </div>

              <label className="vf-checkout2-checkbox">
                <input type="checkbox" checked={form.different_address} onChange={(e) => updateForm("different_address", e.target.checked)} />
                <span>Ship to a different address</span>
              </label>

              <div className="vf-checkout2-notes">
                <h2>Additional Info</h2>
                <label>
                  <span>Order Notes <em>(Optional)</em></span>
                  <textarea placeholder="Notes about your order, e.g. special notes for delivery" value={form.order_note} onChange={(e) => updateForm("order_note", e.target.value)} />
                </label>
              </div>

              {message && <p className="vf-checkout2-alert success">{message}</p>}
              {error && <p className="vf-checkout2-alert error">{error}</p>}
              {couponWarning && <p className="vf-checkout2-alert error">{couponWarning}</p>}
            </div>

            <aside className="vf-checkout2-summary">
              <h2>Order Summary</h2>
              <div className="vf-checkout2-summary-products">
                {cartItems.map((item) => {
                  const product = item.product || {};
                  return (
                    <div className="vf-checkout2-summary-item" key={item.id}>
                      <img src={getProductImage(product)} alt={product.name || "Product"} />
                      <div><p>{product.name || "Product"} <span>x{item.quantity}</span></p></div>
                      <b>{money(item.item_total)}</b>
                    </div>
                  );
                })}
              </div>

              <div className="vf-checkout2-total-line"><span>Subtotal:</span><b>{money(subtotal)}</b></div>
              {discountAmount > 0 && (
                <div className="vf-checkout2-total-line discount">
                  <span>Coupon ({appliedCoupon?.code}):</span>
                  <b>-{money(discountAmount)}</b>
                </div>
              )}
              <div className="vf-checkout2-total-line"><span>Shipping:</span><b>Free</b></div>
              <div className="vf-checkout2-total-line final"><span>Total:</span><b>{money(total)}</b></div>

              <div className="vf-checkout2-payment">
                <h3>Payment Method</h3>
                {(paymentMethods.length ? paymentMethods : [
                  { title: "Cash on Delivery", method_type: "Cash on Delivery" },
                  { title: "Cashfree Online Payment", method_type: "Cashfree" },
                ]).map((method) => (
                  <label key={method.method_type}>
                    <input type="radio" name="payment_method" value={method.method_type} checked={form.payment_method === method.method_type} onChange={(e) => updateForm("payment_method", e.target.value)} />
                    <span>{method.icon || ""} {method.title}</span>
                  </label>
                ))}
              </div>

              <button className="vf-checkout2-place" type="submit" disabled={placingOrder}>
                {placingOrder ? "Processing..." : form.payment_method === "Cashfree" ? "Pay with Cashfree" : "Place Order"}
              </button>
            </aside>
          </form>
        )}
      </section>

      {relatedProducts.length > 0 && (
        <section className="vf-checkout2-related vf-checkout2-container">
          <h2>Related Products</h2>
          <div className="vf-checkout2-related-grid">
            {relatedProducts.map((item) => <ProductCard key={item.id} product={item.product} />)}
          </div>
        </section>
      )}

      {successOrder && (
        <div className="vf-checkout2-success-backdrop">
          <div className="vf-checkout2-success-card">
            <button type="button" className="vf-checkout2-success-close" onClick={() => setSuccessOrder(null)}>×</button>
            <div className="vf-checkout2-success-check">✓</div>
            <h2>{successOrder.payment_status === "paid" ? "Payment Successful" : "Order Placed Successfully"}</h2>
            <p>We will knock your door steps shortly.</p>
            <p className="vf-checkout2-success-order">Order: <b>{successOrder.order_number}</b></p>
            <div className="vf-checkout2-success-actions">
              <button type="button" onClick={() => navigate(`/track-order/${successOrder.order_number}`)}>Track Order</button>
              <button type="button" onClick={() => navigate("/orders")}>My Orders</button>
              <button type="button" onClick={() => downloadInvoice(successOrder)}>Download Invoice</button>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}
