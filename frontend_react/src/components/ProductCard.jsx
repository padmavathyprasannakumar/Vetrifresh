import React from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/client";
import { apiErrorMessage, isOutOfStock, stockMessage } from "../utils/stock";
import "./ProductCardHover.css";

function ProductCard({ product }) {
  const navigate = useNavigate();

  if (!product) return null;

  const imageUrl = product.image_url || product.image;
  const price = Number(product.price || 0).toFixed(0);
  const oldPrice = product.old_price ? Number(product.old_price).toFixed(2) : null;
  const rating = Number(product.rating || 0).toFixed(1);

  const hoverText =
    product.short_description ||
    `Fresh ${product.name} packed with natural goodness.`;

  const saleText =
    product.sale_label ||
    product.badge ||
    (product.discount_percentage > 0 ? `${product.discount_percentage}% OFF` : "");

  const goToDetails = () => {
    navigate(`/product/${product.id}`);
  };

  const addToCart = async (event) => {
    event.preventDefault();
    event.stopPropagation();

    if (!localStorage.getItem("access_token")) {
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

  const addToWishlist = async (event) => {
    event.preventDefault();
    event.stopPropagation();

    if (!localStorage.getItem("access_token")) {
      navigate("/login");
      return;
    }

    try {
      await api.post("/wishlist/", {
        product_id: product.id,
      });

      window.dispatchEvent(new Event("wishlistChanged"));
      navigate("/wishlist");
    } catch (error) {
      alert(error.response?.data?.detail || "Unable to add product to wishlist");
    }
  };

  return (
    <article className="vf-product-card vf-hover-product-card">
      {saleText && <span className="vf-sale">{saleText}</span>}

      <div className="vf-product-actions">
        <button
          type="button"
          className="vf-action-circle"
          onClick={addToWishlist}
          title="Add to wishlist"
        >
          ♡
        </button>

        <button
          type="button"
          className="vf-action-circle"
          onClick={goToDetails}
          title="View product"
        >
          👁
        </button>
      </div>

      <div className="vf-product-img" onClick={goToDetails}>
        {imageUrl ? (
          <img src={imageUrl} alt={product.name} />
        ) : (
          <div className="no-img">No Image</div>
        )}

        <span className="vf-rating-badge">★ {rating}</span>

        <div className="vf-hover-description">
          “{hoverText}”
        </div>

        <button
          type="button"
          className="vf-view-cart"
          onClick={addToCart}
        >
          View Cart <b>›</b>
        </button>
      </div>

      <div className="vf-product-body" onClick={goToDetails}>
        <h3>{product.name}</h3>

        <p>
          <strong>₹{price}/kg</strong>
          {oldPrice && <del>₹{oldPrice}</del>}
        </p>

        <div className="vf-stars">
          ★★★★<span>★</span>
        </div>
      </div>

      <button
        type="button"
        className="vf-bag"
        onClick={addToCart}
        title="Add to cart"
      >
        🛍
      </button>
    </article>
  );
}

export default ProductCard;
