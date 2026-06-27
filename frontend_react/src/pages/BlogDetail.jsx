import React, { useEffect, useMemo, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import api from "../api/client";
import "./BlogDetail.css";

function BlogDetail() {
  const { slug } = useParams();
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);
  const [post, setPost] = useState(null);
  const [pageData, setPageData] = useState({
    banner: null,
    posts: [],
    categories: [],
    popular_tags: [],
    recent_posts: [],
    gallery_images: [],
  });

  useEffect(() => {
    const loadBlogDetail = async () => {
      setLoading(true);

      try {
        const res = await api.get("/blog-page/");
        const data = res.data || {};
        const posts = data.posts || [];
        const currentPost = posts.find((item) => item.slug === slug);

        setPageData({
          banner: data.banner || null,
          posts,
          categories: data.categories || [],
          popular_tags: data.popular_tags || [],
          recent_posts: data.recent_posts || [],
          gallery_images: data.gallery_images || [],
        });

        setPost(currentPost || null);
      } catch (err) {
        console.log("Blog detail API error:", err);
        setPost(null);
      } finally {
        setLoading(false);
      }
    };

    loadBlogDetail();
  }, [slug]);

  const relatedPosts = useMemo(() => {
    if (!post) return [];

    return (pageData.posts || [])
      .filter((item) => item.id !== post.id)
      .filter((item) => {
        if (!post.category_slug) return true;
        return item.category_slug === post.category_slug;
      })
      .slice(0, 3);
  }, [pageData.posts, post]);

  const recentPosts = pageData.recent_posts || [];
  const categories = pageData.categories || [];
  const tags = pageData.popular_tags || [];
  const galleryImages = pageData.gallery_images || [];

  return (
    <main className="vf-blog-detail-page">
      <section
        className="vf-blog-detail-hero"
        style={
          pageData.banner?.background_image_url
            ? {
                backgroundImage: `linear-gradient(90deg, rgba(0,0,0,.70), rgba(0,0,0,.22)), url(${pageData.banner.background_image_url})`,
              }
            : undefined
        }
      >
        <div className="vf-blog-detail-container">
          <div className="vf-blog-detail-breadcrumb">
            <Link to="/">⌂ Home</Link>
            <span>›</span>
            <Link to="/blog">Blog</Link>
            <span>›</span>
            <span>{post?.title || "Blog Details"}</span>
          </div>
        </div>
      </section>

      <section className="vf-blog-detail-container vf-blog-detail-main">
        {loading ? (
          <div className="vf-blog-detail-empty">Loading blog details...</div>
        ) : !post ? (
          <div className="vf-blog-detail-empty">
            <h1>Blog post not found</h1>
            <p>This blog post may be inactive or the link may be incorrect.</p>
            <button type="button" onClick={() => navigate("/blog")}>Back to Blog</button>
          </div>
        ) : (
          <div className="vf-blog-detail-layout">
            <article className="vf-blog-detail-article">
              {post.image_url && (
                <div className="vf-blog-detail-image">
                  <img src={post.image_url} alt={post.title} />
                  {post.is_video && <span className="vf-blog-detail-play">▶</span>}
                </div>
              )}

              <div className="vf-blog-detail-meta">
                <span>👤 {post.author_name || "Admin"}</span>
                <span>📂 {post.category_name || "Blog"}</span>
                <span>💬 {post.comments_count || 0} Comments</span>
                <span>📅 {post.date_label || "18 NOV"}</span>
              </div>

              <h1>{post.title}</h1>

              <p className="vf-blog-detail-excerpt">
                {post.excerpt || "No blog content added yet."}
              </p>

              {post.video_url && (
                <a
                  className="vf-blog-detail-video"
                  href={post.video_url}
                  target="_blank"
                  rel="noreferrer"
                >
                  Watch Video
                </a>
              )}

              <div className="vf-blog-detail-actions">
                <Link to="/blog">← Back to Blog</Link>
                <Link to="/shop">Shop Now →</Link>
              </div>
            </article>

            <aside className="vf-blog-detail-sidebar">
              {categories.length > 0 && (
                <div className="vf-blog-detail-widget">
                  <h3>All Categories</h3>
                  <Link to="/blog">All Posts</Link>
                  {categories.map((cat) => (
                    <Link key={cat.id} to={`/blog?category=${cat.slug}`}>
                      <span>{cat.name}</span>
                      <small>{cat.post_count || 0}</small>
                    </Link>
                  ))}
                </div>
              )}

              {tags.length > 0 && (
                <div className="vf-blog-detail-widget">
                  <h3>Popular Tag</h3>
                  <div className="vf-blog-detail-tags">
                    {tags.map((tag) => (
                      <Link key={tag.id} to={`/blog?tag=${tag.filter_value}`}>
                        {tag.title}
                      </Link>
                    ))}
                  </div>
                </div>
              )}

              {recentPosts.length > 0 && (
                <div className="vf-blog-detail-widget">
                  <h3>Recently Added</h3>
                  {recentPosts.map((item) => {
                    const recent = item.post || {};

                    return (
                      <Link
                        className="vf-blog-detail-recent"
                        key={item.id}
                        to={`/blog/${recent.slug}`}
                      >
                        <span>
                          {recent.image_url ? (
                            <img src={recent.image_url} alt={recent.title} />
                          ) : (
                            "No Image"
                          )}
                        </span>
                        <div>
                          <strong>{recent.title}</strong>
                          <small>{recent.date_label}</small>
                        </div>
                      </Link>
                    );
                  })}
                </div>
              )}

              {galleryImages.length > 0 && (
                <div className="vf-blog-detail-widget">
                  <h3>Our Gallery</h3>
                  <div className="vf-blog-detail-gallery">
                    {galleryImages.map((img) => (
                      <a href={img.url || "#"} key={img.id}>
                        <img src={img.image_url} alt={img.title} />
                      </a>
                    ))}
                  </div>
                </div>
              )}
            </aside>
          </div>
        )}
      </section>

      {relatedPosts.length > 0 && (
        <section className="vf-blog-detail-container vf-blog-detail-related">
          <h2>Related Posts</h2>

          <div className="vf-blog-detail-related-grid">
            {relatedPosts.map((item) => (
              <article className="vf-blog-detail-related-card" key={item.id}>
                {item.image_url && <img src={item.image_url} alt={item.title} />}
                <div>
                  <span>{item.date_label}</span>
                  <h3>{item.title}</h3>
                  <p>{item.excerpt}</p>
                  <Link to={`/blog/${item.slug}`}>Read More →</Link>
                </div>
              </article>
            ))}
          </div>
        </section>
      )}
    </main>
  );
}

export default BlogDetail;
