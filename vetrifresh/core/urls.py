from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    AboutPageAPIView,
    BannerViewSet,
    BlogPageAPIView,
    CartItemViewSet,
    CartPageAPIView,
    CashfreeCreateOrderAPIView,
    CashfreeVerifyAPIView,
    CategoryViewSet,
    CheckoutPageAPIView,
    ContactPageAPIView,
    ContactSubmitAPIView,
    CouponApplyAPIView,
    CouponListAPIView,
    FooterAPIView,
    HomePageAPIView,
    InstagramImageViewSet,
    InvoiceAPIView,
    MeView,
    NavbarAPIView,
    NavbarLinkViewSet,
    NewsPostViewSet,
    NewsletterSubscribeAPIView,
    OrderViewSet,
    ProductViewSet,
    PromoCardViewSet,
    RegisterView,
    ServiceFeatureViewSet,
    ShopPageAPIView,
    SiteSettingViewSet,
    TestimonialViewSet,
    TrackOrderAPIView,
    WishlistItemViewSet,
)


router = DefaultRouter()

router.register("site-setting", SiteSettingViewSet, basename="site-setting")
router.register("navbar-links", NavbarLinkViewSet, basename="navbar-links")
router.register("categories", CategoryViewSet, basename="categories")
router.register("banners", BannerViewSet, basename="banners")
router.register("promo-cards", PromoCardViewSet, basename="promo-cards")
router.register("service-features", ServiceFeatureViewSet, basename="service-features")
router.register("instagram-images", InstagramImageViewSet, basename="instagram-images")
router.register("news-posts", NewsPostViewSet, basename="news-posts")
router.register("testimonials", TestimonialViewSet, basename="testimonials")
router.register("products", ProductViewSet, basename="products")
router.register("cart", CartItemViewSet, basename="cart")
router.register("wishlist", WishlistItemViewSet, basename="wishlist")
router.register("orders", OrderViewSet, basename="orders")


urlpatterns = [
    # Authentication
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/me/", MeView.as_view(), name="me"),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Common layout APIs
    path("navbar/", NavbarAPIView.as_view(), name="navbar"),
    path("footer/", FooterAPIView.as_view(), name="footer"),

    # Page APIs
    path("home/", HomePageAPIView.as_view(), name="home-page"),

    path("shop-page/", ShopPageAPIView.as_view(), name="shop-page"),
    path("shop-page/category/<slug:category_slug>/", ShopPageAPIView.as_view(), name="shop-page-category"),

    path("blog-page/", BlogPageAPIView.as_view(), name="blog-page"),
    path("blog-page/category/<slug:category_slug>/", BlogPageAPIView.as_view(), name="blog-page-category"),

    path("about-page/", AboutPageAPIView.as_view(), name="about-page"),
    path("contact-page/", ContactPageAPIView.as_view(), name="contact-page"),
    path("checkout-page/", CheckoutPageAPIView.as_view(), name="checkout-page"),
    path("cart-page/", CartPageAPIView.as_view(), name="cart-page"),

    # Short aliases for frontend routes
    path("about/", AboutPageAPIView.as_view(), name="about"),
    path("contact/", ContactPageAPIView.as_view(), name="contact"),
    path("checkout/", CheckoutPageAPIView.as_view(), name="checkout"),
    path("cart-view/", CartPageAPIView.as_view(), name="cart-view"),
    path("shop/", ShopPageAPIView.as_view(), name="shop"),
    path("shop/category/<slug:category_slug>/", ShopPageAPIView.as_view(), name="shop-category"),
    path("blog/", BlogPageAPIView.as_view(), name="blog"),
    path("blog/category/<slug:category_slug>/", BlogPageAPIView.as_view(), name="blog-category"),

    # Contact / newsletter
    path("contact/submit/", ContactSubmitAPIView.as_view(), name="contact-submit"),
    path("newsletter/subscribe/", NewsletterSubscribeAPIView.as_view(), name="newsletter-subscribe"),

    # Payments
    path("payments/cashfree/create/", CashfreeCreateOrderAPIView.as_view(), name="cashfree-create-order"),
    path("payments/cashfree/verify/<str:cashfree_order_id>/", CashfreeVerifyAPIView.as_view(), name="cashfree-verify"),

    # Orders
    path("track-order/<str:identifier>/", TrackOrderAPIView.as_view(), name="track-order"),
    path("invoice/<str:identifier>/", InvoiceAPIView.as_view(), name="invoice"),

    # Coupons
    path("coupons/", CouponListAPIView.as_view(), name="coupon-list"),
    path("coupon/apply/", CouponApplyAPIView.as_view(), name="coupon-apply"),

    # DRF router APIs
    path("", include(router.urls)),
]