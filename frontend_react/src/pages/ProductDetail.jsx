import React, { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import api from "../api/client.js";
import ProductCard from "../components/ProductCard.jsx";
import { apiErrorMessage, getAvailableStock, isOutOfStock, stockMessage } from "../utils/stock.js";

export default function ProductDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [product, setProduct] = useState(null);
  const [related, setRelated] = useState([]);
  const [qty, setQty] = useState(1);

  useEffect(() => {
    api.get(`/products/${id}/`).then((res) => setProduct(res.data)).catch(() => {});
    api.get(`/products/${id}/related/`).then((res) => setRelated(res.data)).catch(() => setRelated([]));
  }, [id]);

  const addCart = async () => {
    if (!localStorage.getItem("access_token")) {
      navigate("/login");
      return;
    }

    if (isOutOfStock(product, qty)) {
      alert(stockMessage(product, qty));
      return;
    }

    try {
      await api.post("/cart/", { product_id: product.id, quantity: qty });
      window.dispatchEvent(new Event("cartChanged"));
      navigate("/cart");
    } catch (err) {
      alert(apiErrorMessage(err, "Unable to add cart"));
    }
  };

  if (!product) return <main className="vf-loader">Loading product...</main>;

  const thumbs = product.gallery?.length ? product.gallery : [{ id: "main", image_url: product.image_url }];
  const availableStock = getAvailableStock(product);
  const canIncreaseQty = !Number.isFinite(availableStock) || qty < availableStock;
  const outOfStock = isOutOfStock(product, 1);

  return (
    <main className="vf-detail">
      <div className="vf-detail-grid">
        <div className="vf-thumbs">
          {thumbs.map((img) => (
            <div key={img.id}>
              <img src={img.image_url} alt={product.name} />
            </div>
          ))}
        </div>

        <div className="vf-detail-img">
          <img src={product.image_url} alt={product.name} />
        </div>

        <div className="vf-detail-info">
          <span className="stock">{outOfStock ? "Out of Stock" : "In Stock"}</span>
          <h1>{product.name}</h1>
          <p className="vf-detail-rating">★★★★★ {product.reviews_count} Review</p>

          <div className="vf-detail-price">
            <strong>₹{product.price}</strong>
            {product.old_price && <del>₹{product.old_price}</del>}
            {product.discount_percentage > 0 && <span>{product.discount_percentage}% Off</span>}
          </div>

          <p>{product.short_description || product.description}</p>

          <div className="vf-qty">
            <button type="button" onClick={() => setQty(Math.max(1, qty - 1))}>-</button>
            <span>{qty}</span>
            <button
              type="button"
              onClick={() => {
                if (!canIncreaseQty) {
                  alert(stockMessage(product, qty + 1));
                  return;
                }
                setQty(qty + 1);
              }}
              disabled={outOfStock}
            >
              +
            </button>
          </div>

          <button
            type="button"
            className="vf-add-main"
            onClick={addCart}
            disabled={outOfStock}
          >
            Add To Cart ♧
          </button>

          <div className="vf-meta">
            <p><b>Category:</b> <Link to={`/shop?category=${product.category_slug}`}>{product.category_name}</Link></p>
            <p><b>Brand:</b> {product.brand}</p>
            <p><b>Weight:</b> {product.weight}</p>
            <p><b>Type:</b> {product.product_type}</p>
            <p><b>Tags:</b> {product.tags}</p>
          </div>
        </div>
      </div>

      <section className="vf-description">
        <h2>Description</h2>
        <p>{product.description}</p>
        {product.additional_information && (
          <>
            <h2>Additional Information</h2>
            <p>{product.additional_information}</p>
          </>
        )}
      </section>

      {related.length > 0 && (
        <section className="vf-section">
          <div className="vf-title">
            <h2>Related Products</h2>
            <Link to="/shop">View All →</Link>
          </div>
          <div className="vf-product-grid">
            {related.map((p) => <ProductCard key={p.id} product={p} />)}
          </div>
        </section>
      )}
    </main>
  );
}
