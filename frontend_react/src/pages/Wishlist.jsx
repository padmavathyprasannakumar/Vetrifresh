import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../api/client";
import ProductCard from "../components/ProductCard";
import { apiErrorMessage, isOutOfStock, stockMessage } from "../utils/stock";
import "./Wishlist.css";

function Wishlist() {
  const navigate = useNavigate();
  const [items, setItems] = useState([]);
  const [relatedProducts, setRelatedProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  const isLoggedIn = Boolean(localStorage.getItem("access_token"));

  const loadWishlist = async () => {
    if (!isLoggedIn) {
      setLoading(false);
      return;
    }

    try {
      const res = await api.get("/wishlist/");
      const list = Array.isArray(res.data) ? res.data : res.data.results || [];
      setItems(list);
    } catch (error) {
      console.log("Wishlist error", error);
      setMessage("Unable to load wishlist");
    } finally {
      setLoading(false);
    }
  };

  const loadRelatedProducts = async () => {
    try {
      const res = await api.get("/products/?popular=true");
      const list = Array.isArray(res.data) ? res.data : res.data.results || [];
      setRelatedProducts(list.slice(0, 4));
    } catch (error) {
      console.log("Related products error", error);
    }
  };

  useEffect(() => {
    loadWishlist();
    loadRelatedProducts();
  }, []);

  const removeItem = async (itemId) => {
    try {
      await api.delete(`/wishlist/${itemId}/`);
      setItems((oldItems) => oldItems.filter((item) => item.id !== itemId));
      window.dispatchEvent(new Event("wishlistChanged"));
    } catch (error) {
      alert("Unable to remove item");
    }
  };

  const addToCart = async (product) => {
    if (!isLoggedIn) {
      navigate("/login");
      return;
    }

    if (isOutOfStock(product, 1)) {
      alert(stockMessage(product, 1));
      return;
    }

    try {
      await api.post("/cart/", {
        product_id: product.id,
        quantity: 1,
      });
      window.dispatchEvent(new Event("cartChanged"));
      navigate("/cart");
    } catch (error) {
      alert(apiErrorMessage(error, "Unable to add product to cart"));
    }
  };

  const sharePage = (platform) => {
    const url = window.location.href;
    const text = "Check my VetriFresh wishlist";

    if (platform === "facebook") {
      window.open(`https://www.facebook.com/sharer/sharer.php?u=${url}`, "_blank");
    } else if (platform === "twitter") {
      window.open(`https://twitter.com/intent/tweet?text=${text}&url=${url}`, "_blank");
    } else {
      navigator.clipboard?.writeText(url);
      alert("Wishlist link copied");
    }
  };

  return (
    <main className="vf-wishlist-page">
      <section className="vf-wishlist-hero">
        <div className="vf-wishlist-container">
          <p>
            <Link to="/">Home</Link>
            <span>›</span>
            <b>Wishlist</b>
          </p>
        </div>
      </section>

      <section className="vf-wishlist-container vf-wishlist-content">
        <h1>My Wishlist</h1>

        {!isLoggedIn && (
          <div className="vf-wishlist-empty">
            <h2>Please login to view your wishlist</h2>
            <Link to="/login">Login Now</Link>
          </div>
        )}

        {isLoggedIn && loading && (
          <div className="vf-wishlist-empty">
            <h2>Loading wishlist...</h2>
          </div>
        )}

        {isLoggedIn && !loading && items.length === 0 && (
          <div className="vf-wishlist-empty">
            <h2>Your wishlist is empty</h2>
            <p>Add products to wishlist by clicking the heart icon.</p>
            <Link to="/shop">Continue Shopping</Link>
          </div>
        )}

        {isLoggedIn && !loading && items.length > 0 && (
          <div className="vf-wishlist-card">
            <div className="vf-wishlist-header-row">
              <span>Product</span>
              <span>Price</span>
              <span>Stock Status</span>
              <span></span>
            </div>

            {items.map((item) => {
              const product = item.product;
              if (!product) return null;

              const imageUrl = product.image_url || product.image;
              const inStock = product.in_stock || product.stock > 0;

              return (
                <div className="vf-wishlist-row" key={item.id}>
                  <div className="vf-wishlist-product">
                    <img src={imageUrl} alt={product.name} />
                    <strong>{product.name}</strong>
                  </div>

                  <div className="vf-wishlist-price">
                    <b>₹{Number(product.price || 0).toFixed(2)}</b>
                    {product.old_price && (
                      <del>₹{Number(product.old_price).toFixed(2)}</del>
                    )}
                  </div>

                  <div>
                    <span className={inStock ? "vf-stock in" : "vf-stock out"}>
                      {inStock ? "In Stock" : "Out of Stock"}
                    </span>
                  </div>

                  <div className="vf-wishlist-actions">
                    <button
                      type="button"
                      disabled={!inStock}
                      onClick={() => addToCart(product)}
                    >
                      Add to Cart
                    </button>
                    <button
                      type="button"
                      className="vf-remove-wishlist"
                      onClick={() => removeItem(item.id)}
                    >
                      ×
                    </button>
                  </div>
                </div>
              );
            })}

            <div className="vf-wishlist-share">
              <b>Share:</b>
              <button onClick={() => sharePage("facebook")}>f</button>
              <button onClick={() => sharePage("twitter")}>t</button>
              <button onClick={() => sharePage("copy")}>🔗</button>
            </div>
          </div>
        )}

        {message && <p className="vf-wishlist-message">{message}</p>}
      </section>

      {relatedProducts.length > 0 && (
        <section className="vf-wishlist-container vf-related-products">
          <h2>Related Products</h2>
          <div className="vf-related-grid">
            {relatedProducts.map((product) => (
              <ProductCard product={product} key={product.id} />
            ))}
          </div>
        </section>
      )}
    </main>
  );
}

export default Wishlist;
