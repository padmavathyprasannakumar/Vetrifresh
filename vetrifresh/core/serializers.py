from decimal import Decimal

from rest_framework import serializers

from .models import (
    AboutBrandLogo,
    AboutDeliverySection,
    AboutFeatureItem,
    AboutFeatureSection,
    AboutHeroSection,
    AboutPageBanner,
    AboutTeamMember,
    AboutTestimonial,
    ContactMessage,
    ContactFormSetting,
    ContactInfoItem,
    ContactPageBanner,
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


class AbsoluteImageMixin:
    def absolute_media_url(self, file_field):
        request = self.context.get("request")

        if not file_field:
            return None

        try:
            url = file_field.url
        except ValueError:
            return None

        return request.build_absolute_uri(url) if request else url


# -----------------------------
# AUTH / USER SERIALIZERS
# -----------------------------
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=6,
        style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "phone",
            "address",
            "password",
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "phone",
            "address",
            "first_name",
            "last_name",
        ]


# -----------------------------
# SITE SETTING SERIALIZER
# -----------------------------
class SiteSettingSerializer(AbsoluteImageMixin, serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = SiteSetting
        fields = [
            "id",
            "site_name",
            "logo",
            "logo_url",
            "phone",
            "currency_symbol",
            "currency_code",
            "language",
            "location_placeholder",
            "footer_about",
            "footer_email",
            "free_shipping_text",
            "hero_footer_text",
            "show_search_icon",
            "show_wishlist_icon",
            "show_cart_icon",
            "show_user_icon",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "logo_url",
            "created_at",
            "updated_at",
        ]

    def get_logo_url(self, obj):
        return self.absolute_media_url(obj.logo)


# -----------------------------
# NAVBAR SERIALIZER
# -----------------------------
class NavbarLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = NavbarLink
        fields = [
            "id",
            "title",
            "url",
            "sort_order",
            "is_active",
            "is_category_dropdown",
        ]


# -----------------------------
# CATEGORY SERIALIZER
# -----------------------------
class CategorySerializer(AbsoluteImageMixin, serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    product_count = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "image",
            "image_url",
            "parent",
            "children",
            "is_active",
            "show_in_home",
            "sort_order",
            "product_count",
        ]

        read_only_fields = [
            "slug",
            "image_url",
            "children",
            "product_count",
        ]

    def get_image_url(self, obj):
        return self.absolute_media_url(obj.image)

    def get_product_count(self, obj):
        return obj.products.filter(is_active=True).count()

    def get_children(self, obj):
        children = obj.children.filter(
            is_active=True
        ).order_by("sort_order", "name")

        return CategorySerializer(
            children,
            many=True,
            context=self.context
        ).data


# -----------------------------
# BANNER SERIALIZER
# -----------------------------
class BannerSerializer(AbsoluteImageMixin, serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Banner
        fields = [
            "id",
            "title",
            "subtitle",
            "badge",
            "discount_label",
            "button_text",
            "button_link",
            "image",
            "image_url",
            "banner_type",
            "bg_color",
            "text_color",
            "content_animation",
            "button_animation",
            "is_active",
            "sort_order",
            "created_at",
        ]

        read_only_fields = [
            "image_url",
            "created_at",
        ]

    def get_image_url(self, obj):
        return self.absolute_media_url(obj.image)


# -----------------------------
# PROMO CARD SERIALIZER
# -----------------------------
class PromoCardSerializer(AbsoluteImageMixin, serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = PromoCard
        fields = [
            "id",
            "title",
            "subtitle",
            "badge",
            "button_text",
            "button_link",
            "image",
            "image_url",
            "promo_style",
            "image_position",
            "bg_color",
            "text_color",
            "button_bg_color",
            "button_text_color",
            "image_height_percent",
            "overlay_opacity",
            "content_animation",
            "is_active",
            "sort_order",
        ]

        read_only_fields = [
            "image_url",
        ]

    def get_image_url(self, obj):
        return self.absolute_media_url(obj.image)


# -----------------------------
# SERVICE FEATURE SERIALIZER
# -----------------------------
class ServiceFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceFeature
        fields = [
            "id",
            "title",
            "subtitle",
            "icon",
            "is_active",
            "sort_order",
        ]


# -----------------------------
# PRODUCT GALLERY SERIALIZER
# -----------------------------
class ProductGallerySerializer(AbsoluteImageMixin, serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductGallery
        fields = [
            "id",
            "image",
            "image_url",
            "alt_text",
            "sort_order",
        ]

        read_only_fields = [
            "image_url",
        ]

    def get_image_url(self, obj):
        return self.absolute_media_url(obj.image)


# -----------------------------
# PRODUCT SERIALIZER
# -----------------------------
class ProductSerializer(AbsoluteImageMixin, serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    category_name = serializers.CharField(
        source="category.name",
        read_only=True
    )

    category_slug = serializers.CharField(
        source="category.slug",
        read_only=True
    )

    gallery = ProductGallerySerializer(
        many=True,
        read_only=True
    )

    in_stock = serializers.BooleanField(read_only=True)
    discount_percentage = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "category",
            "category_name",
            "category_slug",
            "sku",
            "brand",
            "image",
            "image_url",
            "price",
            "old_price",
            "sale_label",
            "badge",
            "short_description",
            "description",
            "additional_information",
            "weight",
            "color",
            "product_type",
            "stock",
            "in_stock",
            "rating",
            "reviews_count",
            "tags",
            "is_featured",
            "is_popular",
            "is_active",
            "discount_percentage",
            "gallery",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "slug",
            "sku",
            "image_url",
            "category_name",
            "category_slug",
            "in_stock",
            "discount_percentage",
            "gallery",
            "created_at",
            "updated_at",
        ]

    def get_image_url(self, obj):
        return self.absolute_media_url(obj.image)


# -----------------------------
# INSTAGRAM SERIALIZER
# -----------------------------
class InstagramImageSerializer(AbsoluteImageMixin, serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = InstagramImage
        fields = [
            "id",
            "title",
            "image",
            "image_url",
            "instagram_url",
            "animation",
            "animation_delay_seconds",
            "animation_duration_seconds",
            "is_active",
            "sort_order",
        ]

        read_only_fields = [
            "image_url",
        ]

    def get_image_url(self, obj):
        return self.absolute_media_url(obj.image)


# -----------------------------
# NEWS POST SERIALIZER
# -----------------------------
class NewsPostSerializer(AbsoluteImageMixin, serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = NewsPost
        fields = [
            "id",
            "title",
            "image",
            "image_url",
            "category",
            "author",
            "comments_count",
            "excerpt",
            "date_label",
            "is_active",
            "sort_order",
        ]

        read_only_fields = [
            "image_url",
        ]

    def get_image_url(self, obj):
        return self.absolute_media_url(obj.image)


# -----------------------------
# TESTIMONIAL SERIALIZER
# -----------------------------
class TestimonialSerializer(AbsoluteImageMixin, serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Testimonial
        fields = [
            "id",
            "name",
            "role",
            "image",
            "image_url",
            "message",
            "rating",
            "is_active",
            "sort_order",
        ]

        read_only_fields = [
            "image_url",
        ]

    def get_image_url(self, obj):
        return self.absolute_media_url(obj.image)


# -----------------------------
# SHOP PAGE SIDEBAR SERIALIZERS
# -----------------------------
class ShopPageBannerSerializer(AbsoluteImageMixin, serializers.ModelSerializer):
    background_image_url = serializers.SerializerMethodField()

    class Meta:
        model = ShopPageBanner
        fields = [
            "id",
            "title",
            "breadcrumb_text",
            "background_image",
            "background_image_url",
            "is_active",
        ]

        read_only_fields = [
            "background_image_url",
        ]

    def get_background_image_url(self, obj):
        return self.absolute_media_url(obj.background_image)


class ShopPriceFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopPriceFilter
        fields = [
            "id",
            "label",
            "min_price",
            "max_price",
            "sort_order",
            "is_active",
        ]


class ShopRatingFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopRatingFilter
        fields = [
            "id",
            "label",
            "rating_value",
            "sort_order",
            "is_active",
        ]


class ShopPopularTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopPopularTag
        fields = [
            "id",
            "title",
            "filter_value",
            "sort_order",
            "is_active",
        ]


class ShopDiscountBannerSerializer(
    AbsoluteImageMixin,
    serializers.ModelSerializer
):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ShopDiscountBanner
        fields = [
            "id",
            "discount_text",
            "subtitle",
            "button_text",
            "button_link",
            "image",
            "image_url",
            "is_active",
        ]

        read_only_fields = [
            "image_url",
        ]

    def get_image_url(self, obj):
        return self.absolute_media_url(obj.image)


class ShopSaleProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(
        source="product.id",
        read_only=True
    )

    class Meta:
        model = ShopSaleProduct
        fields = [
            "id",
            "product",
            "product_id",
            "sort_order",
            "is_active",
        ]



# -----------------------------
# SALE OF MONTH + WISHLIST SERIALIZERS
# -----------------------------
class SaleOfMonthBannerSerializer(AbsoluteImageMixin, serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = SaleOfMonthBanner
        fields = [
            "id",
            "small_title",
            "title",
            "discount_text",
            "days",
            "hours",
            "minutes",
            "seconds",
            "button_text",
            "button_link",
            "image",
            "image_url",
            "bg_color",
            "text_color",
            "is_active",
            "sort_order",
        ]

        read_only_fields = [
            "image_url",
        ]

    def get_image_url(self, obj):
        return self.absolute_media_url(obj.image)


class WishlistItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = WishlistItem
        fields = [
            "id",
            "product",
            "product_id",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "product",
            "created_at",
        ]

    def validate_product_id(self, value):
        product = Product.objects.filter(
            id=value,
            is_active=True
        ).first()

        if not product:
            raise serializers.ValidationError("Invalid product.")

        return value

    def create(self, validated_data):
        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Login required.")

        product_id = validated_data.pop("product_id")

        product = Product.objects.filter(
            id=product_id,
            is_active=True
        ).first()

        if not product:
            raise serializers.ValidationError("Invalid product.")

        wishlist_item, created = WishlistItem.objects.get_or_create(
            user=request.user,
            product=product
        )

        return wishlist_item


# -----------------------------
# CART PAGE SERIALIZERS
# -----------------------------
class CartPageBannerSerializer(AbsoluteImageMixin, serializers.ModelSerializer):
    background_image_url = serializers.SerializerMethodField()

    class Meta:
        model = CartPageBanner
        fields = [
            "id",
            "title",
            "breadcrumb_text",
            "background_image",
            "background_image_url",
            "is_active",
        ]

        read_only_fields = [
            "background_image_url",
        ]

    def get_background_image_url(self, obj):
        return self.absolute_media_url(obj.background_image)


class CouponCodeSerializer(serializers.ModelSerializer):
    display_text = serializers.SerializerMethodField()

    class Meta:
        model = CouponCode
        fields = [
            "id",
            "code",
            "discount_type",
            "discount_value",
            "display_text",
            "minimum_order_amount",
            "maximum_discount_amount",
            "is_active",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "display_text",
            "created_at",
        ]

    def get_display_text(self, obj):
        value = obj.discount_value or Decimal("0")

        if obj.discount_type == "fixed":
            return f"₹{value:.0f} OFF" if value == value.to_integral() else f"₹{value:.2f} OFF"

        return f"{value:.0f}% OFF" if value == value.to_integral() else f"{value:.2f}% OFF"


class CartRelatedProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(
        source="product.id",
        read_only=True
    )

    class Meta:
        model = CartRelatedProduct
        fields = [
            "id",
            "product",
            "product_id",
            "sort_order",
            "is_active",
        ]




# -----------------------------
# ABOUT PAGE SERIALIZERS
# -----------------------------
class AboutPageBannerSerializer(AbsoluteImageMixin, serializers.ModelSerializer):
    background_image_url = serializers.SerializerMethodField()

    class Meta:
        model = AboutPageBanner
        fields = ["id", "title", "breadcrumb_text", "background_image", "background_image_url", "is_active"]
        read_only_fields = ["background_image_url"]

    def get_background_image_url(self, obj):
        return self.absolute_media_url(obj.background_image)


class AboutHeroSectionSerializer(AbsoluteImageMixin, serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = AboutHeroSection
        fields = ["id", "title", "description", "image", "image_url", "button_text", "button_link", "is_active"]
        read_only_fields = ["image_url"]

    def get_image_url(self, obj):
        return self.absolute_media_url(obj.image)


class AboutFeatureSectionSerializer(AbsoluteImageMixin, serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = AboutFeatureSection
        fields = ["id", "title", "description", "image", "image_url", "is_active"]
        read_only_fields = ["image_url"]

    def get_image_url(self, obj):
        return self.absolute_media_url(obj.image)


class AboutFeatureItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutFeatureItem
        fields = ["id", "icon", "title", "subtitle", "sort_order", "is_active"]


class AboutDeliverySectionSerializer(AbsoluteImageMixin, serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = AboutDeliverySection
        fields = [
            "id", "title", "description", "image", "image_url",
            "point_one", "point_two", "point_three", "button_text", "button_link", "is_active"
        ]
        read_only_fields = ["image_url"]

    def get_image_url(self, obj):
        return self.absolute_media_url(obj.image)


class AboutTeamMemberSerializer(AbsoluteImageMixin, serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = AboutTeamMember
        fields = [
            "id", "name", "role", "image", "image_url", "facebook_url", "twitter_url",
            "instagram_url", "sort_order", "is_active"
        ]
        read_only_fields = ["image_url"]

    def get_image_url(self, obj):
        return self.absolute_media_url(obj.image)


class AboutTestimonialSerializer(AbsoluteImageMixin, serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = AboutTestimonial
        fields = ["id", "name", "role", "image", "image_url", "message", "rating", "sort_order", "is_active"]
        read_only_fields = ["image_url"]

    def get_image_url(self, obj):
        return self.absolute_media_url(obj.image)


class AboutBrandLogoSerializer(AbsoluteImageMixin, serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = AboutBrandLogo
        fields = ["id", "title", "image", "image_url", "text_logo", "url", "sort_order", "is_active"]
        read_only_fields = ["image_url"]

    def get_image_url(self, obj):
        return self.absolute_media_url(obj.image)




# -----------------------------
# CONTACT PAGE SERIALIZERS
# -----------------------------
class ContactPageBannerSerializer(AbsoluteImageMixin, serializers.ModelSerializer):
    background_image_url = serializers.SerializerMethodField()

    class Meta:
        model = ContactPageBanner
        fields = [
            "id",
            "title",
            "breadcrumb_text",
            "background_image",
            "background_image_url",
            "is_active",
        ]
        read_only_fields = ["background_image_url"]

    def get_background_image_url(self, obj):
        return self.absolute_media_url(obj.background_image)


class ContactInfoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfoItem
        fields = [
            "id",
            "icon_type",
            "custom_icon",
            "title",
            "line_one",
            "line_two",
            "sort_order",
            "is_active",
        ]


class ContactFormSettingSerializer(AbsoluteImageMixin, serializers.ModelSerializer):
    form_background_image_url = serializers.SerializerMethodField()
    map_image_url = serializers.SerializerMethodField()

    class Meta:
        model = ContactFormSetting
        fields = [
            "id",
            "form_title",
            "name_placeholder",
            "email_placeholder",
            "phone_placeholder",
            "message_placeholder",
            "submit_button_text",
            "form_background_image",
            "form_background_image_url",
            "form_bg_color",
            "contact_card_bg_color",
            "map_embed_url",
            "map_image",
            "map_image_url",
            "map_height",
            "success_message",
            "is_active",
        ]
        read_only_fields = [
            "form_background_image_url",
            "map_image_url",
        ]

    def get_form_background_image_url(self, obj):
        return self.absolute_media_url(obj.form_background_image)

    def get_map_image_url(self, obj):
        return self.absolute_media_url(obj.map_image)


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "message",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name is required.")
        return value.strip()

    def validate_message(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message is required.")
        return value.strip()


# -----------------------------
# BLOG PAGE SERIALIZERS
# -----------------------------
class BlogPageBannerSerializer(AbsoluteImageMixin, serializers.ModelSerializer):
    background_image_url = serializers.SerializerMethodField()

    class Meta:
        model = BlogPageBanner
        fields = [
            "id",
            "title",
            "breadcrumb_text",
            "background_image",
            "background_image_url",
            "is_active",
        ]
        read_only_fields = ["background_image_url"]

    def get_background_image_url(self, obj):
        return self.absolute_media_url(obj.background_image)


class BlogCategorySerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()

    class Meta:
        model = BlogCategory
        fields = [
            "id",
            "name",
            "slug",
            "sort_order",
            "is_active",
            "post_count",
        ]
        read_only_fields = ["slug", "post_count"]

    def get_post_count(self, obj):
        return obj.posts.filter(is_active=True).count()


class BlogPostSerializer(AbsoluteImageMixin, serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    category_name = serializers.CharField(source="category.name", read_only=True)
    category_slug = serializers.CharField(source="category.slug", read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            "id",
            "category",
            "category_name",
            "category_slug",
            "title",
            "slug",
            "image",
            "image_url",
            "excerpt",
            "author_name",
            "date_label",
            "comments_count",
            "is_video",
            "video_url",
            "read_more_text",
            "sort_order",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "slug",
            "image_url",
            "category_name",
            "category_slug",
            "created_at",
            "updated_at",
        ]

    def get_image_url(self, obj):
        return self.absolute_media_url(obj.image)


class BlogPopularTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPopularTag
        fields = [
            "id",
            "title",
            "filter_value",
            "sort_order",
            "is_active",
        ]


class BlogDiscountBannerSerializer(AbsoluteImageMixin, serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = BlogDiscountBanner
        fields = [
            "id",
            "discount_text",
            "subtitle",
            "button_text",
            "button_link",
            "image",
            "image_url",
            "is_active",
        ]
        read_only_fields = ["image_url"]

    def get_image_url(self, obj):
        return self.absolute_media_url(obj.image)


class BlogRecentPostSerializer(serializers.ModelSerializer):
    post = BlogPostSerializer(read_only=True)
    post_id = serializers.IntegerField(source="post.id", read_only=True)

    class Meta:
        model = BlogRecentPost
        fields = [
            "id",
            "post",
            "post_id",
            "sort_order",
            "is_active",
        ]


class BlogGalleryImageSerializer(AbsoluteImageMixin, serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = BlogGalleryImage
        fields = [
            "id",
            "title",
            "image",
            "image_url",
            "url",
            "sort_order",
            "is_active",
        ]
        read_only_fields = ["image_url"]

    def get_image_url(self, obj):
        return self.absolute_media_url(obj.image)


class BlogBrandLogoSerializer(AbsoluteImageMixin, serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = BlogBrandLogo
        fields = [
            "id",
            "title",
            "image",
            "image_url",
            "text_logo",
            "url",
            "sort_order",
            "is_active",
        ]
        read_only_fields = ["image_url"]

    def get_image_url(self, obj):
        return self.absolute_media_url(obj.image)


# -----------------------------
# NEWSLETTER + FOOTER SERIALIZERS
# -----------------------------
class NewsletterSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSection
        fields = [
            "id",
            "title",
            "subtitle",
            "placeholder_text",
            "button_text",
            "is_active",
        ]


class FooterSettingSerializer(AbsoluteImageMixin, serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = FooterSetting
        fields = [
            "id",
            "logo",
            "logo_url",
            "logo_text",
            "about_title",
            "about_text",
            "phone",
            "email",
            "facebook_url",
            "twitter_url",
            "pinterest_url",
            "instagram_url",
            "copyright_text",
            "show_payment_badges",
            "is_active",
        ]

        read_only_fields = [
            "logo_url",
        ]

    def get_logo_url(self, obj):
        return self.absolute_media_url(obj.logo)


class FooterLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterLink
        fields = [
            "id",
            "title",
            "url",
            "sort_order",
            "is_active",
        ]


class FooterColumnSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()

    class Meta:
        model = FooterColumn
        fields = [
            "id",
            "title",
            "sort_order",
            "is_active",
            "links",
        ]

    def get_links(self, obj):
        links = obj.links.filter(
            is_active=True
        ).order_by("sort_order", "id")

        return FooterLinkSerializer(
            links,
            many=True
        ).data


class FooterInstagramImageSerializer(
    AbsoluteImageMixin,
    serializers.ModelSerializer
):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = FooterInstagramImage
        fields = [
            "id",
            "title",
            "image",
            "image_url",
            "url",
            "sort_order",
            "is_active",
        ]

        read_only_fields = [
            "image_url",
        ]

    def get_image_url(self, obj):
        return self.absolute_media_url(obj.image)


class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = [
            "id",
            "email",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]


# -----------------------------
# CHECKOUT PAYMENT METHOD SERIALIZER
# -----------------------------
class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = [
            "id",
            "title",
            "method_type",
            "description",
            "icon",
            "sort_order",
            "is_active",
        ]


# -----------------------------
# CART SERIALIZER
# -----------------------------
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    item_total = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "product_id",
            "quantity",
            "item_total",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "product",
            "item_total",
            "created_at",
            "updated_at",
        ]

    def validate_product_id(self, value):
        product = Product.objects.filter(
            id=value,
            is_active=True
        ).first()

        if not product:
            raise serializers.ValidationError("Invalid product.")

        if product.stock <= 0:
            raise serializers.ValidationError("Product is out of stock.")

        return value

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")

        return value

    def create(self, validated_data):
        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Login required.")

        product_id = validated_data.pop("product_id")
        quantity = validated_data.get("quantity", 1)

        product = Product.objects.get(id=product_id)

        if product.stock < quantity:
            raise serializers.ValidationError(
                "Requested quantity is not available in stock."
            )

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={"quantity": quantity}
        )

        if not created:
            new_quantity = cart_item.quantity + quantity

            if product.stock < new_quantity:
                raise serializers.ValidationError(
                    "Requested quantity is not available in stock."
                )

            cart_item.quantity = new_quantity
            cart_item.save()

        return cart_item

    def update(self, instance, validated_data):
        quantity = validated_data.get("quantity", instance.quantity)

        if instance.product.stock < quantity:
            raise serializers.ValidationError(
                "Requested quantity is not available in stock."
            )

        instance.quantity = quantity
        instance.save()

        return instance


# -----------------------------
# ORDER SERIALIZERS
# -----------------------------
class OrderItemSerializer(serializers.ModelSerializer):
    item_total = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    product_image = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_image",
            "product_name",
            "price",
            "quantity",
            "item_total",
        ]

    def get_product_image(self, obj):
        request = self.context.get("request")

        if obj.product and obj.product.image:
            url = obj.product.image.url
            return request.build_absolute_uri(url) if request else url

        return None


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    coupon_code = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        trim_whitespace=True,
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "invoice_number",
            "user",
            "full_name",
            "phone",
            "email",
            "address",
            "city",
            "state",
            "pincode",
            "payment_method",
            "payment_status",
            "status",
            "tracking_status",
            "tracking_message",
            "cashfree_order_id",
            "cashfree_status",
            "total_amount",
            "shipping_charge",
            "discount_amount",
            "coupon_code",
            "order_note",
            "items",
            "created_at",
            "updated_at",
            "delivered_at",
        ]

        read_only_fields = [
            "id",
            "order_number",
            "invoice_number",
            "user",
            "payment_status",
            "status",
            "tracking_status",
            "tracking_message",
            "cashfree_order_id",
            "cashfree_status",
            "total_amount",
            "shipping_charge",
            "discount_amount",
            "items",
            "created_at",
            "updated_at",
            "delivered_at",
        ]

    def create(self, validated_data):
        request = self.context["request"]

        if not request.user or not request.user.is_authenticated:
            raise serializers.ValidationError("Login required to place order.")

        coupon_code = str(validated_data.pop("coupon_code", "") or "").strip()

        cart_items = CartItem.objects.filter(
            user=request.user
        ).select_related("product")

        if not cart_items.exists():
            raise serializers.ValidationError("Your cart is empty.")

        subtotal = Decimal("0.00")

        for item in cart_items:
            if item.product.stock < item.quantity:
                raise serializers.ValidationError(
                    f"{item.product.name} has only "
                    f"{item.product.stock} item(s) available."
                )

            subtotal += item.item_total

        discount_amount = Decimal("0.00")

        if coupon_code:
            coupon = CouponCode.objects.filter(
                code__iexact=coupon_code,
                is_active=True,
            ).first()

            if not coupon:
                raise serializers.ValidationError("Invalid coupon code.")

            if subtotal < coupon.minimum_order_amount:
                raise serializers.ValidationError(
                    f"Minimum order amount is ₹{coupon.minimum_order_amount}."
                )

            discount_amount = coupon.calculate_discount(subtotal)

        total = subtotal - discount_amount

        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            shipping_charge=Decimal("0.00"),
            discount_amount=discount_amount,
            payment_status="pending",
            status="pending",
            tracking_status="Order Placed",
            tracking_message="We will knock your door steps shortly.",
            **validated_data
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                price=item.product.price,
                quantity=item.quantity,
            )

            item.product.stock -= item.quantity
            item.product.save(update_fields=["stock"])

        cart_items.delete()

        return order