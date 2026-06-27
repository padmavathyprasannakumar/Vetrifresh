export function getAvailableStock(product) {
  if (!product) return 0;

  if (product.stock !== undefined && product.stock !== null && product.stock !== "") {
    const stock = Number(product.stock);
    return Number.isFinite(stock) ? stock : 0;
  }

  if (product.in_stock === false) return 0;
  if (product.in_stock === true) return Number.POSITIVE_INFINITY;

  return Number.POSITIVE_INFINITY;
}

export function isOutOfStock(product, requestedQuantity = 1) {
  const quantity = Number(requestedQuantity || 1);
  const stock = getAvailableStock(product);
  return stock <= 0 || quantity > stock;
}

export function stockMessage(product, requestedQuantity = 1) {
  const stock = getAvailableStock(product);
  const availableText = Number.isFinite(stock) ? stock : 0;

  if (stock <= 0) {
    return "Only 0 item(s) available in stock.";
  }

  if (requestedQuantity > stock) {
    return `Only ${availableText} item(s) available in stock.`;
  }

  return "Requested quantity is not available in stock.";
}

export function apiErrorMessage(error, fallback = "Something went wrong.") {
  const data = error?.response?.data;

  if (!data) return fallback;
  if (typeof data === "string") return data;
  if (data.detail) return data.detail;
  if (Array.isArray(data.non_field_errors) && data.non_field_errors.length) {
    return data.non_field_errors.join(" ");
  }

  const firstValue = Object.values(data)[0];
  if (Array.isArray(firstValue) && firstValue.length) {
    return firstValue.join(" ");
  }
  if (typeof firstValue === "string") return firstValue;

  return fallback;
}
