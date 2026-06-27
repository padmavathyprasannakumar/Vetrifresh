import React, { useEffect, useMemo, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import api from "../api/client";
import "./Blog.css";

function Blog() {
  const [searchParams, setSearchParams] = useSearchParams();

  const [data, setData] = useState({
    banner: null,
    categories: [],
    popular_tags: [],
    discount_banner: null,
    recent_posts: [],
    gallery_images: [],
    brand_logos: [],
    posts: [],
    total_posts: 0,
  });

  const [loading, setLoading] = useState(true);
  const [categoriesOpen, setCategoriesOpen] = useState(false);
  const [priceOpen, setPriceOpen] = useState(true);
  const [blogPrice, setBlogPrice] = useState(1500);

  const activeFilters = useMemo(() => {
    return {
      category: searchParams.get("category") || "",
      tag: searchParams.get("tag") || "",
      sort: searchParams.get("sort") || "latest",
      search: searchParams.get("search") || "",
    };
  }, [searchParams]);

  const updateFilter = (key, value) => {
    const next = new URLSearchParams(searchParams);

    if (value) {
      next.set(key, value);
    } else {
      next.delete(key);
    }

    setSearchParams(next);
  };

  useEffect(() => {
    const loadBlog = async () => {
      setLoading(true);

      try {
        const query = searchParams.toString();
        const res = await api.get(`/blog-page/${query ? `?${query}` : ""}`);
        setData(res.data || {});
      } catch (err) {
        console.log("Blog page API error:", err);
      } finally {
        setLoading(false);
      }
    };

    loadBlog();
  }, [searchParams]);

  const banner = data.banner;
  const categories = data.categories || [];
  const posts = data.posts || [];
  const tags = data.popular_tags || [];
  const discountBanner = data.discount_banner;
  const recentPosts = data.recent_posts || [];
  const galleryImages = data.gallery_images || [];
  const brandLogos = data.brand_logos || [];

  return (
    <main className="vf-blog-page">
      <section
        className="vf-blog-hero"
        style={
          banner?.background_image_url
            ? {
                backgroundImage: `linear-gradient(90deg, rgba(0,0,0,.70), rgba(0,0,0,.20)), url(${banner.background_image_url})`,
              }
            : undefined
        }
      >
        <div className="vf-blog-container">
          <div className="vf-blog-breadcrumb">
            <Link to="/">⌂ Home</Link>
            <span>›</span>
            <span>{banner?.breadcrumb_text || "Blog"}</span>
          </div>
        </div>
      </section>

      <section className="vf-blog-container vf-blog-main">
        <aside className="vf-blog-sidebar">
          <button type="button" className="vf-blog-filter-btn">
            <span>Filter</span>
            <span className="vf-blog-filter-icon">☷</span>
          </button>

          <div className="vf-blog-accordion">
            <button
              type="button"
              className={`vf-blog-accordion-head ${
                categoriesOpen ? "active" : ""
              }`}
              onClick={() => setCategoriesOpen(!categoriesOpen)}
            >
              <span>All Categories</span>

              <span className={`vf-blog-arrow ${categoriesOpen ? "open" : ""}`}>
                <svg width="12" height="8" viewBox="0 0 12 8" fill="none">
                  <path
                    d="M1.5 1.5L6 6L10.5 1.5"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              </span>
            </button>

            {categoriesOpen && (
              <div className="vf-blog-accordion-body">
                <button
                  type="button"
                  className={`vf-blog-category-btn ${
                    !activeFilters.category ? "active" : ""
                  }`}
                  onClick={() => updateFilter("category", "")}
                >
                  <span>All Posts</span>
                  <small>{data.total_posts || posts.length}</small>
                </button>

                {categories.map((cat) => (
                  <button
                    key={cat.id}
                    type="button"
                    className={`vf-blog-category-btn ${
                      activeFilters.category === cat.slug ? "active" : ""
                    }`}
                    onClick={() => updateFilter("category", cat.slug)}
                  >
                    <span>{cat.name}</span>
                    <small>{cat.post_count || 0}</small>
                  </button>
                ))}
              </div>
            )}
          </div>

          <div className="vf-blog-accordion">
            <button
              type="button"
              className={`vf-blog-accordion-head ${priceOpen ? "active" : ""}`}
              onClick={() => setPriceOpen(!priceOpen)}
            >
              <span>Price</span>

              <span className={`vf-blog-arrow ${priceOpen ? "open" : ""}`}>
                <svg width="12" height="8" viewBox="0 0 12 8" fill="none">
                  <path
                    d="M1.5 1.5L6 6L10.5 1.5"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              </span>
            </button>

            {priceOpen && (
              <div className="vf-blog-price-panel">
                <input
                  type="range"
                  min="50"
                  max="1500"
                  step="50"
                  value={blogPrice}
                  onChange={(e) => setBlogPrice(e.target.value)}
                  className="vf-blog-price-range"
                />

                <div className="vf-blog-price-text">
                  Price:{" "}
                  <strong>
                    ₹50 — ₹{Number(blogPrice).toLocaleString("en-IN")}
                  </strong>
                </div>
              </div>
            )}
          </div>

          {tags.length > 0 && (
            <div className="vf-blog-widget vf-blog-tags-widget">
              <div className="vf-blog-widget-title">Popular Tag</div>

              <div className="vf-blog-tags">
                {tags.map((tag) => (
                  <button
                    key={tag.id}
                    type="button"
                    className={
                      activeFilters.tag === tag.filter_value ? "active" : ""
                    }
                    onClick={() => updateFilter("tag", tag.filter_value)}
                  >
                    {tag.title}
                  </button>
                ))}
              </div>
            </div>
          )}

          {discountBanner && (
            <div
              className="vf-blog-discount"
              style={
                discountBanner.image_url
                  ? {
                      backgroundImage: `linear-gradient(180deg, rgba(255,255,255,.10), rgba(0,0,0,.12)), url(${discountBanner.image_url})`,
                    }
                  : undefined
              }
            >
              <div>
                <strong>{discountBanner.discount_text}</strong>
                <span>{discountBanner.subtitle}</span>
              </div>

              <Link to={discountBanner.button_link || "/shop"}>
                {discountBanner.button_text || "Shop Now"}
              </Link>
            </div>
          )}

          {recentPosts.length > 0 && (
            <div className="vf-blog-widget">
              <div className="vf-blog-widget-title">Recently Added</div>

              <div className="vf-blog-recent-list">
                {recentPosts.map((item) => {
                  const post = item.post || {};

                  return (
                    <div className="vf-blog-recent" key={item.id}>
                      <div className="vf-blog-recent-img">
                        {post.image_url ? (
                          <img src={post.image_url} alt={post.title} />
                        ) : (
                          <span>No Image</span>
                        )}
                      </div>

                      <div>
                        <h4>{post.title}</h4>
                        <p>{post.date_label}</p>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {galleryImages.length > 0 && (
            <div className="vf-blog-widget">
              <div className="vf-blog-widget-title">Our Gallery</div>

              <div className="vf-blog-gallery">
                {galleryImages.map((img) => (
                  <a href={img.url || "#"} key={img.id}>
                    <img src={img.image_url} alt={img.title} />
                  </a>
                ))}
              </div>
            </div>
          )}
        </aside>

        <section className="vf-blog-content">
          <div className="vf-blog-toolbar">
            <div className="vf-blog-sort">
              <span>Sort by:</span>

              <select
                value={activeFilters.sort}
                onChange={(e) => updateFilter("sort", e.target.value)}
              >
                <option value="latest">Latest</option>
                <option value="oldest">Oldest</option>
                <option value="name">Name</option>
                <option value="comments">Most Comments</option>
              </select>
            </div>

            <div className="vf-blog-count">
              {data.total_posts || posts.length} Posts Found
            </div>
          </div>

          {loading ? (
            <div className="vf-blog-empty">Loading blog posts...</div>
          ) : posts.length === 0 ? (
            <div className="vf-blog-empty">No blog posts found.</div>
          ) : (
            <div className="vf-blog-grid">
              {posts.map((post) => (
                <article className="vf-blog-card" key={post.id}>
                  <div className="vf-blog-card-img">
                    {post.image_url ? (
                      <img src={post.image_url} alt={post.title} />
                    ) : (
                      <div className="vf-blog-no-image">No Image</div>
                    )}

                    <div className="vf-blog-date">{post.date_label}</div>

                    {post.is_video && <div className="vf-blog-play">▶</div>}
                  </div>

                  <div className="vf-blog-card-body">
                    <div className="vf-blog-meta">
                      <span>🏷 {post.category_name || post.category}</span>
                      <span>👤 By {post.author_name || "Admin"}</span>
                      <span>💬 {post.comments_count} Comments</span>
                    </div>

                    <h3>{post.title}</h3>
                    <p>{post.excerpt}</p>

                    <Link to={`/blog/${post.slug}`}>
                      {post.read_more_text || "Read More"} →
                    </Link>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>
      </section>

      {brandLogos.length > 0 && (
        <section className="vf-blog-container vf-blog-brands">
          {brandLogos.map((brand) => (
            <a href={brand.url || "#"} key={brand.id}>
              {brand.image_url ? (
                <img src={brand.image_url} alt={brand.title} />
              ) : (
                <span>{brand.text_logo || brand.title}</span>
              )}
            </a>
          ))}
        </section>
      )}
    </main>
  );
}

export default Blog;
