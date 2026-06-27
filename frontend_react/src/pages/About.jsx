import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/client";
import "./About.css";

function stars(count = 5) {
  const total = Math.max(0, Math.min(5, Number(count || 0)));
  return "★★★★★".slice(0, total);
}

function About() {
  const [data, setData] = useState({
    banner: null,
    hero: null,
    feature_section: null,
    feature_items: [],
    delivery: null,
    team_members: [],
    testimonials: [],
    brand_logos: [],
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadAbout = async () => {
      try {
        const res = await api.get("/about-page/");
        setData(res.data || {});
      } catch (err) {
        console.log("About page API error:", err);
      } finally {
        setLoading(false);
      }
    };

    loadAbout();
  }, []);

  const banner = data.banner;
  const hero = data.hero;
  const featureSection = data.feature_section;
  const features = data.feature_items || [];
  const delivery = data.delivery;
  const team = data.team_members || [];
  const testimonials = data.testimonials || [];
  const brands = data.brand_logos || [];

  if (loading) {
    return <main className="vf-about-page"><div className="vf-about-loading">Loading about page...</div></main>;
  }

  return (
    <main className="vf-about-page">
      <section
        className="vf-about-hero-banner"
        style={
          banner?.background_image_url
            ? {
                backgroundImage: `linear-gradient(90deg, rgba(0,0,0,.70), rgba(0,0,0,.22)), url(${banner.background_image_url})`,
              }
            : undefined
        }
      >
        <div className="vf-about-container">
          <div className="vf-about-breadcrumb">
            <Link to="/">⌂ Home</Link>
            <span>›</span>
            <span>{banner?.breadcrumb_text || "About Us"}</span>
          </div>
        </div>
      </section>

      <section className="vf-about-container vf-about-intro">
        <div className="vf-about-intro-text">
          <h1>{hero?.title || "100% Trusted Organic Food Store"}</h1>
          <p>{hero?.description || "Vetri Fresh is a trusted organic food store delivering fresh, high-quality groceries straight from farm to home."}</p>
          {hero?.button_text && (
            <Link to={hero?.button_link || "/shop"} className="vf-about-green-btn">
              {hero.button_text} →
            </Link>
          )}
        </div>

        <div className="vf-about-intro-image">
          {hero?.image_url ? <img src={hero.image_url} alt={hero.title} /> : <div className="vf-about-image-placeholder">Upload Hero Image</div>}
        </div>
      </section>

      <section className="vf-about-container vf-about-trust">
        <div className="vf-about-trust-image">
          {featureSection?.image_url ? <img src={featureSection.image_url} alt={featureSection.title} /> : <div className="vf-about-image-placeholder">Upload Feature Image</div>}
        </div>

        <div className="vf-about-trust-content">
          <h2>{featureSection?.title || "100% Trusted Organic Food Store"}</h2>
          <p>{featureSection?.description || "Fresh produce and organic groceries delivered with care and quality."}</p>

          <div className="vf-about-feature-grid">
            {(features.length ? features : [
              { id: "f1", icon: "🌿", title: "100% Organic food", subtitle: "100% healthy & fresh food." },
              { id: "f2", icon: "🎧", title: "Great Support 24/7", subtitle: "Instant access to contact." },
              { id: "f3", icon: "⭐", title: "Customer Feedback", subtitle: "Our happy customer." },
              { id: "f4", icon: "🔒", title: "100% Secure Payment", subtitle: "Your money is safe." },
              { id: "f5", icon: "🚚", title: "Free Shipping", subtitle: "Free shipping with discount." },
              { id: "f6", icon: "📦", title: "Fresh Organic Food", subtitle: "100% healthy & fresh food." },
            ]).map((item) => (
              <div className="vf-about-feature" key={item.id}>
                <div className="vf-about-feature-icon">{item.icon}</div>
                <div>
                  <h4>{item.title}</h4>
                  <span>{item.subtitle}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="vf-about-container vf-about-delivery">
        <div className="vf-about-delivery-text">
          <h2>{delivery?.title || "We Delivered, You Enjoy Your Order."}</h2>
          <p>{delivery?.description || "We ensure quick and safe delivery of your groceries right to your doorstep."}</p>
          <ul>
            <li>{delivery?.point_one || "Sed in metus pellentesque."}</li>
            <li>{delivery?.point_two || "Fusce et ex commodo, aliquam nulla efficitur, tempus lorem."}</li>
            <li>{delivery?.point_three || "Maecenas mi turpis fringilla erat varius."}</li>
          </ul>
          <Link to={delivery?.button_link || "/shop"} className="vf-about-green-btn">
            {delivery?.button_text || "Shop Now"} →
          </Link>
        </div>

        <div className="vf-about-delivery-image">
          {delivery?.image_url ? <img src={delivery.image_url} alt={delivery.title} /> : <div className="vf-about-image-placeholder">Upload Delivery Image</div>}
        </div>
      </section>

      <section className="vf-about-container vf-about-team-section">
        <div className="vf-about-section-title">
          <h2>Our Awesome Team</h2>
          <p>Our Vetri Team works with passion and care to bring you fresh products, fast delivery, and a smooth shopping experience every day.</p>
        </div>

        <div className="vf-about-team-grid">
          {team.map((member) => (
            <article className="vf-about-team-card" key={member.id}>
              <div className="vf-about-team-img">
                {member.image_url ? <img src={member.image_url} alt={member.name} /> : <span>No Image</span>}
                {(member.facebook_url || member.twitter_url || member.instagram_url) && (
                  <div className="vf-about-team-socials">
                    {member.facebook_url && <a href={member.facebook_url}>f</a>}
                    {member.twitter_url && <a href={member.twitter_url}>t</a>}
                    {member.instagram_url && <a href={member.instagram_url}>◎</a>}
                  </div>
                )}
              </div>
              <h3>{member.name}</h3>
              <p>{member.role}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="vf-about-container vf-about-testimonials-section">
        <div className="vf-about-testimonial-head">
          <h2>Client Testimonial</h2>
          <div>
            <button type="button">←</button>
            <button type="button" className="active">→</button>
          </div>
        </div>

        <div className="vf-about-testimonial-grid">
          {testimonials.map((item) => (
            <article className="vf-about-testimonial-card" key={item.id}>
              <div className="vf-about-quote">”</div>
              <p>{item.message}</p>
              <div className="vf-about-testimonial-user">
                <div>
                  {item.image_url ? <img src={item.image_url} alt={item.name} /> : <span>{item.name?.charAt(0)}</span>}
                  <div>
                    <h4>{item.name}</h4>
                    <small>{item.role}</small>
                  </div>
                </div>
                <strong>{stars(item.rating)}</strong>
              </div>
            </article>
          ))}
        </div>
      </section>

      {brands.length > 0 && (
        <section className="vf-about-container vf-about-brands">
          {brands.map((brand) => (
            <a href={brand.url || "#"} key={brand.id}>
              {brand.image_url ? <img src={brand.image_url} alt={brand.title} /> : <span>{brand.text_logo || brand.title}</span>}
            </a>
          ))}
        </section>
      )}
    </main>
  );
}

export default About;
