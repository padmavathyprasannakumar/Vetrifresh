import React, { useEffect, useMemo, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../api/client";
import ProductCard from "../components/ProductCard";
import { apiErrorMessage, isOutOfStock, stockMessage } from "../utils/stock";
import "./Cart.css";

const APPLIED_COUPON_KEY = "vf_applied_coupon";

function money(value) {
  const number = Number(value || 0);
  return `₹${number.toFixed(2)}`;
}

function couponLabel(coupon) {
  if (coupon?.display_text) return coupon.display_text;

  const value = Number(coupon?.discount_value || 0);
  if (coupon?.discount_type === "fixed") return `₹${value.toFixed(0)} OFF`;
  return `${value.toFixed(0)}% OFF`;
}

function couponTerms(coupon) {
  const parts = [];

  if (Number(coupon?.minimum_order_amount || 0) > 0) {
    parts.push(`Min order ${money(coupon.minimum_order_amount)}`);
  }

  if (Number(coupon?.maximum_discount_amount || 0) > 0) {
    parts.push(`Max discount ${money(coupon.maximum_discount_amount)}`);
  }

  return parts.join(" • ") || "No minimum order";
}

function Cart() {
  const navigate = useNavigate();

  const [items, setItems] = useState([]);
  const [pageData, setPageData] = useState({
    banner: null,
    related_products: [],
    active_coupons: [],
  });
  const [loading, setLoading] = useState(true);
  const [couponCode, setCouponCode] = useState("");
  const [couponInfo, setCouponInfo] = useState(null);
  const [couponMessage, setCouponMessage] = useState("");
  const [couponError, setCouponError] = useState("");
  const [applyingCoupon, setApplyingCoupon] = useState(false);

  const clearAppliedCoupon = () => {
    localStorage.removeItem(APPLIED_COUPON_KEY);
    setCouponInfo(null);
    setCouponMessage("");
    setCouponError("");
  };

  const loadCart = async () => {
    try {
      const res = await api.get("/cart/");
      const data = Array.isArray(res.data) ? res.data : res.data.results || [];
      setItems(data);
      return data;
    } catch (err) {
      navigate("/login");
      return [];
    }
  };

  const loadCartPage = async () => {
    try {
      const res = await api.get("/cart-page/");
      setPageData({
        banner: res.data?.banner || null,
        related_products: res.data?.related_products || [],
        active_coupons: res.data?.active_coupons || [],
      });
    } catch (err) {
      setPageData({
        banner: null,
        related_products: [],
        active_coupons: [],
      });
    }
  };

  useEffect(() => {
    const loadAll = async () => {
      setLoading(true);
      await Promise.all([loadCart(), loadCartPage()]);
      setLoading(false);
    };

    loadAll();
  }, []);

  const subtotal = useMemo(() => {
    return items.reduce((sum, item) => sum + Number(item.item_total || 0), 0);
  }, [items]);

  const discountAmount = Number(couponInfo?.discount_amount || 0);
  const total = Math.max(subtotal - discountAmount, 0);

  const resetCouponAfterCartChange = () => {
    clearAppliedCoupon();
    setCouponCode("");
  };

  const updateQty = async (item, qty) => {
    if (qty < 1) return;

    if (isOutOfStock(item.product, qty)) {
      alert(stockMessage(item.product, qty));
      return;
    }

    try {
      await api.patch(`/cart/${item.id}/`, { quantity: qty });
      resetCouponAfterCartChange();
      await loadCart();
      window.dispatchEvent(new Event("cartChanged"));
    } catch (err) {
      alert(apiErrorMessage(err, "Unable to update cart."));
    }
  };

  const removeItem = async (id) => {
    try {
      await api.delete(`/cart/${id}/`);
      resetCouponAfterCartChange();
      await loadCart();
      window.dispatchEvent(new Event("cartChanged"));
    } catch (err) {
      alert("Unable to remove item.");
    }
  };

  const applyCoupon = async (event, selectedCode) => {
    event?.preventDefault?.();
    setCouponMessage("");
    setCouponError("");

    const cleanCode = String(selectedCode || couponCode || "").trim();

    if (!cleanCode) {
      setCouponError("Please enter coupon code.");
      return;
    }

    try {
      setApplyingCoupon(true);
      const res = await api.post("/coupon/apply/", { code: cleanCode });
      const appliedData = {
        ...res.data,
        code: res.data?.code || cleanCode,
      };

      setCouponInfo(appliedData);
      setCouponCode(appliedData.code);
      setCouponMessage(res.data?.message || "Coupon applied successfully.");
      localStorage.setItem(
        APPLIED_COUPON_KEY,
        JSON.stringify({
          code: appliedData.code,
          discount_amount: appliedData.discount_amount,
          subtotal: appliedData.subtotal,
          total: appliedData.total,
        })
      );
    } catch (err) {
      clearAppliedCoupon();
      setCouponCode(cleanCode);
      setCouponError(err.response?.data?.detail || "Invalid coupon code.");
    } finally {
      setApplyingCoupon(false);
    }
  };

  const banner = pageData.banner;
  const relatedProducts = pageData.related_products || [];
  const availableCoupons = pageData.active_coupons || [];

  return (
    <main className="vf2-cart-page">
      <section
        className="vf2-cart-hero"
        style={
          banner?.background_image_url
            ? {
                backgroundImage: `linear-gradient(90deg, rgba(0,0,0,.72), rgba(0,0,0,.24)), url(${banner.background_image_url})`,
              }
            : undefined
        }
      >
        <div className="vf2-cart-container">
          <div className="vf2-cart-breadcrumb">
            <Link to="/">⌂ Home</Link>
            <span>›</span>
            <Link to="/shop">Category</Link>
            <span>›</span>
            <span>{banner?.breadcrumb_text || "Shopping cart"}</span>
          </div>
        </div>
      </section>

      <section className="vf2-cart-main vf2-cart-container">
        <h1>{banner?.title || "My Shopping Cart"}</h1>

        {loading ? (
          <div className="vf2-cart-empty">Loading cart...</div>
        ) : items.length === 0 ? (
          <div className="vf2-cart-empty">
            <h2>Your cart is empty.</h2>
            <p>Add fresh products to your cart and come back here.</p>
            <Link to="/shop">Continue Shopping</Link>
          </div>
        ) : (
          <div className="vf2-cart-layout">
            <div className="vf2-cart-left">
              <div className="vf2-cart-card">
                <div className="vf2-cart-scroll">
                  <div className="vf2-cart-grid vf2-cart-grid-head">
                    <div>Product</div>
                    <div>Price</div>
                    <div>Quantity</div>
                    <div>Subtotal</div>
                    <div></div>
                  </div>

                  {items.map((item) => {
                    const product = item.product || {};
                    const productName = product.name || "Product";
                    const productImage = product.image_url || "";
                    const productPrice = product.price || 0;
                    const nextQtyOutOfStock = isOutOfStock(product, item.quantity + 1);

                    return (
                      <div className="vf2-cart-grid vf2-cart-grid-row" key={item.id}>
                        <div className="vf2-cart-product-cell">
                          <div className="vf2-cart-image-box">
                            {productImage ? (
                              <img src={productImage} alt={productName} />
                            ) : (
                              <span>No Image</span>
                            )}
                          </div>
                          <div className="vf2-cart-product-name">{productName}</div>
                        </div>

                        <div className="vf2-cart-price-cell">
                          {money(productPrice)}/kg
                        </div>

                        <div className="vf2-cart-qty-cell">
                          <button
                            type="button"
                            onClick={() => updateQty(item, item.quantity - 1)}
                            disabled={item.quantity <= 1}
                          >
                            −
                          </button>
                          <span>{item.quantity}</span>
                          <button
                            type="button"
                            onClick={() => updateQty(item, item.quantity + 1)}
                            disabled={nextQtyOutOfStock}
                          >
                            +
                          </button>
                        </div>

                        <div className="vf2-cart-subtotal-cell">
                          {money(item.item_total)}
                        </div>

                        <button
                          type="button"
                          className="vf2-cart-remove-btn"
                          onClick={() => removeItem(item.id)}
                          title="Remove"
                        >
                          ×
                        </button>
                      </div>
                    );
                  })}
                </div>

                <div className="vf2-cart-actions-row">
                  <Link to="/shop" className="vf2-cart-muted-btn">
                    Return to shop
                  </Link>

                  <button
                    type="button"
                    className="vf2-cart-muted-btn"
                    onClick={() => {
                      loadCart();
                      window.dispatchEvent(new Event("cartChanged"));
                    }}
                  >
                    Update Cart
                  </button>
                </div>
              </div>

              {availableCoupons.length > 0 && (
                <section className="vf2-available-coupons">
                  <div className="vf2-coupon-title-row">
                    <h2>Available Coupons</h2>
                    <span>Click a code to apply it</span>
                  </div>

                  <div className="vf2-coupon-list">
                    {availableCoupons.map((coupon) => (
                      <button
                        type="button"
                        className="vf2-coupon-card"
                        key={coupon.id}
                        onClick={() => applyCoupon(null, coupon.code)}
                        disabled={applyingCoupon}
                      >
                        <span>{couponLabel(coupon)}</span>
                        <strong>{coupon.code}</strong>
                        <small>{couponTerms(coupon)}</small>
                      </button>
                    ))}
                  </div>
                </section>
              )}

              <form className="vf2-coupon-box" onSubmit={applyCoupon}>
                <label>Coupon Code</label>
                <input
                  value={couponCode}
                  onChange={(e) => setCouponCode(e.target.value)}
                  placeholder="Enter code"
                />
                <button type="submit" disabled={applyingCoupon}>
                  {applyingCoupon ? "Applying..." : "Apply Coupon"}
                </button>
              </form>

              {couponInfo?.code && (
                <div className="vf2-applied-coupon">
                  <span>
                    Applied coupon: <strong>{couponInfo.code}</strong>
                  </span>
                  <button type="button" onClick={clearAppliedCoupon}>Remove</button>
                </div>
              )}

              {(couponMessage || couponError) && (
                <p
                  className={`vf2-coupon-message ${
                    couponError ? "error" : "success"
                  }`}
                >
                  {couponError || couponMessage}
                </p>
              )}
            </div>

            <aside className="vf2-cart-summary">
              <h2>Cart Total</h2>

              <div>
                <span>Subtotal:</span>
                <b>{money(subtotal)}</b>
              </div>

              {discountAmount > 0 && (
                <div className="discount-line">
                  <span>Discount:</span>
                  <b>-{money(discountAmount)}</b>
                </div>
              )}

              <div>
                <span>Shipping:</span>
                <b>Free</b>
              </div>

              <div className="vf2-grand-total">
                <span>Total:</span>
                <b>{money(total)}</b>
              </div>

              <Link to="/checkout" className="vf2-checkout-btn">
                Proceed to checkout
              </Link>
            </aside>
          </div>
        )}
      </section>

      {relatedProducts.length > 0 && (
        <section className="vf2-cart-related vf2-cart-container">
          <h2>Related Products</h2>
          <div className="vf2-cart-related-grid">
            {relatedProducts.map((item) => {
              const product = item.product || item;
              return <ProductCard key={item.id || product.id} product={product} />;
            })}
          </div>
        </section>
      )}
    </main>
  );
}

export default Cart;
