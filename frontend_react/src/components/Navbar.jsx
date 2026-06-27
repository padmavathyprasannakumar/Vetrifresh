import React, { useEffect, useRef, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import api from "../api/client";

function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();
  const navbarRef = useRef(null);

  const [navbarData, setNavbarData] = useState(null);
  const [openDropdownId, setOpenDropdownId] = useState(null);
  const [profileOpen, setProfileOpen] = useState(false);
  const [topDropdown, setTopDropdown] = useState(null);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [searchText, setSearchText] = useState("");
  const [user, setUser] = useState(null);
  const [cartCount, setCartCount] = useState(0);

  const [selectedLanguage, setSelectedLanguage] = useState("Eng");
  const [selectedCurrency, setSelectedCurrency] = useState("INR");

  const languageOptions = ["Eng", "Hindi", "Tamil", "Telugu"];
  const currencyOptions = ["INR", "USD", "EUR"];

  const ChevronIcon = ({ size = 10 }) => (
    <svg width={size} height={Math.round(size * 0.6)} viewBox="0 0 10 6" fill="none">
      <path
        d="M1 1L5 5L9 1"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );

  const closeMenus = () => {
    setOpenDropdownId(null);
    setProfileOpen(false);
    setTopDropdown(null);
    setMobileOpen(false);
  };

  const loadCartCount = async () => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      setCartCount(0);
      return;
    }

    try {
      const res = await api.get("/cart/summary/");
      const countValue = Number(res.data?.count || 0);
      setCartCount(countValue);
    } catch (err) {
      setCartCount(0);
    }
  };

  const loadUser = async () => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      setUser(null);
      setCartCount(0);
      return;
    }

    try {
      const res = await api.get("/auth/me/");
      setUser(res.data);
      localStorage.setItem("user", JSON.stringify(res.data));
      loadCartCount();
    } catch (err) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      localStorage.removeItem("user");
      setUser(null);
      setCartCount(0);
    }
  };

  useEffect(() => {
    api
      .get("/navbar/")
      .then((res) => {
        setNavbarData(res.data);

        if (res.data?.site?.language) {
          setSelectedLanguage(res.data.site.language);
        }

        if (res.data?.site?.currency_code) {
          setSelectedCurrency(res.data.site.currency_code);
        }
      })
      .catch((err) => console.log("Navbar API Error:", err));

    loadUser();

    const handleAuthChange = () => {
      loadUser();
      loadCartCount();
    };

    const handleCartChange = () => {
      loadCartCount();
    };

    const handleStorageChange = () => {
      loadUser();
      loadCartCount();
    };

    const handleWindowFocus = () => {
      loadCartCount();
    };

    const handleClickOutside = (event) => {
      if (navbarRef.current && !navbarRef.current.contains(event.target)) {
        closeMenus();
      }
    };

    window.addEventListener("authChanged", handleAuthChange);
    window.addEventListener("cartChanged", handleCartChange);
    window.addEventListener("storage", handleStorageChange);
    window.addEventListener("focus", handleWindowFocus);
    document.addEventListener("mousedown", handleClickOutside);

    const cartTimer = setInterval(() => {
      loadCartCount();
    }, 3000);

    return () => {
      window.removeEventListener("authChanged", handleAuthChange);
      window.removeEventListener("cartChanged", handleCartChange);
      window.removeEventListener("storage", handleStorageChange);
      window.removeEventListener("focus", handleWindowFocus);
      document.removeEventListener("mousedown", handleClickOutside);
      clearInterval(cartTimer);
    };
  }, []);

  useEffect(() => {
    loadCartCount();
    closeMenus();
  }, [location.pathname, location.search]);

  const handleSearch = (e) => {
    e.preventDefault();

    const cleanSearch = searchText.trim();

    if (cleanSearch) {
      navigate(`/shop?search=${encodeURIComponent(cleanSearch)}`);
      setSearchText("");
      closeMenus();
    }
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user");
    setUser(null);
    setCartCount(0);
    closeMenus();
    window.dispatchEvent(new Event("authChanged"));
    window.dispatchEvent(new Event("cartChanged"));
    navigate("/login");
  };

  if (!navbarData) {
    return (
      <header className="site-header">
        <div className="navbar">
          <h1 className="fallback-logo">VetriFresh</h1>
        </div>
      </header>
    );
  }

  const { site, navbar_links, categories } = navbarData;

  return (
    <header className="site-header" ref={navbarRef}>
      <div className="top-bar">
        <div className="top-left">
          <span>⌖</span>
          <input
            type="text"
            placeholder={site?.location_placeholder || "Pincode"}
          />
        </div>

        <div className="top-right">
          <span className="top-phone">☎ {site?.phone || "+91 93738 34940"}</span>

          <div className="top-select-wrapper">
            <button
              type="button"
              className={`top-select-btn ${topDropdown === "language" ? "top-select-open" : ""}`}
              onClick={() => {
                setTopDropdown(topDropdown === "language" ? null : "language");
                setProfileOpen(false);
                setOpenDropdownId(null);
              }}
            >
              <span>{selectedLanguage}</span>
              <span className="top-select-arrow">
                <ChevronIcon />
              </span>
            </button>

            {topDropdown === "language" && (
              <div className="top-select-menu">
                {languageOptions.map((language) => (
                  <button
                    type="button"
                    key={language}
                    className={`top-select-option ${selectedLanguage === language ? "active" : ""}`}
                    onClick={() => {
                      setSelectedLanguage(language);
                      setTopDropdown(null);
                    }}
                  >
                    {language}
                  </button>
                ))}
              </div>
            )}
          </div>

          <div className="top-select-wrapper">
            <button
              type="button"
              className={`top-select-btn ${topDropdown === "currency" ? "top-select-open" : ""}`}
              onClick={() => {
                setTopDropdown(topDropdown === "currency" ? null : "currency");
                setProfileOpen(false);
                setOpenDropdownId(null);
              }}
            >
              <span>{selectedCurrency}</span>
              <span className="top-select-arrow">
                <ChevronIcon />
              </span>
            </button>

            {topDropdown === "currency" && (
              <div className="top-select-menu">
                {currencyOptions.map((currency) => (
                  <button
                    type="button"
                    key={currency}
                    className={`top-select-option ${selectedCurrency === currency ? "active" : ""}`}
                    onClick={() => {
                      setSelectedCurrency(currency);
                      setTopDropdown(null);
                    }}
                  >
                    {currency}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      <nav className="navbar">
        <Link to="/" className="logo-area" onClick={closeMenus}>
          {site?.logo_url ? (
            <img src={site.logo_url} alt={site.site_name || "VetriFresh"} />
          ) : (
            <h1>{site?.site_name || "VetriFresh"}</h1>
          )}
        </Link>

        <button
          type="button"
          className={`mobile-menu-btn ${mobileOpen ? "active" : ""}`}
          onClick={() => {
            setMobileOpen((old) => !old);
            setOpenDropdownId(null);
            setProfileOpen(false);
            setTopDropdown(null);
          }}
          aria-label="Toggle navigation menu"
        >
          <span></span>
          <span></span>
          <span></span>
        </button>

        <ul className={`nav-menu ${mobileOpen ? "mobile-open" : ""}`}>
          {navbar_links?.map((link) => {
            const isDropdown = link.is_category_dropdown;
            const isOpen = openDropdownId === link.id;

            return (
              <li
                key={link.id}
                className={`nav-item ${isDropdown ? "has-dropdown" : ""} ${isOpen ? "dropdown-open" : ""}`}
              >
                <Link
                  to={link.url}
                  className="nav-link"
                  onMouseEnter={() => {
                    if (isDropdown) {
                      setOpenDropdownId(link.id);
                    }
                  }}
                  onClick={(e) => {
                    if (isDropdown) {
                      e.preventDefault();
                      setOpenDropdownId(isOpen ? null : link.id);
                      return;
                    }

                    closeMenus();
                  }}
                >
                  <span>{link.title}</span>

                  {isDropdown && (
                    <span className="nav-arrow" aria-hidden="true">
                      <ChevronIcon />
                    </span>
                  )}
                </Link>

                {isDropdown && isOpen && (
                  <div
                    className="shop-dropdown"
                    onMouseEnter={() => setOpenDropdownId(link.id)}
                    onMouseDown={(e) => e.stopPropagation()}
                  >
                    <div className="shop-dropdown-inner">
                      {categories?.length > 0 ? (
                        categories.map((category) => (
                          <Link
                            key={category.id}
                            to={`/shop?category=${category.slug || category.id}`}
                            className="shop-dropdown-link"
                            onClick={closeMenus}
                          >
                            <span className="shop-dropdown-img">
                              {category.image_url ? (
                                <img src={category.image_url} alt={category.name} />
                              ) : (
                                <span>{category.name?.charAt(0)}</span>
                              )}
                            </span>

                            <span className="shop-dropdown-name">
                              {category.name}
                            </span>
                          </Link>
                        ))
                      ) : (
                        <span className="empty-dropdown">No categories added</span>
                      )}
                    </div>
                  </div>
                )}
              </li>
            );
          })}
        </ul>

        <div className="nav-actions">
          {site?.show_search_icon && (
            <form onSubmit={handleSearch} className="nav-search">
              <input
                value={searchText}
                onChange={(e) => setSearchText(e.target.value)}
                placeholder="Search"
              />
              <button type="submit" aria-label="Search">⌕</button>
            </form>
          )}

          {site?.show_wishlist_icon && (
            <Link to="/wishlist" className="icon-btn" title="Wishlist" onClick={closeMenus}>
              ♡
            </Link>
          )}

          {site?.show_cart_icon && (
            <Link to="/cart" className="icon-btn cart-icon" title="Cart" onClick={closeMenus}>
              🛍
              <span className="cart-count">{cartCount}</span>
            </Link>
          )}

          {site?.show_user_icon && (
            <div className="profile-wrapper">
              {!user ? (
                <Link to="/login" className="profile-login-btn" title="Login" onClick={closeMenus}>
                  <span className="profile-icon">👤</span>
                </Link>
              ) : (
                <>
                  <button
                    type="button"
                    className={`profile-user-btn ${profileOpen ? "profile-open" : ""}`}
                    onClick={() => {
                      setProfileOpen(!profileOpen);
                      setOpenDropdownId(null);
                      setTopDropdown(null);
                    }}
                  >
                    <span className="profile-avatar">
                      {user.username?.charAt(0)?.toUpperCase() || "U"}
                    </span>

                    <span className="profile-name">
                      {user.first_name || user.username}
                    </span>

                    <span className="profile-arrow" aria-hidden="true">
                      <ChevronIcon />
                    </span>
                  </button>

                  {profileOpen && (
                    <div className="profile-dropdown">
                      <div className="profile-info">
                        <strong>{user.username}</strong>
                        {user.email && <small>{user.email}</small>}
                      </div>

                      <Link to="/wishlist" onClick={closeMenus}>My Wishlist</Link>
                      <Link to="/cart" onClick={closeMenus}>My Cart</Link>
                      <Link to="/track-order" onClick={closeMenus}>Track Order</Link>
                      <Link to="/orders" onClick={closeMenus}>My Orders</Link>

                      <button type="button" onClick={logout}>Logout</button>
                    </div>
                  )}
                </>
              )}
            </div>
          )}
        </div>
      </nav>
    </header>
  );
}

export default Navbar;
