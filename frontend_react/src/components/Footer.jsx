import React, { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/client";
import "./Footer.css";

const fallbackFooter = {
  about_title: "About Vetri Fresh",
  about_text:
    "Morbi cursus porttitor enim lobortis molestie. Duis gravida turpis dui, eget bibendum magna congue nec.",
  phone: "7836389098",
  email: "vetrifresh@gmail.com",
  facebook_url: "#",
  twitter_url: "#",
  pinterest_url: "#",
  instagram_url: "#",
  copyright_text: "VetriFresh eCommerce © 2021. All Rights Reserved",
  show_payment_badges: true,
};

const fallbackColumns = [
  {
    id: "my-account",
    title: "My Account",
    links: [
      { id: "my-account-1", title: "My Account", url: "/login" },
      { id: "my-account-2", title: "Order History", url: "/track-order" },
      { id: "my-account-3", title: "Shoping Cart", url: "/cart" },
      { id: "my-account-4", title: "Wishlist", url: "/wishlist" },
      { id: "my-account-5", title: "Settings", url: "/login" },
    ],
  },
  {
    id: "helps",
    title: "Helps",
    links: [
      { id: "helps-1", title: "Contact", url: "/contact" },
      { id: "helps-2", title: "Faqs", url: "#" },
      { id: "helps-3", title: "Terms & Condition", url: "#" },
      { id: "helps-4", title: "Privacy Policy", url: "#" },
    ],
  },
  {
    id: "proxy",
    title: "Proxy",
    links: [
      { id: "proxy-1", title: "About", url: "/about" },
      { id: "proxy-2", title: "Shop", url: "/shop" },
      { id: "proxy-3", title: "Product", url: "/shop" },
      { id: "proxy-4", title: "Products Details", url: "/shop" },
      { id: "proxy-5", title: "Track Order", url: "/track-order" },
    ],
  },
];

const placeholderInstagram = ["🥬", "🥦", "🍅", "🥕", "🍎", "🥒", "🌽", "🍊"];

function FooterLink({ href, children }) {
  const link = href || "#";

  if (link.startsWith("/")) {
    return <Link to={link}>{children}</Link>;
  }

  return (
    <a href={link} target={link === "#" ? undefined : "_blank"} rel={link === "#" ? undefined : "noreferrer"}>
      {children}
    </a>
  );
}

function Footer() {
  const [data, setData] = useState(null);

  useEffect(() => {
    api
      .get("/footer/")
      .then((res) => setData(res.data))
      .catch((err) => console.log("Footer API Error:", err));
  }, []);

  const footer = { ...fallbackFooter, ...(data?.footer || {}) };
  const columns = useMemo(() => {
    const apiColumns = data?.columns || [];
    return apiColumns.length ? apiColumns : fallbackColumns;
  }, [data]);
  const instagramImages = data?.instagram_images || [];
  const paymentBadges = [" Pay", "VISA", "DISCOVER", "MC", "Secure Payment"];

  return (
    <footer className="vf-dynamic-footer">
      <section className="vf-footer-main">
        <div className="vf-footer-pattern" aria-hidden="true" />

        <div className="vf-footer-about">
          <h3>{footer.about_title}</h3>
          <p>{footer.about_text}</p>

          <div className="vf-footer-contact">
            {footer.phone && <a href={`tel:${footer.phone}`}>{footer.phone}</a>}
            {footer.phone && footer.email && <b>or</b>}
            {footer.email && <a href={`mailto:${footer.email}`}>{footer.email}</a>}
          </div>
        </div>

        {columns.map((column) => (
          <div className="vf-footer-column" key={column.id || column.title}>
            <h3>{column.title}</h3>
            {(column.links || []).map((link) => (
              <FooterLink href={link.url} key={link.id || link.title}>
                {link.title}
              </FooterLink>
            ))}
          </div>
        ))}

        <div className="vf-footer-instagram">
          <h3>Instagram</h3>
          <div className="vf-footer-insta-grid">
            {instagramImages.length > 0
              ? instagramImages.slice(0, 8).map((item) => (
                  <a key={item.id} href={item.url || "#"} target="_blank" rel="noreferrer">
                    <img src={item.image_url} alt={item.title || "Instagram"} />
                  </a>
                ))
              : placeholderInstagram.map((item, index) => (
                  <span className="vf-footer-insta-placeholder" key={index}>
                    {item}
                  </span>
                ))}
          </div>
        </div>
      </section>

      <section className="vf-footer-bottom">
        <div className="vf-footer-social">
          {footer.facebook_url && <a href={footer.facebook_url} aria-label="Facebook">f</a>}
          {footer.twitter_url && <a href={footer.twitter_url} aria-label="Twitter">♥</a>}
          {footer.pinterest_url && <a href={footer.pinterest_url} aria-label="Pinterest">p</a>}
          {footer.instagram_url && <a href={footer.instagram_url} aria-label="Instagram">◎</a>}
        </div>

        <p>{footer.copyright_text}</p>

        {footer.show_payment_badges && (
          <div className="vf-payment-badges">
            {paymentBadges.map((badge) => (
              <span key={badge}>{badge}</span>
            ))}
          </div>
        )}
      </section>
    </footer>
  );
}

export default Footer;
