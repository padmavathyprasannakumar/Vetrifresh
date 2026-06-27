from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import (
    AboutBrandLogo,
    AboutDeliverySection,
    AboutFeatureItem,
    AboutFeatureSection,
    AboutHeroSection,
    AboutPageBanner,
    AboutTeamMember,
    AboutTestimonial,
    Banner,
    BlogBrandLogo,
    BlogCategory,
    BlogDiscountBanner,
    BlogGalleryImage,
    BlogPageBanner,
    BlogPopularTag,
    BlogPost,
    BlogRecentPost,
    CartItem,
    CartPageBanner,
    CartRelatedProduct,
    CouponCode,
    Category,
    ContactFormSetting,
    ContactInfoItem,
    ContactMessage,
    ContactPageBanner,
    FooterColumn,
    FooterInstagramImage,
    FooterLink,
    FooterSetting,
    InstagramImage,
    NavbarLink,
    NewsPost,
    NewsletterSection,
    NewsletterSubscriber,
    Order,
    OrderItem,
    PaymentMethod,
    Product,
    ProductGallery,
    PromoCard,
    SaleOfMonthBanner,
    ServiceFeature,
    ShopDiscountBanner,
    ShopPageBanner,
    ShopPopularTag,
    ShopPriceFilter,
    ShopRatingFilter,
    ShopSaleProduct,
    SiteSetting,
    Testimonial,
    User,
    WishlistItem,
)


def preview_image(obj, field="image", height=70, width=100):
    img = getattr(obj, field, None)

    if img:
        return format_html(
            '<img src="{}" style="height:{}px;width:{}px;object-fit:contain;border-radius:6px;" />',
            img.url,
            height,
            width,
        )

    return "No image"


# -----------------------------
# USER ADMIN
# -----------------------------
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Extra Information", {
            "fields": ("phone", "address")
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Extra Information", {
            "fields": ("phone", "address")
        }),
    )

    list_display = (
        "username",
        "email",
        "phone",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "username",
        "email",
        "phone",
    )


# -----------------------------
# SITE SETTING ADMIN
# -----------------------------
@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = (
        "site_name",
        "logo_preview",
        "phone",
        "currency_symbol",
        "currency_code",
        "language",
    )

    readonly_fields = (
        "logo_preview",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Logo & Website Name", {
            "fields": (
                "site_name",
                "logo",
                "logo_preview",
            )
        }),
        ("Top Bar Details", {
            "fields": (
                "phone",
                "location_placeholder",
                "language",
                "currency_symbol",
                "currency_code",
            )
        }),
        ("Navbar Icons", {
            "fields": (
                "show_search_icon",
                "show_wishlist_icon",
                "show_cart_icon",
                "show_user_icon",
            )
        }),
        ("Footer Details", {
            "fields": (
                "footer_about",
                "footer_email",
            )
        }),
        ("Extra Homepage Text", {
            "fields": (
                "free_shipping_text",
                "hero_footer_text",
            )
        }),
        ("Date Information", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    def logo_preview(self, obj):
        return preview_image(obj, "logo", 55, 180)

    logo_preview.short_description = "Logo Preview"


# -----------------------------
# NAVBAR LINK ADMIN
# -----------------------------
@admin.register(NavbarLink)
class NavbarLinkAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "url",
        "sort_order",
        "is_category_dropdown",
        "is_active",
    )

    list_editable = (
        "url",
        "sort_order",
        "is_category_dropdown",
        "is_active",
    )

    search_fields = (
        "title",
        "url",
    )

    list_filter = (
        "is_active",
        "is_category_dropdown",
    )

    ordering = (
        "sort_order",
        "id",
    )

    fieldsets = (
        ("Navbar Menu Details", {
            "fields": (
                "title",
                "url",
                "sort_order",
            )
        }),
        ("Dropdown Settings", {
            "fields": (
                "is_category_dropdown",
                "is_active",
            )
        }),
    )


# -----------------------------
# CATEGORY ADMIN
# -----------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "parent",
        "image_preview",
        "show_in_home",
        "is_active",
        "sort_order",
    )

    list_editable = (
        "show_in_home",
        "is_active",
        "sort_order",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    search_fields = (
        "name",
        "slug",
    )

    list_filter = (
        "is_active",
        "show_in_home",
        "parent",
    )

    readonly_fields = (
        "image_preview",
    )

    fieldsets = (
        ("Category Details", {
            "fields": (
                "name",
                "slug",
                "parent",
                "image",
                "image_preview",
            )
        }),
        ("Display Settings", {
            "fields": (
                "show_in_home",
                "is_active",
                "sort_order",
            )
        }),
    )

    def image_preview(self, obj):
        return preview_image(obj, "image", 70, 90)

    image_preview.short_description = "Image Preview"


# -----------------------------
# PRODUCT GALLERY INLINE
# -----------------------------
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

    fields = (
        "image",
        "image_preview",
        "alt_text",
        "sort_order",
    )

    readonly_fields = (
        "image_preview",
    )

    def image_preview(self, obj):
        return preview_image(obj, "image", 60, 70)

    image_preview.short_description = "Preview"


# -----------------------------
# PRODUCT ADMIN
# -----------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "product_image",
        "category",
        "price",
        "old_price",
        "discount_percentage",
        "stock",
        "is_featured",
        "is_popular",
        "is_active",
    )

    list_editable = (
        "price",
        "old_price",
        "stock",
        "is_featured",
        "is_popular",
        "is_active",
    )

    list_filter = (
        "category",
        "is_featured",
        "is_popular",
        "is_active",
        "product_type",
    )

    search_fields = (
        "name",
        "slug",
        "sku",
        "brand",
        "description",
        "tags",
        "category__name",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    readonly_fields = (
        "product_image",
        "discount_percentage",
        "in_stock",
        "created_at",
        "updated_at",
    )

    inlines = [
        ProductGalleryInline,
    ]

    fieldsets = (
        ("Basic Product Details", {
            "fields": (
                "name",
                "slug",
                "category",
                "sku",
                "brand",
            )
        }),
        ("Product Image", {
            "fields": (
                "image",
                "product_image",
            )
        }),
        ("Price Details", {
            "fields": (
                "price",
                "old_price",
                "discount_percentage",
                "sale_label",
                "badge",
            )
        }),
        ("Descriptions", {
            "fields": (
                "short_description",
                "description",
                "additional_information",
            )
        }),
        ("Product Specifications", {
            "fields": (
                "weight",
                "color",
                "product_type",
                "tags",
            )
        }),
        ("Stock & Rating", {
            "fields": (
                "stock",
                "in_stock",
                "rating",
                "reviews_count",
            )
        }),
        ("Display Settings", {
            "fields": (
                "is_featured",
                "is_popular",
                "is_active",
            )
        }),
        ("Date Information", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    def product_image(self, obj):
        return preview_image(obj, "image", 70, 90)

    product_image.short_description = "Image"


# -----------------------------
# BANNER ADMIN
# -----------------------------
@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "banner_preview",
        "banner_type",
        "button_text",
        "button_link",
        "content_animation",
        "button_animation",
        "is_active",
        "sort_order",
    )

    list_editable = (
        "is_active",
        "sort_order",
    )

    list_filter = (
        "banner_type",
        "content_animation",
        "button_animation",
        "is_active",
    )

    search_fields = (
        "title",
        "subtitle",
        "badge",
        "discount_label",
    )

    readonly_fields = (
        "banner_preview",
        "created_at",
    )

    fieldsets = (
        ("Banner Content", {
            "fields": (
                "title",
                "subtitle",
                "badge",
                "discount_label",
            )
        }),
        ("Button Details", {
            "fields": (
                "button_text",
                "button_link",
            )
        }),
        ("Banner Image", {
            "fields": (
                "image",
                "banner_preview",
            )
        }),
        ("Banner Type & Style", {
            "fields": (
                "banner_type",
                "bg_color",
                "text_color",
            )
        }),
        ("Animation Settings", {
            "fields": (
                "content_animation",
                "button_animation",
            )
        }),
        ("Display Settings", {
            "fields": (
                "is_active",
                "sort_order",
            )
        }),
        ("Date Information", {
            "fields": (
                "created_at",
            )
        }),
    )

    def banner_preview(self, obj):
        return preview_image(obj, "image", 90, 160)

    banner_preview.short_description = "Banner Preview"


# -----------------------------
# PROMO CARD ADMIN
# -----------------------------
@admin.register(PromoCard)
class PromoCardAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "promo_preview",
        "promo_style",
        "image_position",
        "button_text",
        "button_link",
        "is_active",
        "sort_order",
    )

    list_editable = (
        "promo_style",
        "image_position",
        "is_active",
        "sort_order",
    )

    list_filter = (
        "promo_style",
        "image_position",
        "content_animation",
        "is_active",
    )

    search_fields = (
        "title",
        "subtitle",
        "badge",
    )

    readonly_fields = (
        "promo_preview",
    )

    fieldsets = (
        ("Promo Content", {
            "fields": (
                "title",
                "subtitle",
                "badge",
            )
        }),
        ("Button Details", {
            "fields": (
                "button_text",
                "button_link",
                "button_bg_color",
                "button_text_color",
            )
        }),
        ("Promo Image", {
            "fields": (
                "image",
                "promo_preview",
                "image_position",
                "image_height_percent",
            )
        }),
        ("Dynamic Promo Style", {
            "fields": (
                "promo_style",
                "bg_color",
                "text_color",
                "overlay_opacity",
                "content_animation",
            ),
            "description": "Use Yellow style for fresh fruit cards, Dark style for sale/meat cards, or Custom to fully control colors. Keep overlay opacity 0 to remove the dark green/black full background over images."
        }),
        ("Display Settings", {
            "fields": (
                "is_active",
                "sort_order",
            )
        }),
    )

    def promo_preview(self, obj):
        return preview_image(obj, "image", 90, 150)

    promo_preview.short_description = "Promo Preview"


# -----------------------------
# SERVICE FEATURE ADMIN
# -----------------------------
@admin.register(ServiceFeature)
class ServiceFeatureAdmin(admin.ModelAdmin):
    list_display = (
        "icon",
        "title",
        "subtitle",
        "is_active",
        "sort_order",
    )

    list_editable = (
        "is_active",
        "sort_order",
    )

    search_fields = (
        "title",
        "subtitle",
    )


# -----------------------------
# INSTAGRAM IMAGE ADMIN
# -----------------------------
@admin.register(InstagramImage)
class InstagramImageAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "image_preview",
        "instagram_url",
        "animation",
        "animation_delay_seconds",
        "animation_duration_seconds",
        "is_active",
        "sort_order",
    )

    list_editable = (
        "animation",
        "animation_delay_seconds",
        "animation_duration_seconds",
        "is_active",
        "sort_order",
    )

    list_filter = (
        "animation",
        "is_active",
    )

    search_fields = (
        "title",
        "instagram_url",
    )

    readonly_fields = (
        "image_preview",
    )

    fieldsets = (
        ("Instagram Image Details", {
            "fields": (
                "title",
                "image",
                "image_preview",
                "instagram_url",
            )
        }),
        ("Animation Settings", {
            "fields": (
                "animation",
                "animation_delay_seconds",
                "animation_duration_seconds",
            ),
            "description": "Set delay in seconds so images animate one by one. Example: first 0.00, second 0.35, third 0.70."
        }),
        ("Display Settings", {
            "fields": (
                "is_active",
                "sort_order",
            )
        }),
    )

    def image_preview(self, obj):
        return preview_image(obj, "image", 80, 80)

    image_preview.short_description = "Image Preview"


# -----------------------------
# NEWS POST ADMIN
# -----------------------------
@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "news_preview",
        "category",
        "date_label",
        "is_active",
        "sort_order",
    )

    list_editable = (
        "is_active",
        "sort_order",
    )

    list_filter = (
        "category",
        "is_active",
    )

    search_fields = (
        "title",
        "category",
        "author",
        "excerpt",
    )

    readonly_fields = (
        "news_preview",
    )

    fieldsets = (
        ("News Content", {
            "fields": (
                "title",
                "category",
                "author",
                "comments_count",
                "excerpt",
                "date_label",
            )
        }),
        ("News Image", {
            "fields": (
                "image",
                "news_preview",
            )
        }),
        ("Display Settings", {
            "fields": (
                "is_active",
                "sort_order",
            )
        }),
    )

    def news_preview(self, obj):
        return preview_image(obj, "image", 70, 100)

    news_preview.short_description = "News Preview"


# -----------------------------
# TESTIMONIAL ADMIN
# -----------------------------
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "role",
        "rating",
        "is_active",
        "sort_order",
    )

    list_editable = (
        "rating",
        "is_active",
        "sort_order",
    )

    search_fields = (
        "name",
        "role",
        "message",
    )

    fieldsets = (
        ("Customer Details", {
            "fields": (
                "name",
                "role",
                "image",
                "image_preview",
            )
        }),
        ("Review Details", {
            "fields": (
                "message",
                "rating",
            )
        }),
        ("Display Settings", {
            "fields": (
                "is_active",
                "sort_order",
            )
        }),
    )

    readonly_fields = (
        "image_preview",
    )

    def image_preview(self, obj):
        return preview_image(obj, "image", 70, 70)

    image_preview.short_description = "Customer Image"


# -----------------------------
# SHOP PAGE BANNER ADMIN
# -----------------------------
@admin.register(ShopPageBanner)
class ShopPageBannerAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "breadcrumb_text",
        "banner_preview",
        "is_active",
    )

    list_editable = (
        "is_active",
    )

    search_fields = (
        "title",
        "breadcrumb_text",
    )

    readonly_fields = (
        "banner_preview",
    )

    fieldsets = (
        ("Shop Banner Content", {
            "fields": (
                "title",
                "breadcrumb_text",
                "background_image",
                "banner_preview",
            )
        }),
        ("Display Settings", {
            "fields": (
                "is_active",
            )
        }),
    )

    def banner_preview(self, obj):
        return preview_image(obj, "background_image", 80, 260)

    banner_preview.short_description = "Banner Preview"


# -----------------------------
# SHOP PRICE FILTER ADMIN
# -----------------------------
@admin.register(ShopPriceFilter)
class ShopPriceFilterAdmin(admin.ModelAdmin):
    list_display = (
        "label",
        "min_price",
        "max_price",
        "sort_order",
        "is_active",
    )

    list_editable = (
        "min_price",
        "max_price",
        "sort_order",
        "is_active",
    )

    search_fields = (
        "label",
    )

    list_filter = (
        "is_active",
    )

    fieldsets = (
        ("Price Filter", {
            "fields": (
                "label",
                "min_price",
                "max_price",
                "sort_order",
                "is_active",
            )
        }),
    )


# -----------------------------
# SHOP RATING FILTER ADMIN
# -----------------------------
@admin.register(ShopRatingFilter)
class ShopRatingFilterAdmin(admin.ModelAdmin):
    list_display = (
        "label",
        "rating_value",
        "sort_order",
        "is_active",
    )

    list_editable = (
        "rating_value",
        "sort_order",
        "is_active",
    )

    search_fields = (
        "label",
    )

    list_filter = (
        "is_active",
    )

    fieldsets = (
        ("Rating Filter", {
            "fields": (
                "label",
                "rating_value",
                "sort_order",
                "is_active",
            )
        }),
    )


# -----------------------------
# SHOP POPULAR TAG ADMIN
# -----------------------------
@admin.register(ShopPopularTag)
class ShopPopularTagAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "filter_value",
        "sort_order",
        "is_active",
    )

    list_editable = (
        "filter_value",
        "sort_order",
        "is_active",
    )

    search_fields = (
        "title",
        "filter_value",
    )

    list_filter = (
        "is_active",
    )

    fieldsets = (
        ("Popular Tag", {
            "fields": (
                "title",
                "filter_value",
                "sort_order",
                "is_active",
            )
        }),
    )


# -----------------------------
# SHOP DISCOUNT BANNER ADMIN
# -----------------------------
@admin.register(ShopDiscountBanner)
class ShopDiscountBannerAdmin(admin.ModelAdmin):
    list_display = (
        "discount_text",
        "subtitle",
        "banner_preview",
        "button_text",
        "button_link",
        "is_active",
    )

    list_editable = (
        "button_text",
        "button_link",
        "is_active",
    )

    search_fields = (
        "discount_text",
        "subtitle",
        "button_text",
        "button_link",
    )

    readonly_fields = (
        "banner_preview",
    )

    fieldsets = (
        ("Discount Banner Content", {
            "fields": (
                "discount_text",
                "subtitle",
                "button_text",
                "button_link",
            )
        }),
        ("Discount Banner Image", {
            "fields": (
                "image",
                "banner_preview",
            )
        }),
        ("Display Settings", {
            "fields": (
                "is_active",
            )
        }),
    )

    def banner_preview(self, obj):
        return preview_image(obj, "image", 95, 170)

    banner_preview.short_description = "Banner Preview"


# -----------------------------
# SHOP SALE PRODUCTS ADMIN
# -----------------------------
@admin.register(ShopSaleProduct)
class ShopSaleProductAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "product_image",
        "sort_order",
        "is_active",
    )

    list_editable = (
        "sort_order",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "product__name",
        "product__sku",
        "product__brand",
    )

    autocomplete_fields = (
        "product",
    )

    fieldsets = (
        ("Sale Product", {
            "fields": (
                "product",
                "sort_order",
                "is_active",
            )
        }),
    )

    def product_image(self, obj):
        if obj.product:
            return preview_image(obj.product, "image", 55, 65)
        return "No product"

    product_image.short_description = "Product Image"


# -----------------------------
# SALE OF THE MONTH BANNER ADMIN
# -----------------------------
@admin.register(SaleOfMonthBanner)
class SaleOfMonthBannerAdmin(admin.ModelAdmin):
    list_display = (
        "small_title",
        "title",
        "discount_text",
        "banner_preview",
        "button_text",
        "button_link",
        "is_active",
        "sort_order",
    )

    list_editable = (
        "button_text",
        "button_link",
        "is_active",
        "sort_order",
    )

    search_fields = (
        "small_title",
        "title",
        "discount_text",
        "button_text",
        "button_link",
    )

    readonly_fields = (
        "banner_preview",
    )

    fieldsets = (
        ("Banner Text", {
            "fields": (
                "small_title",
                "title",
                "discount_text",
            )
        }),
        ("Countdown Timer", {
            "fields": (
                "days",
                "hours",
                "minutes",
                "seconds",
            )
        }),
        ("Button Details", {
            "fields": (
                "button_text",
                "button_link",
            )
        }),
        ("Banner Image & Style", {
            "fields": (
                "image",
                "banner_preview",
                "bg_color",
                "text_color",
            )
        }),
        ("Display Settings", {
            "fields": (
                "is_active",
                "sort_order",
            )
        }),
    )

    def banner_preview(self, obj):
        return preview_image(obj, "image", 90, 180)

    banner_preview.short_description = "Banner Preview"




# -----------------------------
# CART PAGE BANNER ADMIN
# -----------------------------
@admin.register(CartPageBanner)
class CartPageBannerAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "breadcrumb_text",
        "banner_preview",
        "is_active",
    )

    list_editable = (
        "is_active",
    )

    search_fields = (
        "title",
        "breadcrumb_text",
    )

    readonly_fields = (
        "banner_preview",
    )

    fieldsets = (
        ("Cart Banner Content", {
            "fields": (
                "title",
                "breadcrumb_text",
            )
        }),
        ("Banner Image", {
            "fields": (
                "background_image",
                "banner_preview",
            )
        }),
        ("Display Settings", {
            "fields": (
                "is_active",
            )
        }),
    )

    def banner_preview(self, obj):
        return preview_image(obj, "background_image", 90, 260)

    banner_preview.short_description = "Banner Preview"


# -----------------------------
# COUPON CODE ADMIN
# -----------------------------
@admin.register(CouponCode)
class CouponCodeAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "discount_type",
        "discount_value",
        "minimum_order_amount",
        "maximum_discount_amount",
        "is_active",
        "created_at",
    )

    list_editable = (
        "discount_type",
        "discount_value",
        "minimum_order_amount",
        "maximum_discount_amount",
        "is_active",
    )

    search_fields = (
        "code",
    )

    list_filter = (
        "discount_type",
        "is_active",
        "created_at",
    )

    readonly_fields = (
        "created_at",
    )

    fieldsets = (
        ("Coupon Details", {
            "fields": (
                "code",
                "discount_type",
                "discount_value",
            )
        }),
        ("Order Rules", {
            "fields": (
                "minimum_order_amount",
                "maximum_discount_amount",
            )
        }),
        ("Display Settings", {
            "fields": (
                "is_active",
            )
        }),
        ("Date Information", {
            "fields": (
                "created_at",
            )
        }),
    )


# -----------------------------
# CART RELATED PRODUCTS ADMIN
# -----------------------------
@admin.register(CartRelatedProduct)
class CartRelatedProductAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "product_image",
        "sort_order",
        "is_active",
    )

    list_editable = (
        "sort_order",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "product__name",
        "product__sku",
        "product__brand",
    )

    autocomplete_fields = (
        "product",
    )

    fieldsets = (
        ("Related Product", {
            "fields": (
                "product",
                "sort_order",
                "is_active",
            )
        }),
    )

    def product_image(self, obj):
        if obj.product:
            return preview_image(obj.product, "image", 55, 65)
        return "No product"

    product_image.short_description = "Product Image"




# -----------------------------
# BLOG PAGE BANNER ADMIN
# -----------------------------
@admin.register(BlogPageBanner)
class BlogPageBannerAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "breadcrumb_text",
        "banner_preview",
        "is_active",
    )
    list_editable = ("is_active",)
    search_fields = ("title", "breadcrumb_text")
    readonly_fields = ("banner_preview",)

    fieldsets = (
        ("Banner Content", {
            "fields": (
                "title",
                "breadcrumb_text",
                "background_image",
                "banner_preview",
            )
        }),
        ("Display Settings", {"fields": ("is_active",)}),
    )

    def banner_preview(self, obj):
        return preview_image(obj, "background_image", 80, 260)

    banner_preview.short_description = "Banner Preview"


# -----------------------------
# BLOG CATEGORY ADMIN
# -----------------------------
@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "post_count",
        "sort_order",
        "is_active",
    )
    list_editable = ("sort_order", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "slug")
    list_filter = ("is_active",)

    def post_count(self, obj):
        return obj.posts.filter(is_active=True).count()

    post_count.short_description = "Posts"


# -----------------------------
# BLOG POST ADMIN
# -----------------------------
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "post_preview",
        "category",
        "author_name",
        "date_label",
        "comments_count",
        "is_video",
        "is_active",
        "sort_order",
    )
    list_editable = (
        "comments_count",
        "is_video",
        "is_active",
        "sort_order",
    )
    list_filter = ("category", "is_active", "is_video")
    search_fields = ("title", "excerpt", "author_name", "category__name")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("post_preview", "created_at", "updated_at")

    fieldsets = (
        ("Post Content", {
            "fields": (
                "category",
                "title",
                "slug",
                "excerpt",
                "author_name",
                "date_label",
                "comments_count",
                "read_more_text",
            )
        }),
        ("Post Image", {"fields": ("image", "post_preview")}),
        ("Video Option", {"fields": ("is_video", "video_url")}),
        ("Display Settings", {"fields": ("is_active", "sort_order")}),
        ("Date Information", {"fields": ("created_at", "updated_at")}),
    )

    def post_preview(self, obj):
        return preview_image(obj, "image", 75, 120)

    post_preview.short_description = "Post Preview"


# -----------------------------
# BLOG POPULAR TAG ADMIN
# -----------------------------
@admin.register(BlogPopularTag)
class BlogPopularTagAdmin(admin.ModelAdmin):
    list_display = ("title", "filter_value", "sort_order", "is_active")
    list_editable = ("filter_value", "sort_order", "is_active")
    search_fields = ("title", "filter_value")
    list_filter = ("is_active",)


# -----------------------------
# BLOG DISCOUNT BANNER ADMIN
# -----------------------------
@admin.register(BlogDiscountBanner)
class BlogDiscountBannerAdmin(admin.ModelAdmin):
    list_display = (
        "discount_text",
        "subtitle",
        "banner_preview",
        "button_text",
        "button_link",
        "is_active",
    )
    list_editable = ("button_text", "button_link", "is_active")
    search_fields = ("discount_text", "subtitle", "button_text")
    readonly_fields = ("banner_preview",)

    fieldsets = (
        ("Discount Content", {
            "fields": (
                "discount_text",
                "subtitle",
                "button_text",
                "button_link",
            )
        }),
        ("Discount Image", {"fields": ("image", "banner_preview")}),
        ("Display Settings", {"fields": ("is_active",)}),
    )

    def banner_preview(self, obj):
        return preview_image(obj, "image", 95, 170)

    banner_preview.short_description = "Banner Preview"


# -----------------------------
# BLOG RECENTLY ADDED ADMIN
# -----------------------------
@admin.register(BlogRecentPost)
class BlogRecentPostAdmin(admin.ModelAdmin):
    list_display = ("post", "post_image", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    search_fields = ("post__title", "post__category__name")
    list_filter = ("is_active",)
    autocomplete_fields = ("post",)

    def post_image(self, obj):
        if obj.post:
            return preview_image(obj.post, "image", 55, 70)
        return "No post"

    post_image.short_description = "Post Image"


# -----------------------------
# BLOG GALLERY IMAGE ADMIN
# -----------------------------
@admin.register(BlogGalleryImage)
class BlogGalleryImageAdmin(admin.ModelAdmin):
    list_display = ("title", "image_preview", "url", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    search_fields = ("title", "url")
    readonly_fields = ("image_preview",)

    fieldsets = (
        ("Gallery Image", {"fields": ("title", "image", "image_preview", "url")}),
        ("Display Settings", {"fields": ("sort_order", "is_active")}),
    )

    def image_preview(self, obj):
        return preview_image(obj, "image", 70, 90)

    image_preview.short_description = "Image Preview"


# -----------------------------
# BLOG BRAND LOGO ADMIN
# -----------------------------
@admin.register(BlogBrandLogo)
class BlogBrandLogoAdmin(admin.ModelAdmin):
    list_display = ("title", "logo_preview", "text_logo", "url", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    search_fields = ("title", "text_logo", "url")
    readonly_fields = ("logo_preview",)

    fieldsets = (
        ("Brand Details", {"fields": ("title", "image", "logo_preview", "text_logo", "url")}),
        ("Display Settings", {"fields": ("sort_order", "is_active")}),
    )

    def logo_preview(self, obj):
        return preview_image(obj, "image", 45, 120)

    logo_preview.short_description = "Logo Preview"




# -----------------------------
# CONTACT PAGE ADMIN
# -----------------------------
@admin.register(ContactPageBanner)
class ContactPageBannerAdmin(admin.ModelAdmin):
    list_display = ("title", "breadcrumb_text", "banner_preview", "is_active")
    list_editable = ("is_active",)
    search_fields = ("title", "breadcrumb_text")
    readonly_fields = ("banner_preview",)

    fieldsets = (
        ("Banner Content", {"fields": ("title", "breadcrumb_text")}),
        ("Banner Image", {"fields": ("background_image", "banner_preview")}),
        ("Display Settings", {"fields": ("is_active",)}),
    )

    def banner_preview(self, obj):
        return preview_image(obj, "background_image", 80, 220)

    banner_preview.short_description = "Banner Preview"


@admin.register(ContactInfoItem)
class ContactInfoItemAdmin(admin.ModelAdmin):
    list_display = ("icon_type", "title", "line_one", "line_two", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    search_fields = ("title", "line_one", "line_two")
    list_filter = ("icon_type", "is_active")

    fieldsets = (
        ("Icon", {"fields": ("icon_type", "custom_icon")}),
        ("Contact Text", {"fields": ("title", "line_one", "line_two")}),
        ("Display Settings", {"fields": ("sort_order", "is_active")}),
    )


@admin.register(ContactFormSetting)
class ContactFormSettingAdmin(admin.ModelAdmin):
    list_display = ("form_title", "recipient_email", "submit_button_text", "form_preview", "is_active")
    list_editable = ("submit_button_text", "is_active")
    search_fields = ("form_title", "recipient_email", "email_subject_prefix")
    readonly_fields = ("form_preview", "map_preview")

    fieldsets = (
        ("Form Text", {"fields": ("form_title", "name_placeholder", "email_placeholder", "phone_placeholder", "message_placeholder", "submit_button_text")}),
        ("Email Delivery", {"fields": ("recipient_email", "email_subject_prefix", "success_message")}),
        ("Design", {"fields": ("form_background_image", "form_preview", "form_bg_color", "contact_card_bg_color")}),
        ("Map", {"fields": ("map_embed_url", "map_image", "map_preview", "map_height")}),
        ("Display Settings", {"fields": ("is_active",)}),
    )

    def form_preview(self, obj):
        return preview_image(obj, "form_background_image", 80, 150)

    form_preview.short_description = "Form Background Preview"

    def map_preview(self, obj):
        return preview_image(obj, "map_image", 80, 150)

    map_preview.short_description = "Map Image Preview"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "email_sent", "is_read", "created_at")
    list_editable = ("is_read",)
    search_fields = ("name", "email", "phone", "message")
    list_filter = ("is_read", "email_sent", "created_at")
    readonly_fields = ("name", "email", "phone", "message", "email_sent", "email_error", "created_at", "updated_at")

    fieldsets = (
        ("Message", {"fields": ("name", "email", "phone", "message", "is_read")}),
        ("Email Status", {"fields": ("email_sent", "email_error")}),
        ("Date Information", {"fields": ("created_at", "updated_at")}),
    )


# -----------------------------
# NEWSLETTER SECTION ADMIN
# -----------------------------
@admin.register(NewsletterSection)
class NewsletterSectionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "subtitle",
        "placeholder_text",
        "button_text",
        "is_active",
    )

    list_editable = (
        "is_active",
    )

    search_fields = (
        "title",
        "subtitle",
        "placeholder_text",
        "button_text",
    )

    fieldsets = (
        ("Newsletter Content", {
            "fields": (
                "title",
                "subtitle",
                "placeholder_text",
                "button_text",
            )
        }),
        ("Display Settings", {
            "fields": (
                "is_active",
            )
        }),
    )


# -----------------------------
# FOOTER SETTING ADMIN
# -----------------------------
@admin.register(FooterSetting)
class FooterSettingAdmin(admin.ModelAdmin):
    list_display = (
        "logo_text",
        "logo_preview",
        "phone",
        "email",
        "show_payment_badges",
        "is_active",
    )

    list_editable = (
        "show_payment_badges",
        "is_active",
    )

    search_fields = (
        "logo_text",
        "about_title",
        "about_text",
        "phone",
        "email",
    )

    readonly_fields = (
        "logo_preview",
    )

    fieldsets = (
        ("Footer Logo", {
            "fields": (
                "logo",
                "logo_preview",
                "logo_text",
            )
        }),
        ("About Section", {
            "fields": (
                "about_title",
                "about_text",
            )
        }),
        ("Contact Details", {
            "fields": (
                "phone",
                "email",
            )
        }),
        ("Social Media Links", {
            "fields": (
                "facebook_url",
                "twitter_url",
                "pinterest_url",
                "instagram_url",
            )
        }),
        ("Bottom Footer", {
            "fields": (
                "copyright_text",
                "show_payment_badges",
                "is_active",
            )
        }),
    )

    def logo_preview(self, obj):
        return preview_image(obj, "logo", 55, 180)

    logo_preview.short_description = "Logo Preview"


# -----------------------------
# FOOTER COLUMN + FOOTER LINK ADMIN
# -----------------------------
class FooterLinkInline(admin.TabularInline):
    model = FooterLink
    extra = 1

    fields = (
        "title",
        "url",
        "sort_order",
        "is_active",
    )


@admin.register(FooterColumn)
class FooterColumnAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "sort_order",
        "is_active",
    )

    list_editable = (
        "sort_order",
        "is_active",
    )

    search_fields = (
        "title",
    )

    inlines = [
        FooterLinkInline,
    ]

    fieldsets = (
        ("Footer Column Details", {
            "fields": (
                "title",
                "sort_order",
                "is_active",
            )
        }),
    )


# -----------------------------
# FOOTER INSTAGRAM IMAGE ADMIN
# -----------------------------
@admin.register(FooterInstagramImage)
class FooterInstagramImageAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "image_preview",
        "url",
        "sort_order",
        "is_active",
    )

    list_editable = (
        "sort_order",
        "is_active",
    )

    search_fields = (
        "title",
        "url",
    )

    readonly_fields = (
        "image_preview",
    )

    fieldsets = (
        ("Footer Instagram Image", {
            "fields": (
                "title",
                "image",
                "image_preview",
                "url",
            )
        }),
        ("Display Settings", {
            "fields": (
                "sort_order",
                "is_active",
            )
        }),
    )

    def image_preview(self, obj):
        return preview_image(obj, "image", 70, 90)

    image_preview.short_description = "Image Preview"


# -----------------------------
# NEWSLETTER SUBSCRIBERS ADMIN
# -----------------------------
@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "created_at",
    )

    search_fields = (
        "email",
    )

    readonly_fields = (
        "email",
        "created_at",
    )

    list_filter = (
        "created_at",
    )


# -----------------------------
# WISHLIST ITEM ADMIN
# -----------------------------
@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "product",
        "product_image",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "product__name",
        "product__sku",
        "product__brand",
    )

    list_filter = (
        "created_at",
    )

    autocomplete_fields = (
        "user",
        "product",
    )

    readonly_fields = (
        "created_at",
        "product_image",
    )

    fieldsets = (
        ("Wishlist Details", {
            "fields": (
                "user",
                "product",
                "product_image",
            )
        }),
        ("Date Information", {
            "fields": (
                "created_at",
            )
        }),
    )

    def product_image(self, obj):
        if obj.product:
            return preview_image(obj.product, "image", 55, 65)
        return "No product"

    product_image.short_description = "Product Image"


# -----------------------------
# CHECKOUT PAYMENT METHOD ADMIN
# -----------------------------
@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "method_type",
        "description",
        "sort_order",
        "is_active",
    )
    list_editable = (
        "method_type",
        "sort_order",
        "is_active",
    )
    search_fields = (
        "title",
        "method_type",
        "description",
    )
    list_filter = (
        "method_type",
        "is_active",
    )

    fieldsets = (
        ("Payment Method", {
            "fields": (
                "title",
                "method_type",
                "description",
                "icon",
            )
        }),
        ("Display Settings", {
            "fields": (
                "sort_order",
                "is_active",
            )
        }),
    )


# -----------------------------
# CART ITEM ADMIN
# -----------------------------
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "product",
        "quantity",
        "item_total",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "user__username",
        "product__name",
    )

    list_filter = (
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "item_total",
        "created_at",
        "updated_at",
    )


# -----------------------------
# ORDER ITEM INLINE
# -----------------------------
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

    fields = (
        "product",
        "product_name",
        "price",
        "quantity",
    )

    readonly_fields = ()

    can_delete = False


# -----------------------------
# ORDER ADMIN
# -----------------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "full_name",
        "phone",
        "city",
        "pincode",
        "payment_method",
        "total_amount",
        "status",
        "created_at",
    )

    list_editable = (
        "status",
    )

    list_filter = (
        "status",
        "payment_method",
        "city",
        "created_at",
    )

    search_fields = (
        "user__username",
        "full_name",
        "phone",
        "email",
        "city",
        "pincode",
    )

    readonly_fields = (
        "created_at",
    )

    inlines = [
        OrderItemInline,
    ]

    fieldsets = (
        ("Customer Details", {
            "fields": (
                "user",
                "full_name",
                "phone",
                "email",
            )
        }),
        ("Delivery Address", {
            "fields": (
                "address",
                "city",
                "state",
                "pincode",
            )
        }),
        ("Payment & Order Status", {
            "fields": (
                "payment_method",
                "total_amount",
                "status",
                "order_note",
            )
        }),
        ("Date Information", {
            "fields": (
                "created_at",
            )
        }),
    )

# -----------------------------
# ABOUT PAGE ADMIN
# -----------------------------
@admin.register(AboutPageBanner)
class AboutPageBannerAdmin(admin.ModelAdmin):
    list_display = ("title", "breadcrumb_text", "banner_preview", "is_active")
    list_editable = ("is_active",)
    search_fields = ("title", "breadcrumb_text")
    readonly_fields = ("banner_preview",)

    fieldsets = (
        ("Banner Content", {"fields": ("title", "breadcrumb_text")}),
        ("Banner Image", {"fields": ("background_image", "banner_preview")}),
        ("Display Settings", {"fields": ("is_active",)}),
    )

    def banner_preview(self, obj):
        return preview_image(obj, "background_image", 80, 220)

    banner_preview.short_description = "Banner Preview"


@admin.register(AboutHeroSection)
class AboutHeroSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "hero_preview", "button_text", "is_active")
    list_editable = ("button_text", "is_active")
    search_fields = ("title", "description")
    readonly_fields = ("hero_preview",)

    fieldsets = (
        ("Content", {"fields": ("title", "description", "button_text", "button_link")}),
        ("Image", {"fields": ("image", "hero_preview")}),
        ("Display Settings", {"fields": ("is_active",)}),
    )

    def hero_preview(self, obj):
        return preview_image(obj, "image", 90, 160)

    hero_preview.short_description = "Hero Preview"


@admin.register(AboutFeatureSection)
class AboutFeatureSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "feature_preview", "is_active")
    list_editable = ("is_active",)
    search_fields = ("title", "description")
    readonly_fields = ("feature_preview",)

    fieldsets = (
        ("Content", {"fields": ("title", "description")}),
        ("Image", {"fields": ("image", "feature_preview")}),
        ("Display Settings", {"fields": ("is_active",)}),
    )

    def feature_preview(self, obj):
        return preview_image(obj, "image", 90, 160)

    feature_preview.short_description = "Feature Preview"


@admin.register(AboutFeatureItem)
class AboutFeatureItemAdmin(admin.ModelAdmin):
    list_display = ("icon", "title", "subtitle", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    search_fields = ("title", "subtitle")
    list_filter = ("is_active",)


@admin.register(AboutDeliverySection)
class AboutDeliverySectionAdmin(admin.ModelAdmin):
    list_display = ("title", "delivery_preview", "button_text", "is_active")
    list_editable = ("button_text", "is_active")
    search_fields = ("title", "description")
    readonly_fields = ("delivery_preview",)

    fieldsets = (
        ("Content", {"fields": ("title", "description")}),
        ("Checklist", {"fields": ("point_one", "point_two", "point_three")}),
        ("Button", {"fields": ("button_text", "button_link")}),
        ("Image", {"fields": ("image", "delivery_preview")}),
        ("Display Settings", {"fields": ("is_active",)}),
    )

    def delivery_preview(self, obj):
        return preview_image(obj, "image", 100, 150)

    delivery_preview.short_description = "Delivery Preview"


@admin.register(AboutTeamMember)
class AboutTeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "member_preview", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    search_fields = ("name", "role")
    list_filter = ("is_active",)
    readonly_fields = ("member_preview",)

    def member_preview(self, obj):
        return preview_image(obj, "image", 70, 70)

    member_preview.short_description = "Member Preview"


@admin.register(AboutTestimonial)
class AboutTestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "rating", "testimonial_preview", "sort_order", "is_active")
    list_editable = ("rating", "sort_order", "is_active")
    search_fields = ("name", "role", "message")
    list_filter = ("is_active", "rating")
    readonly_fields = ("testimonial_preview",)

    def testimonial_preview(self, obj):
        return preview_image(obj, "image", 60, 60)

    testimonial_preview.short_description = "Image Preview"


@admin.register(AboutBrandLogo)
class AboutBrandLogoAdmin(admin.ModelAdmin):
    list_display = ("title", "brand_preview", "text_logo", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    search_fields = ("title", "text_logo", "url")
    list_filter = ("is_active",)
    readonly_fields = ("brand_preview",)

    def brand_preview(self, obj):
        return preview_image(obj, "image", 50, 120)

    brand_preview.short_description = "Brand Preview"
