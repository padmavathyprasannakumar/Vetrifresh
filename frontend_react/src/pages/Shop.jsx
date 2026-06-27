import React, { useEffect, useMemo, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import api from "../api/client";
import ProductCard from "../components/ProductCard";
import "./Shop.css";

const DEFAULT_SORT_OPTIONS = [
  { value: "latest", label: "Latest" },
  { value: "price_low", label: "Price: Low to High" },
  { value: "price_high", label: "Price: High to Low" },
  { value: "name", label: "Name" },
];

const PRODUCTS_PER_PAGE = 9;

function getPageNumber(value) {
  const page = Number(value || 1);
  return Number.isFinite(page) && page > 0 ? Math.floor(page) : 1;
}

function getPaginationItems(currentPage, totalPages) {
  if (totalPages <= 7) {
    return Array.from({ length: totalPages }, (_, index) => index + 1);
  }

  const pages = new Set([1, totalPages, currentPage]);

  if (currentPage > 1) pages.add(currentPage - 1);
  if (currentPage < totalPages) pages.add(currentPage + 1);
  if (currentPage <= 3) pages.add(2);
  if (currentPage >= totalPages - 2) pages.add(totalPages - 1);

  const sorted = Array.from(pages).sort((a, b) => a - b);
  const items = [];

  sorted.forEach((page, index) => {
    if (index > 0 && page - sorted[index - 1] > 1) {
      items.push(`ellipsis-${sorted[index - 1]}-${page}`);
    }

    items.push(page);
  });

  return items;
}

function FilterArrow({ open }) {
  return (
    <span className={`vf-shop-arrow-icon2 ${open ? "open" : ""}`}>
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
  );
}

function Shop() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  const [openBox, setOpenBox] = useState({
    categories: true,
    price: false,
    rating: true,
    tags: true,
    discount: true,
    sale: true,
  });

  const category = searchParams.get("category") || "";
  const priceFilter = searchParams.get("price_filter") || "";
  const ratingFilter = searchParams.get("rating_filter") || "";
  const minPrice = searchParams.get("min_price") || "";
  const maxPrice = searchParams.get("max_price") || "";
  const rating = searchParams.get("rating") || "";
  const tag = searchParams.get("tag") || "";
  const search = searchParams.get("search") || "";
  const sort = searchParams.get("sort") || "latest";
  const page = getPageNumber(searchParams.get("page"));

  const paramsObject = useMemo(() => {
    const params = {};

    if (category) params.category = category;
    if (priceFilter) params.price_filter = priceFilter;
    if (ratingFilter) params.rating_filter = ratingFilter;
    if (minPrice) params.min_price = minPrice;
    if (maxPrice) params.max_price = maxPrice;
    if (rating) params.rating = rating;
    if (tag) params.tag = tag;
    if (search) params.search = search;
    if (sort) params.sort = sort;
    params.page = page;
    params.page_size = PRODUCTS_PER_PAGE;

    return params;
  }, [category, priceFilter, ratingFilter, minPrice, maxPrice, rating, tag, search, sort, page]);

  useEffect(() => {
    setLoading(true);

    api
      .get("/shop-page/", { params: paramsObject })
      .then((res) => setData(res.data))
      .catch((err) => console.log("Shop page API error:", err))
      .finally(() => setLoading(false));
  }, [paramsObject]);

  const toggleBox = (boxName) => {
    setOpenBox((old) => ({
      ...old,
      [boxName]: !old[boxName],
    }));
  };

  const updateFilter = (key, value) => {
    const next = new URLSearchParams(searchParams);

    if (value) {
      next.set(key, value);
    } else {
      next.delete(key);
    }

    if (key !== "page") {
      next.delete("page");
    }

    setSearchParams(next);
  };

  const updateCategory = (value) => {
    const next = new URLSearchParams(searchParams);

    if (value) {
      next.set("category", value);
    } else {
      next.delete("category");
    }

    next.delete("page");
    setSearchParams(next);
  };

  const updatePriceFilter = (item) => {
    const next = new URLSearchParams(searchParams);

    if (priceFilter === String(item.id)) {
      next.delete("price_filter");
      next.delete("min_price");
      next.delete("max_price");
    } else {
      next.set("price_filter", String(item.id));
      next.set("min_price", item.min_price);

      if (item.max_price) {
        next.set("max_price", item.max_price);
      } else {
        next.delete("max_price");
      }
    }

    next.delete("page");
    setSearchParams(next);
  };

  const updateRatingFilter = (item) => {
    const next = new URLSearchParams(searchParams);

    if (ratingFilter === String(item.id)) {
      next.delete("rating_filter");
      next.delete("rating");
    } else {
      next.set("rating_filter", String(item.id));
      next.set("rating", item.rating_value);
    }

    next.delete("page");
    setSearchParams(next);
  };

  const clearFilters = () => {
    setSearchParams({ sort });
  };

  const clearSearch = () => {
    const next = new URLSearchParams(searchParams);
    next.delete("search");
    next.delete("page");
    setSearchParams(next);
  };

  const goToPage = (nextPage) => {
    const safePage = Math.max(1, Math.min(nextPage, totalPages));
    const next = new URLSearchParams(searchParams);

    if (safePage <= 1) {
      next.delete("page");
    } else {
      next.set("page", String(safePage));
    }

    setSearchParams(next);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const pageBanner = data?.page_banner || data?.banner;
  const selectedCategory = data?.selected_category || data?.current_category;
  const categories = data?.categories || [];
  const priceFilters = data?.price_filters || [];
  const ratingFilters = data?.rating_filters || [];
  const popularTags = data?.popular_tags || [];
  const discountBanner = data?.discount_banner;
  const saleProducts = data?.sale_products || [];
  const products = data?.products || [];
  const sortOptions = data?.sort_options?.length ? data.sort_options : DEFAULT_SORT_OPTIONS;
  const totalCount = data?.total_count ?? data?.total_products ?? products.length;
  const totalPages = Math.max(1, data?.pagination?.total_pages || Math.ceil(totalCount / PRODUCTS_PER_PAGE));
  const currentPage = Math.min(page, totalPages);
  const paginationItems = getPaginationItems(currentPage, totalPages);

  return (
    <main className="vf-shop-page2">
      <section
        className="vf-shop-hero2"
        style={
          pageBanner?.background_image_url
            ? {
                backgroundImage: `linear-gradient(rgba(0,0,0,.45), rgba(0,0,0,.45)), url(${pageBanner.background_image_url})`,
              }
            : undefined
        }
      >
        <div className="vf-shop-hero-inner2">
          <span>⌂</span>
          <Link to="/">Home</Link>
          <span>›</span>
          <Link to="/shop">Categories</Link>
          {selectedCategory && (
            <>
              <span>›</span>
              <strong>{selectedCategory.name}</strong>
            </>
          )}
        </div>
      </section>

      <section className="vf-shop-layout2">
        <aside className="vf-shop-sidebar2">
          <div className="vf-filter-box2">
            <div className="vf-filter-title2">
              <h3>All Categories</h3>
              <button
                type="button"
                className="vf-shop-arrow-btn2"
                onClick={() => toggleBox("categories")}
                aria-label={openBox.categories ? "Collapse section" : "Expand section"}
              >
                <FilterArrow open={openBox.categories} />
              </button>
            </div>

            {openBox.categories && (
              <div className="vf-filter-content2">
                <label className="vf-radio-row2">
                  <input
                    type="radio"
                    checked={!category}
                    onChange={() => updateCategory("")}
                  />
                  <span>All Products</span>
                </label>

                {categories.map((item) => (
                  <label className="vf-radio-row2" key={item.id}>
                    <input
                      type="radio"
                      checked={category === item.slug}
                      onChange={() => updateCategory(item.slug)}
                    />
                    <span>
                      {item.name} <small>({item.product_count})</small>
                    </span>
                  </label>
                ))}
              </div>
            )}
          </div>

          <div className="vf-filter-box2">
            <div className="vf-filter-title2">
              <h3>Price</h3>
              <button
                type="button"
                className="vf-shop-arrow-btn2"
                onClick={() => toggleBox("price")}
                aria-label={openBox.price ? "Collapse section" : "Expand section"}
              >
                <FilterArrow open={openBox.price} />
              </button>
            </div>

            {openBox.price && (
              <div className="vf-filter-content2">
                {priceFilters.map((item) => (
                  <label className="vf-radio-row2" key={item.id}>
                    <input
                      type="radio"
                      checked={priceFilter === String(item.id)}
                      onChange={() => updatePriceFilter(item)}
                    />
                    <span>{item.label}</span>
                  </label>
                ))}
              </div>
            )}
          </div>

          <div className="vf-filter-box2">
            <div className="vf-filter-title2">
              <h3>Rating</h3>
              <button
                type="button"
                className="vf-shop-arrow-btn2"
                onClick={() => toggleBox("rating")}
                aria-label={openBox.rating ? "Collapse section" : "Expand section"}
              >
                <FilterArrow open={openBox.rating} />
              </button>
            </div>

            {openBox.rating && (
              <div className="vf-filter-content2">
                {ratingFilters.map((item) => (
                  <label className="vf-rating-row2" key={item.id}>
                    <input
                      type="checkbox"
                      checked={ratingFilter === String(item.id)}
                      onChange={() => updateRatingFilter(item)}
                    />
                    <span className="vf-stars2">★★★★★</span>
                    <small>{item.label}</small>
                  </label>
                ))}
              </div>
            )}
          </div>

          <div className="vf-filter-box2">
            <div className="vf-filter-title2">
              <h3>Popular Tag</h3>
              <button
                type="button"
                className="vf-shop-arrow-btn2"
                onClick={() => toggleBox("tags")}
                aria-label={openBox.tags ? "Collapse section" : "Expand section"}
              >
                <FilterArrow open={openBox.tags} />
              </button>
            </div>

            {openBox.tags && (
              <div className="vf-tags2">
                {popularTags.map((item) => (
                  <button
                    type="button"
                    key={item.id}
                    className={tag === item.filter_value ? "active" : ""}
                    onClick={() => updateFilter("tag", tag === item.filter_value ? "" : item.filter_value)}
                  >
                    {item.title}
                  </button>
                ))}
              </div>
            )}
          </div>

          {discountBanner && (
            <div className="vf-sidebar-discount2">
              {discountBanner.image_url && (
                <img src={discountBanner.image_url} alt={discountBanner.discount_text} />
              )}
              <div className="vf-discount-text2">
                <h3>{discountBanner.discount_text}</h3>
                <p>{discountBanner.subtitle}</p>
                <Link to={discountBanner.button_link || "/shop"}>
                  {discountBanner.button_text} →
                </Link>
              </div>
            </div>
          )}

          <div className="vf-filter-box2 vf-sale-box2">
            <div className="vf-filter-title2">
              <h3>Sale Products</h3>
              <button
                type="button"
                className="vf-shop-arrow-btn2"
                onClick={() => toggleBox("sale")}
                aria-label={openBox.sale ? "Collapse section" : "Expand section"}
              >
                <FilterArrow open={openBox.sale} />
              </button>
            </div>

            {openBox.sale && (
              <div className="vf-filter-content2">
                {saleProducts.map((item) => {
                  const product = item.product;
                  if (!product) return null;

                  return (
                    <Link
                      to={`/product/${product.id}`}
                      className="vf-sale-product2"
                      key={item.id}
                    >
                      <img src={product.image_url} alt={product.name} />
                      <div>
                        <h4>{product.name}</h4>
                        <p>
                          ₹{product.price}
                          {product.old_price && <del>₹{product.old_price}</del>}
                        </p>
                        <span>★★★★★</span>
                      </div>
                    </Link>
                  );
                })}
              </div>
            )}
          </div>

          <button type="button" className="vf-clear-filter2" onClick={clearFilters}>
            Clear Filters
          </button>
        </aside>

        <section className="vf-shop-products2">
          <div className="vf-shop-topbar2">
            <div>
              <span>Sort by:</span>
              <select value={sort} onChange={(e) => updateFilter("sort", e.target.value)}>
                {sortOptions.map((item) => (
                  <option value={item.value} key={item.value}>
                    {item.label}
                  </option>
                ))}
              </select>
            </div>

            <p>{totalCount} Products Found</p>
          </div>

          {search && (
            <div className="vf-shop-search-result2">
              <span>Search result for: <strong>{search}</strong></span>
              <button type="button" onClick={clearSearch}>Clear Search</button>
            </div>
          )}

          {loading ? (
            <div className="vf-shop-loading2">Loading products...</div>
          ) : products.length === 0 ? (
            <div className="vf-shop-empty2">No products found.</div>
          ) : (
            <div className="vf-products-grid2">
              {products.map((product) => (
                <ProductCard product={product} key={product.id} />
              ))}
            </div>
          )}

          {!loading && totalPages > 1 && (
            <div className="vf-shop-pagination2">
              <button
                type="button"
                onClick={() => goToPage(currentPage - 1)}
                disabled={currentPage <= 1}
                aria-label="Previous page"
              >
                ‹
              </button>

              {paginationItems.map((item) =>
                typeof item === "number" ? (
                  <button
                    type="button"
                    key={item}
                    className={item === currentPage ? "active" : ""}
                    onClick={() => goToPage(item)}
                    aria-label={`Page ${item}`}
                  >
                    {item}
                  </button>
                ) : (
                  <span className="vf-pagination-dots2" key={item}>
                    ...
                  </span>
                )
              )}

              <button
                type="button"
                onClick={() => goToPage(currentPage + 1)}
                disabled={currentPage >= totalPages}
                aria-label="Next page"
              >
                ›
              </button>
            </div>
          )}
        </section>
      </section>
    </main>
  );
}

export default Shop;
