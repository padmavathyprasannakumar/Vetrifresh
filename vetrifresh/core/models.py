from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
from django.utils import timezone


class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.username


class SiteSetting(models.Model):
    site_name = models.CharField(max_length=100, default="VetriFresh")
    logo = models.ImageField(upload_to="site/logo/", blank=True, null=True)

    phone = models.CharField(max_length=25, default="+91 93738 34940")
    currency_symbol = models.CharField(max_length=5, default="₹")
    currency_code = models.CharField(max_length=10, default="INR")
    language = models.CharField(max_length=20, default="Eng")
    location_placeholder = models.CharField(max_length=100, default="Pincode")

    footer_about = models.CharField(
        max_length=255,
        default="Fresh organic products delivered to your home."
    )
    footer_email = models.EmailField(default="support@vetrifresh.com")

    free_shipping_text = models.CharField(
        max_length=150,
        default="Free shipping on all your order"
    )
    hero_footer_text = models.CharField(
        max_length=150,
        default="Freshness Score Guaranteed Quality Products"
    )

    show_search_icon = models.BooleanField(default=True)
    show_wishlist_icon = models.BooleanField(default=True)
    show_cart_icon = models.BooleanField(default=True)
    show_user_icon = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name


class NavbarLink(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200, default="/")
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_category_dropdown = models.BooleanField(default=False)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Navbar Link"
        verbose_name_plural = "Navbar Links"

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)

    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="children"
    )

    is_active = models.BooleanField(default=True)
    show_in_home = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name) or "category"
            slug = base
            number = 1

            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                number += 1
                slug = f"{base}-{number}"

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Banner(models.Model):
    BANNER_TYPES = (
        ("main", "Main Hero Banner"),
        ("side", "Side Banner"),
        ("wide", "Wide Full Banner / Carousel"),
    )

    CONTENT_ANIMATIONS = (
        ("fade-up", "Fade Up"),
        ("slide-left", "Slide Left"),
        ("slide-right", "Slide Right"),
        ("zoom-in", "Zoom In"),
        ("none", "No Animation"),
    )

    BUTTON_ANIMATIONS = (
        ("pulse", "Pulse"),
        ("shine", "Shine"),
        ("bounce", "Bounce"),
        ("none", "No Animation"),
    )

    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=220, blank=True)
    badge = models.CharField(max_length=100, blank=True)
    discount_label = models.CharField(max_length=100, blank=True)

    button_text = models.CharField(max_length=50, default="Shop Now")
    button_link = models.CharField(max_length=200, default="/shop")

    image = models.ImageField(upload_to="banners/", blank=True, null=True)

    banner_type = models.CharField(
        max_length=20,
        choices=BANNER_TYPES,
        default="main"
    )

    bg_color = models.CharField(max_length=20, default="#00B207")
    text_color = models.CharField(max_length=20, default="#FFFFFF")

    content_animation = models.CharField(
        max_length=30,
        choices=CONTENT_ANIMATIONS,
        default="fade-up"
    )

    button_animation = models.CharField(
        max_length=30,
        choices=BUTTON_ANIMATIONS,
        default="pulse"
    )

    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.title


class PromoCard(models.Model):
    PROMO_STYLES = (
        ("dark", "Dark top with image bottom"),
        ("yellow", "Yellow fresh fruit style"),
        ("light", "Light clean card"),
        ("image", "Image focus"),
        ("custom", "Custom colors"),
    )

    IMAGE_POSITIONS = (
        ("bottom-cover", "Bottom image - cover"),
        ("bottom-contain", "Bottom image - contain"),
        ("right-contain", "Right image - contain"),
        ("full-cover", "Full card image"),
    )

    CONTENT_ANIMATIONS = (
        ("fade-up", "Fade Up"),
        ("slide-left", "Slide Left"),
        ("slide-right", "Slide Right"),
        ("zoom-in", "Zoom In"),
        ("none", "No Animation"),
    )

    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=220, blank=True)
    badge = models.CharField(max_length=100, blank=True)

    button_text = models.CharField(max_length=50, default="Shop now")
    button_link = models.CharField(max_length=200, default="/shop")

    image = models.ImageField(upload_to="promo/", blank=True, null=True)

    promo_style = models.CharField(
        max_length=20,
        choices=PROMO_STYLES,
        default="dark",
        help_text="Controls the card layout/style on the home page."
    )
    image_position = models.CharField(
        max_length=20,
        choices=IMAGE_POSITIONS,
        default="bottom-cover",
        help_text="Choose how the promo image should be placed inside the card."
    )

    bg_color = models.CharField(
        max_length=20,
        default="#073B14",
        help_text="Used by Custom style and as fallback for dark/light styles."
    )
    text_color = models.CharField(max_length=20, default="#FFFFFF")
    button_bg_color = models.CharField(max_length=20, default="#FFFFFF")
    button_text_color = models.CharField(max_length=20, default="#00B207")

    image_height_percent = models.PositiveIntegerField(
        default=52,
        help_text="Promo image height in percent for bottom image styles. Example: 52."
    )
    overlay_opacity = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00,
        help_text="Dark overlay over image from 0.00 to 1.00. Use 0 to remove dark background."
    )
    content_animation = models.CharField(
        max_length=30,
        choices=CONTENT_ANIMATIONS,
        default="fade-up"
    )

    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.title


class ServiceFeature(models.Model):
    title = models.CharField(max_length=120)
    subtitle = models.CharField(max_length=200)
    icon = models.CharField(max_length=30, default="🚚")

    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.title


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    sku = models.CharField(max_length=50, blank=True)
    brand = models.CharField(max_length=100, default="VetriFresh")

    image = models.ImageField(upload_to="products/", blank=True, null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    sale_label = models.CharField(max_length=50, blank=True)
    badge = models.CharField(max_length=50, blank=True)

    short_description = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    additional_information = models.TextField(blank=True)

    weight = models.CharField(max_length=50, default="1 kg")
    color = models.CharField(max_length=50, blank=True)
    product_type = models.CharField(max_length=50, default="Organic")

    stock = models.PositiveIntegerField(default=10)

    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.5)
    reviews_count = models.PositiveIntegerField(default=0)

    tags = models.CharField(max_length=250, blank=True)

    is_featured = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name) or "product"
            slug = base
            number = 1

            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                number += 1
                slug = f"{base}-{number}"

            self.slug = slug

        if not self.sku:
            self.sku = (slugify(self.name).upper().replace("-", "") or "PRODUCT")[:20]

        super().save(*args, **kwargs)

    @property
    def in_stock(self):
        return self.stock > 0

    @property
    def discount_percentage(self):
        if self.old_price and self.old_price > self.price:
            return round(((self.old_price - self.price) / self.old_price) * 100)
        return 0

    def __str__(self):
        return self.name


class ProductGallery(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="gallery"
    )

    image = models.ImageField(upload_to="product-gallery/")
    alt_text = models.CharField(max_length=150, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Product Gallery Image"
        verbose_name_plural = "Product Gallery Images"

    def __str__(self):
        return f"{self.product.name} image"


class InstagramImage(models.Model):
    ANIMATION_TYPES = (
        ("fade-up", "Fade Up"),
        ("zoom-in", "Zoom In"),
        ("slide-left", "Slide Left"),
        ("slide-right", "Slide Right"),
        ("flip", "Flip"),
        ("none", "No Animation"),
    )

    title = models.CharField(max_length=100, default="Instagram Image")
    image = models.ImageField(upload_to="instagram/")
    instagram_url = models.URLField(blank=True)

    animation = models.CharField(
        max_length=30,
        choices=ANIMATION_TYPES,
        default="fade-up"
    )
    animation_delay_seconds = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0.00,
        help_text="Delay before this image animates. Example: 0.40 seconds."
    )
    animation_duration_seconds = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0.60,
        help_text="Animation speed in seconds. Example: 0.60."
    )

    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Instagram Image"
        verbose_name_plural = "Instagram Images"

    def __str__(self):
        return self.title


class NewsPost(models.Model):
    title = models.CharField(max_length=180)
    image = models.ImageField(upload_to="news/", blank=True, null=True)

    category = models.CharField(max_length=80, default="Food")
    author = models.CharField(max_length=80, default="Admin")
    comments_count = models.PositiveIntegerField(default=0)

    excerpt = models.TextField(blank=True)
    date_label = models.CharField(max_length=20, default="18 NOV")

    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "News Post"
        verbose_name_plural = "News Posts"

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, default="Customer")
    image = models.ImageField(upload_to="testimonials/", blank=True, null=True)

    message = models.TextField()
    rating = models.PositiveIntegerField(default=5)

    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.name


# -----------------------------
# SHOP PAGE SIDEBAR MODELS
# -----------------------------
class ShopPageBanner(models.Model):
    title = models.CharField(max_length=120, default="Categories")
    breadcrumb_text = models.CharField(max_length=120, default="Categories")
    background_image = models.ImageField(
        upload_to="shop/banner/",
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Shop Page Banner"
        verbose_name_plural = "Shop Page Banner"

    def __str__(self):
        return self.title


class ShopPriceFilter(models.Model):
    label = models.CharField(max_length=100, default="₹0 - ₹500")
    min_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    max_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Shop Price Filter"
        verbose_name_plural = "Shop Price Filters"

    def __str__(self):
        return self.label


class ShopRatingFilter(models.Model):
    label = models.CharField(max_length=100, default="4.0 & up")
    rating_value = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=4.0
    )
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Shop Rating Filter"
        verbose_name_plural = "Shop Rating Filters"

    def __str__(self):
        return self.label


class ShopPopularTag(models.Model):
    title = models.CharField(max_length=60)
    filter_value = models.CharField(
        max_length=80,
        help_text="Example: low fat, vegetarian, fruit"
    )
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Shop Popular Tag"
        verbose_name_plural = "Shop Popular Tags"

    def __str__(self):
        return self.title


class ShopDiscountBanner(models.Model):
    discount_text = models.CharField(
        max_length=80,
        default="79% Discount"
    )
    subtitle = models.CharField(
        max_length=120,
        default="on your first order"
    )
    button_text = models.CharField(
        max_length=50,
        default="Shop Now"
    )
    button_link = models.CharField(
        max_length=200,
        default="/shop"
    )
    image = models.ImageField(
        upload_to="shop/sidebar-discount/",
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Shop Discount Banner"
        verbose_name_plural = "Shop Discount Banner"

    def __str__(self):
        return self.discount_text


class ShopSaleProduct(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="shop_sale_items"
    )
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Shop Sale Product"
        verbose_name_plural = "Shop Sale Products"

    def __str__(self):
        return self.product.name if self.product else "Sale Product"


# -----------------------------
# WISHLIST MODEL
# -----------------------------
class WishlistItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wishlist_items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="wishlist_items"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")
        ordering = ["-created_at"]
        verbose_name = "Wishlist Item"
        verbose_name_plural = "Wishlist Items"

    def __str__(self):
        username = self.user.username if self.user else "No User"
        product_name = self.product.name if self.product else "No Product"
        return f"{username} - {product_name}"


# -----------------------------
# SALE OF THE MONTH BANNER MODEL
# -----------------------------
class SaleOfMonthBanner(models.Model):
    small_title = models.CharField(
        max_length=80,
        default="BEST DEALS"
    )
    title = models.CharField(
        max_length=150,
        default="Sale of the Month"
    )
    discount_text = models.CharField(
        max_length=80,
        default="56% OFF"
    )

    days = models.PositiveIntegerField(default=0)
    hours = models.PositiveIntegerField(default=2)
    minutes = models.PositiveIntegerField(default=18)
    seconds = models.PositiveIntegerField(default=46)

    button_text = models.CharField(
        max_length=50,
        default="Shop Now"
    )
    button_link = models.CharField(
        max_length=200,
        default="/shop"
    )

    image = models.ImageField(
        upload_to="sale-month/",
        blank=True,
        null=True
    )

    bg_color = models.CharField(max_length=20, default="#002603")
    text_color = models.CharField(max_length=20, default="#FFFFFF")

    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Sale of the Month Banner"
        verbose_name_plural = "Sale of the Month Banners"

    def __str__(self):
        return self.title


# -----------------------------
# CART PAGE MODELS
# -----------------------------
class CartPageBanner(models.Model):
    title = models.CharField(
        max_length=120,
        default="My Shopping Cart"
    )
    breadcrumb_text = models.CharField(
        max_length=255,
        default="Home > Category > Vegetables > Shopping cart"
    )
    background_image = models.ImageField(
        upload_to="cart/banner/",
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Cart Page Banner"
        verbose_name_plural = "Cart Page Banner"

    def __str__(self):
        return self.title


class CouponCode(models.Model):
    DISCOUNT_TYPES = (
        ("percentage", "Percentage"),
        ("fixed", "Fixed Amount"),
    )

    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(
        max_length=20,
        choices=DISCOUNT_TYPES,
        default="percentage"
    )
    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    minimum_order_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    maximum_discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["code"]
        verbose_name = "Coupon Code"
        verbose_name_plural = "Coupon Codes"

    def calculate_discount(self, subtotal):
        subtotal = Decimal(str(subtotal or 0))

        if subtotal < self.minimum_order_amount:
            return Decimal("0.00")

        if self.discount_type == "fixed":
            discount = self.discount_value
        else:
            discount = subtotal * (self.discount_value / Decimal("100"))

        if self.maximum_discount_amount:
            discount = min(discount, self.maximum_discount_amount)

        discount = min(discount, subtotal)
        return discount.quantize(Decimal("0.01"))

    def __str__(self):
        return self.code.upper()


class CartRelatedProduct(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_related_items"
    )
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Cart Related Product"
        verbose_name_plural = "Cart Related Products"

    def __str__(self):
        return self.product.name if self.product else "Cart Related Product"




# -----------------------------

# -----------------------------
# ABOUT PAGE MODELS
# -----------------------------
class AboutPageBanner(models.Model):
    title = models.CharField(max_length=120, default="About Us")
    breadcrumb_text = models.CharField(max_length=120, default="About Us")
    background_image = models.ImageField(upload_to="about/banner/", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "About Page Banner"
        verbose_name_plural = "About Page Banner"

    def __str__(self):
        return self.title


class AboutHeroSection(models.Model):
    title = models.CharField(max_length=180, default="100% Trusted Organic Food Store")
    description = models.TextField(
        default="Vetri Fresh is a trusted organic food store delivering fresh, high-quality groceries straight from farm to home."
    )
    image = models.ImageField(upload_to="about/hero/", blank=True, null=True)
    button_text = models.CharField(max_length=50, blank=True, default="")
    button_link = models.CharField(max_length=200, blank=True, default="/shop")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "About Hero Section"
        verbose_name_plural = "About Hero Section"

    def __str__(self):
        return self.title


class AboutFeatureSection(models.Model):
    title = models.CharField(max_length=180, default="100% Trusted Organic Food Store")
    description = models.TextField(
        default="Pellentesque a ante vulputate leo porttitor luctus sed eget eros. Nulla et rhoncus neque."
    )
    image = models.ImageField(upload_to="about/features/", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "About Feature Section"
        verbose_name_plural = "About Feature Section"

    def __str__(self):
        return self.title


class AboutFeatureItem(models.Model):
    icon = models.CharField(max_length=30, default="🌿")
    title = models.CharField(max_length=120, default="100% Organic food")
    subtitle = models.CharField(max_length=180, default="100% healthy & fresh food.")
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "About Feature Item"
        verbose_name_plural = "About Feature Items"

    def __str__(self):
        return self.title


class AboutDeliverySection(models.Model):
    title = models.CharField(max_length=180, default="We Delivered, You Enjoy Your Order.")
    description = models.TextField(
        default="At Vetri Fresh, we ensure quick and safe delivery of your groceries right to your doorstep."
    )
    image = models.ImageField(upload_to="about/delivery/", blank=True, null=True)
    point_one = models.CharField(max_length=160, default="Sed in metus pellentesque.")
    point_two = models.CharField(max_length=160, default="Fusce et ex commodo, aliquam nulla efficitur, tempus lorem.")
    point_three = models.CharField(max_length=160, default="Maecenas mi turpis fringilla erat varius.")
    button_text = models.CharField(max_length=50, default="Shop Now")
    button_link = models.CharField(max_length=200, default="/shop")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "About Delivery Section"
        verbose_name_plural = "About Delivery Section"

    def __str__(self):
        return self.title


class AboutTeamMember(models.Model):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120, default="Team Member")
    image = models.ImageField(upload_to="about/team/", blank=True, null=True)
    facebook_url = models.URLField(blank=True, default="")
    twitter_url = models.URLField(blank=True, default="")
    instagram_url = models.URLField(blank=True, default="")
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "About Team Member"
        verbose_name_plural = "About Team Members"

    def __str__(self):
        return self.name


class AboutTestimonial(models.Model):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120, default="Customer")
    image = models.ImageField(upload_to="about/testimonials/", blank=True, null=True)
    message = models.TextField()
    rating = models.PositiveIntegerField(default=5)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "About Testimonial"
        verbose_name_plural = "About Testimonials"

    def __str__(self):
        return self.name


class AboutBrandLogo(models.Model):
    title = models.CharField(max_length=120, default="Brand Logo")
    image = models.ImageField(upload_to="about/brands/", blank=True, null=True)
    text_logo = models.CharField(max_length=80, blank=True, default="")
    url = models.URLField(blank=True, default="")
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "About Brand Logo"
        verbose_name_plural = "About Brand Logos"

    def __str__(self):
        return self.title



# -----------------------------
# CONTACT PAGE MODELS
# -----------------------------
class ContactPageBanner(models.Model):
    title = models.CharField(max_length=120, default="Contact")
    breadcrumb_text = models.CharField(max_length=120, default="Contact")
    background_image = models.ImageField(
        upload_to="contact/banner/",
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Contact Page Banner"
        verbose_name_plural = "Contact Page Banner"

    def __str__(self):
        return self.title


class ContactInfoItem(models.Model):
    ICON_CHOICES = (
        ("location", "Location"),
        ("email", "Email"),
        ("phone", "Phone"),
        ("custom", "Custom"),
    )

    icon_type = models.CharField(
        max_length=20,
        choices=ICON_CHOICES,
        default="location"
    )
    custom_icon = models.CharField(max_length=30, blank=True, default="")
    title = models.CharField(max_length=120, blank=True, default="")
    line_one = models.CharField(max_length=180)
    line_two = models.CharField(max_length=180, blank=True, default="")
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Contact Info Item"
        verbose_name_plural = "Contact Info Items"

    def __str__(self):
        return self.title or self.line_one


class ContactFormSetting(models.Model):
    form_title = models.CharField(max_length=120, default="Get in Touch")

    name_placeholder = models.CharField(max_length=80, default="Name")
    email_placeholder = models.CharField(max_length=80, default="Email")
    phone_placeholder = models.CharField(max_length=80, default="Phone Number")
    message_placeholder = models.CharField(max_length=80, default="Message")
    submit_button_text = models.CharField(max_length=50, default="Submit")

    recipient_email = models.EmailField(default="padmavathyparasanna4@gmail.com")
    email_subject_prefix = models.CharField(
        max_length=120,
        default="VetriFresh Contact Message"
    )

    form_background_image = models.ImageField(
        upload_to="contact/form-bg/",
        blank=True,
        null=True
    )
    form_bg_color = models.CharField(max_length=20, default="#7ccf8d")
    contact_card_bg_color = models.CharField(max_length=20, default="#e4f8bf")

    map_embed_url = models.TextField(
        blank=True,
        default="https://www.google.com/maps?q=Soorandi,Tenkasi&output=embed",
        help_text=(
            "Paste Google Maps embed URL or use a query URL like "
            "https://www.google.com/maps?q=Tenkasi&output=embed"
        )
    )
    map_image = models.ImageField(
        upload_to="contact/map/",
        blank=True,
        null=True
    )
    map_height = models.PositiveIntegerField(default=320)

    success_message = models.CharField(
        max_length=180,
        default="Message sent successfully."
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Contact Form Setting"
        verbose_name_plural = "Contact Form Setting"

    def __str__(self):
        return self.form_title


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True, default="")
    message = models.TextField()

    is_read = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)
    email_error = models.TextField(blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.name} - {self.email}"

# BLOG PAGE MODELS
# -----------------------------
class BlogPageBanner(models.Model):
    title = models.CharField(max_length=120, default="Blog")
    breadcrumb_text = models.CharField(max_length=120, default="Blog")
    background_image = models.ImageField(
        upload_to="blog/banner/",
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Blog Page Banner"
        verbose_name_plural = "Blog Page Banner"

    def __str__(self):
        return self.title


class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name) or "blog-category"
            slug = base
            number = 1

            while BlogCategory.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                number += 1
                slug = f"{base}-{number}"

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.SET_NULL,
        related_name="posts",
        blank=True,
        null=True
    )
    title = models.CharField(max_length=220)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to="blog/posts/", blank=True, null=True)
    excerpt = models.TextField(blank=True)
    author_name = models.CharField(max_length=80, default="Admin")
    date_label = models.CharField(max_length=30, default="18 NOV")
    comments_count = models.PositiveIntegerField(default=0)
    is_video = models.BooleanField(default=False)
    video_url = models.URLField(blank=True, default="")
    read_more_text = models.CharField(max_length=40, default="Read More")
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "-created_at"]
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title) or "blog-post"
            slug = base
            number = 1

            while BlogPost.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                number += 1
                slug = f"{base}-{number}"

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class BlogPopularTag(models.Model):
    title = models.CharField(max_length=60)
    filter_value = models.CharField(
        max_length=80,
        help_text="Example: food, healthy, organic"
    )
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Blog Popular Tag"
        verbose_name_plural = "Blog Popular Tags"

    def __str__(self):
        return self.title


class BlogDiscountBanner(models.Model):
    discount_text = models.CharField(max_length=80, default="79% Discount")
    subtitle = models.CharField(max_length=120, default="on your first order")
    button_text = models.CharField(max_length=50, default="Shop Now")
    button_link = models.CharField(max_length=200, default="/shop")
    image = models.ImageField(
        upload_to="blog/sidebar-discount/",
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Blog Discount Banner"
        verbose_name_plural = "Blog Discount Banner"

    def __str__(self):
        return self.discount_text


class BlogRecentPost(models.Model):
    post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name="recent_items"
    )
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Blog Recently Added"
        verbose_name_plural = "Blog Recently Added"

    def __str__(self):
        return self.post.title if self.post else "Recent Blog Post"


class BlogGalleryImage(models.Model):
    title = models.CharField(max_length=100, default="Gallery Image")
    image = models.ImageField(upload_to="blog/gallery/")
    url = models.CharField(max_length=200, blank=True, default="")
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Blog Gallery Image"
        verbose_name_plural = "Blog Gallery Images"

    def __str__(self):
        return self.title


class BlogBrandLogo(models.Model):
    title = models.CharField(max_length=100, default="Brand Logo")
    image = models.ImageField(upload_to="blog/brands/", blank=True, null=True)
    text_logo = models.CharField(max_length=100, blank=True, default="")
    url = models.CharField(max_length=200, blank=True, default="")
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Blog Brand Logo"
        verbose_name_plural = "Blog Brand Logos"

    def __str__(self):
        return self.title

# -----------------------------
# NEWSLETTER + FOOTER MODELS
# -----------------------------
class NewsletterSection(models.Model):
    title = models.CharField(
        max_length=150,
        default="Subscribe our Newsletter"
    )
    subtitle = models.CharField(
        max_length=200,
        default="Get the latest updates by subscribing"
    )
    placeholder_text = models.CharField(
        max_length=100,
        default="Your email address"
    )
    button_text = models.CharField(
        max_length=50,
        default="Subscribe"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Newsletter Section"
        verbose_name_plural = "Newsletter Section"

    def __str__(self):
        return self.title


class FooterSetting(models.Model):
    logo = models.ImageField(
        upload_to="footer/logo/",
        blank=True,
        null=True
    )
    logo_text = models.CharField(
        max_length=100,
        default="VetriFresh"
    )

    about_title = models.CharField(
        max_length=120,
        default="About Vetri Fresh"
    )
    about_text = models.TextField(
        default="Morbi cursus porttitor enim lobortis molestie. Duis gravida turpis dui, eget bibendum magna congue nec."
    )

    phone = models.CharField(
        max_length=30,
        default="7836389098"
    )
    email = models.EmailField(
        default="vetrifresh@gmail.com"
    )

    facebook_url = models.URLField(blank=True, default="")
    twitter_url = models.URLField(blank=True, default="")
    pinterest_url = models.URLField(blank=True, default="")
    instagram_url = models.URLField(blank=True, default="")

    copyright_text = models.CharField(
        max_length=200,
        default="VetriFresh eCommerce © 2021. All Rights Reserved"
    )

    show_payment_badges = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Footer Setting"
        verbose_name_plural = "Footer Setting"

    def __str__(self):
        return self.logo_text


class FooterColumn(models.Model):
    title = models.CharField(max_length=100)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Footer Column"
        verbose_name_plural = "Footer Columns"

    def __str__(self):
        return self.title


class FooterLink(models.Model):
    column = models.ForeignKey(
        FooterColumn,
        on_delete=models.CASCADE,
        related_name="links"
    )
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200, default="#")
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Footer Link"
        verbose_name_plural = "Footer Links"

    def __str__(self):
        return self.title


class FooterInstagramImage(models.Model):
    title = models.CharField(
        max_length=100,
        default="Footer Instagram"
    )
    image = models.ImageField(upload_to="footer/instagram/")
    url = models.URLField(blank=True, default="")
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Footer Instagram Image"
        verbose_name_plural = "Footer Instagram Images"

    def __str__(self):
        return self.title


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Newsletter Subscriber"
        verbose_name_plural = "Newsletter Subscribers"

    def __str__(self):
        return self.email


# -----------------------------
# CHECKOUT PAYMENT METHOD MODELS
# -----------------------------
class PaymentMethod(models.Model):
    METHOD_TYPES = (
        ("Cash on Delivery", "Cash on Delivery"),
        ("Cashfree", "Cashfree Payment Gateway"),
        ("UPI", "UPI"),
        ("Card", "Card Payment"),
        ("Net Banking", "Net Banking"),
    )

    title = models.CharField(max_length=80, default="Cash on Delivery")
    method_type = models.CharField(
        max_length=50,
        choices=METHOD_TYPES,
        default="Cash on Delivery"
    )
    description = models.CharField(max_length=180, blank=True, default="")
    icon = models.CharField(max_length=30, blank=True, default="")
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Checkout Payment Method"
        verbose_name_plural = "Checkout Payment Methods"

    def __str__(self):
        return self.title


class CartItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )

    quantity = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "product")
        ordering = ["-created_at"]

    @property
    def item_total(self):
        if not self.product or self.product.price is None or self.quantity is None:
            return Decimal("0.00")
        return self.product.price * self.quantity

    def __str__(self):
        product_name = self.product.name if self.product else "No Product"
        username = self.user.username if self.user else "No User"
        return f"{username} - {product_name}"


class Order(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("packed", "Packed"),
        ("shipped", "Shipped"),
        ("out_for_delivery", "Out for Delivery"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    )

    PAYMENT_CHOICES = (
        ("Cash on Delivery", "Cash on Delivery"),
        ("Cashfree", "Cashfree Payment Gateway"),
        ("UPI", "UPI"),
        ("Card", "Card"),
        ("Net Banking", "Net Banking"),
    )

    PAYMENT_STATUS_CHOICES = (
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
        ("cancelled", "Cancelled"),
        ("refunded", "Refunded"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    order_number = models.CharField(
        max_length=40,
        unique=True,
        blank=True,
        null=True
    )

    invoice_number = models.CharField(
        max_length=40,
        unique=True,
        blank=True,
        null=True
    )

    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)

    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10)

    payment_method = models.CharField(
        max_length=50,
        choices=PAYMENT_CHOICES,
        default="Cash on Delivery"
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="pending"
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="pending"
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    shipping_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    cashfree_order_id = models.CharField(
        max_length=120,
        unique=True,
        blank=True,
        null=True
    )
    cashfree_payment_session_id = models.TextField(blank=True, default="")
    cashfree_status = models.CharField(max_length=80, blank=True, default="")

    tracking_status = models.CharField(
        max_length=80,
        default="Order Placed"
    )
    tracking_message = models.CharField(
        max_length=255,
        default="We will knock your door steps shortly."
    )

    order_note = models.TextField(blank=True)
    delivered_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        updates = []

        if not self.order_number:
            self.order_number = f"VF{timezone.now().strftime('%Y%m%d')}{self.id:05d}"
            updates.append("order_number")

        if not self.invoice_number:
            self.invoice_number = f"INV{timezone.now().strftime('%Y%m%d')}{self.id:05d}"
            updates.append("invoice_number")

        if updates:
            super().save(update_fields=updates)

    def __str__(self):
        username = self.user.username if self.user else "Guest"
        return f"{self.order_number or 'Order'} - {username}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    product_name = models.CharField(
        max_length=200,
        blank=True,
        default=""
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        default=0
    )
    quantity = models.PositiveIntegerField(default=1)

    @property
    def item_total(self):
        if self.price is None or self.quantity is None:
            return Decimal("0.00")
        return self.price * self.quantity

    def __str__(self):
        return self.product_name or "Order Item"