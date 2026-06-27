import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/client";
import "./Contact.css";

const iconMap = {
  location: "⌖",
  email: "✉",
  phone: "☏",
};

function Contact() {
  const [data, setData] = useState({
    banner: null,
    form_setting: null,
    info_items: [],
  });
  const [form, setForm] = useState({
    name: "",
    email: "",
    phone: "",
    message: "",
  });
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    const loadContact = async () => {
      setLoading(true);
      try {
        const res = await api.get("/contact-page/");
        setData(res.data || {});
      } catch (err) {
        console.log("Contact page API error:", err);
      } finally {
        setLoading(false);
      }
    };

    loadContact();
  }, []);

  const handleChange = (e) => {
    setForm((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSuccess("");
    setError("");
    setSending(true);

    try {
      const res = await api.post("/contact/submit/", form);
      setSuccess(res.data?.message || "Message sent successfully.");
      setForm({ name: "", email: "", phone: "", message: "" });
    } catch (err) {
      const response = err.response?.data;
      if (response && typeof response === "object") {
        const firstKey = Object.keys(response)[0];
        const firstError = Array.isArray(response[firstKey])
          ? response[firstKey][0]
          : response[firstKey];
        setError(firstError || "Unable to send message.");
      } else {
        setError("Unable to send message. Please try again.");
      }
    } finally {
      setSending(false);
    }
  };

  const banner = data.banner;
  const setting = data.form_setting || {};
  const infoItems = data.info_items || [];

  return (
    <main className="vf-contact-page">
      <section
        className="vf-contact-hero"
        style={
          banner?.background_image_url
            ? {
                backgroundImage: `linear-gradient(90deg, rgba(0,0,0,.72), rgba(0,0,0,.18)), url(${banner.background_image_url})`,
              }
            : undefined
        }
      >
        <div className="vf-contact-container">
          <div className="vf-contact-breadcrumb">
            <Link to="/">⌂</Link>
            <span>›</span>
            <span>{banner?.breadcrumb_text || "Contact"}</span>
          </div>
        </div>
      </section>

      <section className="vf-contact-main vf-contact-container">
        {loading ? (
          <div className="vf-contact-loading">Loading contact page...</div>
        ) : (
          <div className="vf-contact-card-wrap">
            <aside
              className="vf-contact-info"
              style={{ backgroundColor: setting.contact_card_bg_color || "#e4f8bf" }}
            >
              {infoItems.length > 0 ? (
                infoItems.map((item) => (
                  <div className="vf-contact-info-item" key={item.id}>
                    <div className="vf-contact-info-icon">
                      {item.custom_icon || iconMap[item.icon_type] || "•"}
                    </div>
                    {item.title && <h3>{item.title}</h3>}
                    <p>{item.line_one}</p>
                    {item.line_two && <p>{item.line_two}</p>}
                  </div>
                ))
              ) : (
                <>
                  <div className="vf-contact-info-item">
                    <div className="vf-contact-info-icon">⌖</div>
                    <p>Soorandi, Tenkasi</p>
                  </div>
                  <div className="vf-contact-info-item">
                    <div className="vf-contact-info-icon">✉</div>
                    <p>Proxy@gmail.com</p>
                    <p>Help.proxy@gmail.com</p>
                  </div>
                  <div className="vf-contact-info-item">
                    <div className="vf-contact-info-icon">☏</div>
                    <p>+91 76709 28721</p>
                  </div>
                </>
              )}
            </aside>

            <section
              className="vf-contact-form-area"
              style={{
                backgroundColor: setting.form_bg_color || "#7ccf8d",
                backgroundImage: setting.form_background_image_url
                  ? `linear-gradient(90deg, rgba(107,201,126,.80), rgba(107,201,126,.62)), url(${setting.form_background_image_url})`
                  : undefined,
              }}
            >
              <h1>{setting.form_title || "Get in Touch"}</h1>

              <form onSubmit={handleSubmit} className="vf-contact-form">
                <div className="vf-contact-row">
                  <input
                    name="name"
                    value={form.name}
                    onChange={handleChange}
                    placeholder={setting.name_placeholder || "Name"}
                    required
                  />
                  <input
                    type="email"
                    name="email"
                    value={form.email}
                    onChange={handleChange}
                    placeholder={setting.email_placeholder || "Email"}
                    required
                  />
                </div>

                <input
                  name="phone"
                  value={form.phone}
                  onChange={handleChange}
                  placeholder={setting.phone_placeholder || "Phone Number"}
                />

                <textarea
                  name="message"
                  value={form.message}
                  onChange={handleChange}
                  placeholder={setting.message_placeholder || "Message"}
                  required
                />

                <button type="submit" disabled={sending}>
                  {sending ? "Sending..." : setting.submit_button_text || "Submit"}
                </button>
              </form>

              {success && <p className="vf-contact-success">{success}</p>}
              {error && <p className="vf-contact-error">{error}</p>}
            </section>
          </div>
        )}
      </section>

      <section className="vf-contact-map">
        {setting.map_embed_url ? (
          <iframe
            title="VetriFresh Location"
            src={setting.map_embed_url}
            style={{ height: `${setting.map_height || 320}px` }}
            loading="lazy"
            referrerPolicy="no-referrer-when-downgrade"
          />
        ) : setting.map_image_url ? (
          <img src={setting.map_image_url} alt="Map" />
        ) : (
          <div className="vf-contact-map-empty">Add map in admin dashboard</div>
        )}
      </section>
    </main>
  );
}

export default Contact;
