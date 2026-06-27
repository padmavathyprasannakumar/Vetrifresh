import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/client";
import ProductCard from "../components/ProductCard";
import "./HomeReferenceSection.css";

function WideBannerCarousel({ banners }) {
  const [active, setActive] = useState(0);

  useEffect(() => {
    if (!banners || banners.length <= 1) return undefined;

    const timer = setInterval(() => {
      setActive((prev) => (prev + 1) % banners.length);
    }, 3500);

    return () => clearInterval(timer);
  }, [banners]);

  if (!banners || banners.length === 0) return null;

  return (
    <section className="vf-wide-carousel vf-wide-carousel-auto">
      <div className="vf-wide-track">
        {banners.map((banner, index) => (
          <Link
            to={banner.button_link || "/shop"}
            key={banner.id || index}
            className={`vf-wide-slide ${
              active === index ? "active" : ""
            } animate-${banner.content_animation || "fade-up"}`}
            style={{
              backgroundColor: banner.bg_color || "#8ecb22",
              color: banner.text_color || "#ffffff",
            }}
            aria-hidden={active === index ? "false" : "true"}
          >
            {banner.image_url && (
              <img src={banner.image_url} alt={banner.title} />
            )}

            <div className="vf-wide-content">
              {banner.badge && <p>{banner.badge}</p>}
              <h2>{banner.title}</h2>
              {banner.subtitle && <h3>{banner.subtitle}</h3>}

              <span
                className={`vf-animated-btn btn-${
                  banner.button_animation || "pulse"
                }`}
              >
                {banner.button_text || "Shop Now"} →
              </span>
            </div>
          </Link>
        ))}
      </div>

      {banners.length > 1 && (
        <div className="vf-carousel-dots">
          {banners.map((_, index) => (
            <button
              type="button"
              key={index}
              className={active === index ? "active" : ""}
              onClick={() => setActive(index)}
              aria-label={`Go to banner ${index + 1}`}
            />
          ))}
        </div>
      )}
    </section>
  );
}

function Home() {
  const [home, setHome] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .get("/home/")
      .then((res) => {
        setHome(res.data);
        setError("");
      })
      .catch((err) => {
        console.log("Home API Error:", err);
        setError("Home API not loading. Check backend /api/home/ and CORS.");
      });
  }, []);

  if (!home && !error) {
    return <div className="vf-loader">Loading VetriFresh...</div>;
  }

  const banners = home?.banners || [];

  const mainBanner =
    banners.find((item) => item.banner_type === "main") || null;

  const sideBanners = banners
    .filter((item) => item.banner_type === "side")
    .slice(0, 2);

  const wideBanners = banners.filter((item) => item.banner_type === "wide");

  const categories = home?.categories || [];
  const promoCards = home?.promo_cards || [];
  const services = home?.service_features || [];
  const popularProducts = home?.popular_products || [];
  const latestProducts = home?.latest_products || [];
  const testimonials = home?.testimonials || [];
  const newsPosts = home?.news_posts || [];
  const instagramImages = home?.instagram_images || [];

  const products = popularProducts.length ? popularProducts : latestProducts;

  return (
    <main className="vf-home vf-home-ref">
      {error && <div className="vf-api-error">{error}</div>}

      {/* TOP HERO SECTION: LEFT 1 BIG BANNER + RIGHT 2 SMALL BANNERS */}
      <section className="vf-hero-grid">
        {mainBanner ? (
          <Link
            to={mainBanner.button_link || "/shop"}
            className={`vf-hero-main animate-${
              mainBanner.content_animation || "fade-up"
            }`}
            style={{
              backgroundColor: mainBanner.bg_color || "#00B207",
              color: mainBanner.text_color || "#ffffff",
            }}
          >
            <div className="vf-hero-copy">
              {mainBanner.badge && <p>{mainBanner.badge}</p>}

              <h1>{mainBanner.title}</h1>

              <div className="vf-sale-row">
                <span>{mainBanner.subtitle || "Sale up to"}</span>

                {mainBanner.discount_label && (
                  <b>{mainBanner.discount_label}</b>
                )}
              </div>

              <small>Free shipping on all your order.</small>

              <em
                className={`vf-animated-btn btn-${
                  mainBanner.button_animation || "pulse"
                }`}
              >
                {mainBanner.button_text || "Shop Now"} →
              </em>
            </div>

            {mainBanner.image_url && (
              <img src={mainBanner.image_url} alt={mainBanner.title} />
            )}
          </Link>
        ) : (
          <div className="vf-empty-admin">
            Add Main Hero Banner in Admin → Banners
          </div>
        )}

        <div className="vf-side-stack">
          {sideBanners.length > 0 ? (
            sideBanners.map((banner) => (
              <Link
                to={banner.button_link || "/shop"}
                key={banner.id}
                className={`vf-side-banner animate-${
                  banner.content_animation || "fade-up"
                }`}
                style={{
                  backgroundColor: banner.bg_color || "#f7f7f7",
                  color: banner.text_color || "#111111",
                }}
              >
                <div>
                  {banner.badge && <p>{banner.badge}</p>}

                  <h2>{banner.title}</h2>

                  {banner.subtitle && <span>{banner.subtitle}</span>}

                  <strong
                    className={`vf-animated-btn btn-${
                      banner.button_animation || "pulse"
                    }`}
                  >
                    {banner.button_text || "Shop Now"} →
                  </strong>
                </div>

                {banner.image_url && (
                  <img src={banner.image_url} alt={banner.title} />
                )}
              </Link>
            ))
          ) : (
            <>
              <div className="vf-empty-admin">Add Side Banner 1</div>
              <div className="vf-empty-admin">Add Side Banner 2</div>
            </>
          )}
        </div>
      </section>

      {/* SERVICE FEATURES */}
      {services.length > 0 && (
        <section className="vf-service-row">
          {services.map((item) => (
            <div className="vf-service" key={item.id}>
              <span>{item.icon}</span>
              <div>
                <h4>{item.title}</h4>
                <p>{item.subtitle}</p>
              </div>
            </div>
          ))}
        </section>
      )}

      {/* POPULAR CATEGORIES - REFERENCE DESIGN */}
      <section className="vf-section vf-reference-category-section">
        <div className="vf-title vf-reference-title">
          <h2>Popular Categories</h2>
          <Link to="/shop">View All →</Link>
        </div>

        {categories.length > 0 ? (
          <div className="vf-category-grid vf-reference-category-grid">
            {categories.slice(0, 12).map((category) => (
              <Link
                to={`/shop?category=${category.slug || category.id}`}
                className="vf-cat-card vf-reference-cat-card"
                key={category.id}
              >
                <span className="vf-reference-cat-img">
                  {category.image_url ? (
                    <img src={category.image_url} alt={category.name} />
                  ) : (
                    <span className="vf-reference-cat-placeholder">
                      {category.name?.charAt(0)?.toUpperCase() || "C"}
                    </span>
                  )}
                </span>

                <h3>{category.name}</h3>
              </Link>
            ))}
          </div>
        ) : (
          <div className="vf-empty-admin">
            Add 12 active categories in Admin → Categories
          </div>
        )}
      </section>

     {/* THREE PROMO CARDS - ADMIN DYNAMIC REFERENCE DESIGN */}
{promoCards.length > 0 ? (
  <section className="vf-promo-grid vf-reference-promo-grid">
    {promoCards.slice(0, 3).map((promo, index) => {
      const fallbackStyle = index === 2 ? "yellow" : "dark";
      const styleName = promo.promo_style || fallbackStyle;

      // Force full image design, so no top color box appears
      const imagePosition = "full-cover";

      const overlayOpacity = promo.overlay_opacity ?? 0;

      return (
        <Link
          to={promo.button_link || "/shop"}
          className={`vf-promo-card vf-reference-promo-card promo-style-${styleName} promo-image-${imagePosition} animate-${
            promo.content_animation || "fade-up"
          } vf-reference-promo-${index + 1}`}
          key={promo.id}
          style={{
            "--promo-bg": "transparent",
            "--promo-text":
              promo.text_color ||
              (styleName === "yellow" || styleName === "light"
                ? "#111111"
                : "#ffffff"),
            "--promo-button-bg": promo.button_bg_color || "#ffffff",
            "--promo-button-text": promo.button_text_color || "#00b207",
            "--promo-overlay-opacity": overlayOpacity,
          }}
        >
          {promo.image_url && (
            <img
              className="vf-promo-full-img"
              src={promo.image_url}
              alt={promo.title}
            />
          )}

          <div className="vf-reference-promo-content">
            {promo.badge && <p>{promo.badge}</p>}
            <h2>{promo.title}</h2>
            {promo.subtitle && <span>{promo.subtitle}</span>}
            <b>{promo.button_text || "Shop now"} →</b>
          </div>
        </Link>
      );
    })}
  </section>
) : (
  <div className="vf-empty-admin">
    Add 3 active promo cards in Admin → Promo Cards
  </div>
)}

      {/* AUTO CAROUSEL BEFORE POPULAR PRODUCTS */}
      <WideBannerCarousel banners={wideBanners} />

      {/* POPULAR PRODUCTS */}
      <section className="vf-section">
        <div className="vf-title">
          <h2>Popular Products</h2>
          <Link to="/shop">View All →</Link>
        </div>

        {products.length > 0 ? (
          <div className="vf-product-grid">
            {products.slice(0, 8).map((product) => (
              <ProductCard product={product} key={product.id} />
            ))}
          </div>
        ) : (
          <div className="vf-empty-admin">
            Add products in Admin → Products
          </div>
        )}
      </section>

      {/* LATEST NEWS */}
      {newsPosts.length > 0 && (
        <section className="vf-section vf-news-wrap">
          <div className="vf-title centered">
            <h2>Latest News</h2>
          </div>

          <div className="vf-news-grid">
            {newsPosts.slice(0, 3).map((post) => (
              <article className="vf-news" key={post.id}>
                {post.image_url && (
                  <img src={post.image_url} alt={post.title} />
                )}

                <span>{post.date_label}</span>

                <small>
                  {post.category} &nbsp; | &nbsp; By {post.author} &nbsp; |
                  &nbsp; {post.comments_count} Comments
                </small>

                <h3>{post.title}</h3>

                <Link to="/blog">Read More →</Link>
              </article>
            ))}
          </div>
        </section>
      )}

      {/* INSTAGRAM */}
      {instagramImages.length > 0 && (
        <section className="vf-instagram">
          <h2>Follow us on Instagram</h2>

          <div className="vf-insta-row">
            {instagramImages.slice(0, 6).map((item, index) => {
              const delay = item.animation_delay_seconds ?? index * 0.35;
              const duration = item.animation_duration_seconds ?? 0.6;

              return (
                <a
                  href={item.instagram_url || "#"}
                  className={`vf-insta-card insta-animate-${
                    item.animation || "fade-up"
                  }`}
                  key={item.id}
                  style={{
                    animationDelay: `${delay}s`,
                    animationDuration: `${duration}s`,
                  }}
                  target="_blank"
                  rel="noreferrer"
                >
                  {item.image_url && (
                    <img src={item.image_url} alt={item.title} />
                  )}
                  <span>◎</span>
                </a>
              );
            })}
          </div>
        </section>
      )}

      {/* TESTIMONIALS */}
      {testimonials.length > 0 && (
        <section className="vf-section vf-testimonials">
          <div className="vf-title">
            <h2>Client Testimonials</h2>

            <div>
              <button type="button">←</button>
              <button type="button">→</button>
            </div>
          </div>

          <div className="vf-test-grid">
            {testimonials.map((item) => (
              <div className="vf-test" key={item.id}>
                <div className="vf-quote">❝</div>

                <p>{item.message}</p>

                <div className="vf-test-user">
                  {item.image_url ? (
                    <img src={item.image_url} alt={item.name} />
                  ) : (
                    <div className="vf-test-avatar">
                      {item.name?.charAt(0)?.toUpperCase() || "U"}
                    </div>
                  )}

                  <div>
                    <h4>{item.name}</h4>
                    <small>{item.role}</small>
                  </div>

                  <b>{"★".repeat(Number(item.rating || 5))}</b>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}
    </main>
  );
}

export default Home;