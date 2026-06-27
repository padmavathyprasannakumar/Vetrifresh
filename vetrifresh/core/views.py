from decimal import Decimal

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
import json
import uuid
from urllib import request as urllib_request
from urllib.error import HTTPError, URLError
from django.db.models import F, Q
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

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
    FooterSetting,
    InstagramImage,
    NavbarLink,
    NewsPost,
    NewsletterSection,
    Order,
    OrderItem,
    PaymentMethod,
    Product,
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

from .serializers import (
    AboutBrandLogoSerializer,
    AboutDeliverySectionSerializer,
    AboutFeatureItemSerializer,
    AboutFeatureSectionSerializer,
    AboutHeroSectionSerializer,
    AboutPageBannerSerializer,
    AboutTeamMemberSerializer,
    AboutTestimonialSerializer,
    BannerSerializer,
    BlogBrandLogoSerializer,
    BlogCategorySerializer,
    BlogDiscountBannerSerializer,
    BlogGalleryImageSerializer,
    BlogPageBannerSerializer,
    BlogPopularTagSerializer,
    BlogPostSerializer,
    BlogRecentPostSerializer,
    CartItemSerializer,
    CartPageBannerSerializer,
    CartRelatedProductSerializer,
    CouponCodeSerializer,
    CategorySerializer,
    ContactFormSettingSerializer,
    ContactInfoItemSerializer,
    ContactMessageSerializer,
    ContactPageBannerSerializer,
    FooterColumnSerializer,
    FooterInstagramImageSerializer,
    FooterSettingSerializer,
    InstagramImageSerializer,
    NavbarLinkSerializer,
    NewsPostSerializer,
    NewsletterSectionSerializer,
    NewsletterSubscriberSerializer,
    OrderSerializer,
    PaymentMethodSerializer,
    ProductSerializer,
    PromoCardSerializer,
    RegisterSerializer,
    SaleOfMonthBannerSerializer,
    ServiceFeatureSerializer,
    ShopDiscountBannerSerializer,
    ShopPageBannerSerializer,
    ShopPopularTagSerializer,
    ShopPriceFilterSerializer,
    ShopRatingFilterSerializer,
    ShopSaleProductSerializer,
    SiteSettingSerializer,
    TestimonialSerializer,
    UserSerializer,
    WishlistItemSerializer,
)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_staff)


def get_frontend_url(request):
    origin = request.headers.get("Origin", "")
    if origin:
        return origin.rstrip("/")

    frontend_url = getattr(settings, "FRONTEND_URL", "")
    return frontend_url.rstrip("/") or "http://localhost:5173"


def get_cashfree_base_url():
    env = str(getattr(settings, "CASHFREE_ENV", "sandbox")).lower()
    if env == "production":
        return "https://api.cashfree.com/pg"
    return "https://sandbox.cashfree.com/pg"


def cashfree_request(method, path, payload=None):
    client_id = getattr(settings, "CASHFREE_CLIENT_ID", "")
    client_secret = getattr(settings, "CASHFREE_CLIENT_SECRET", "")

    if not client_id or not client_secret:
        raise ValueError("Cashfree credentials missing. Add CASHFREE_CLIENT_ID and CASHFREE_CLIENT_SECRET.")

    url = f"{get_cashfree_base_url()}{path}"
    data = None

    if payload is not None:
        data = json.dumps(payload).encode("utf-8")

    req = urllib_request.Request(
        url=url,
        data=data,
        method=method.upper(),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-client-id": client_id,
            "x-client-secret": client_secret,
            "x-api-version": getattr(settings, "CASHFREE_API_VERSION", "2025-01-01"),
        },
    )

    try:
        with urllib_request.urlopen(req, timeout=30) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except HTTPError as exc:
        body = exc.read().decode("utf-8")
        try:
            parsed = json.loads(body)
        except Exception:
            parsed = {"message": body}
        raise ValueError(parsed.get("message") or parsed.get("detail") or str(parsed))
    except URLError as exc:
        raise ValueError(str(exc.reason))


def serialize_order(order, request):
    return OrderSerializer(order, context={"request": request}).data


# -----------------------------
# AUTH VIEWS
# -----------------------------
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


# -----------------------------
# SITE SETTING
# -----------------------------
class SiteSettingViewSet(viewsets.ModelViewSet):
    serializer_class = SiteSettingSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return SiteSetting.objects.all()

    def list(self, request, *args, **kwargs):
        site = SiteSetting.objects.first()

        if not site:
            return Response(None)

        return Response(
            self.get_serializer(
                site,
                context={"request": request}
            ).data
        )


# -----------------------------
# NAVBAR
# -----------------------------
class NavbarLinkViewSet(viewsets.ModelViewSet):
    serializer_class = NavbarLinkSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        qs = NavbarLink.objects.all().order_by("sort_order", "id")

        if not (self.request.user and self.request.user.is_staff):
            qs = qs.filter(is_active=True)

        return qs


class NavbarAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        site = SiteSetting.objects.first()

        links = NavbarLink.objects.filter(
            is_active=True
        ).order_by("sort_order", "id")

        categories = Category.objects.filter(
            is_active=True
        ).order_by("sort_order", "name")

        return Response({
            "site": SiteSettingSerializer(
                site,
                context={"request": request}
            ).data if site else None,

            "navbar_links": NavbarLinkSerializer(
                links,
                many=True,
                context={"request": request}
            ).data,

            "categories": CategorySerializer(
                categories,
                many=True,
                context={"request": request}
            ).data,
        })


# -----------------------------
# HOME PAGE API
# -----------------------------
class HomePageAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        ctx = {"request": request}

        site = SiteSetting.objects.first()

        links = NavbarLink.objects.filter(
            is_active=True
        ).order_by("sort_order", "id")

        categories = Category.objects.filter(
            is_active=True,
            show_in_home=True
        ).order_by("sort_order", "name")

        banners = Banner.objects.filter(
            is_active=True
        ).order_by("sort_order", "id")

        promo_cards = PromoCard.objects.filter(
            is_active=True
        ).order_by("sort_order", "id")

        services = ServiceFeature.objects.filter(
            is_active=True
        ).order_by("sort_order", "id")

        products = Product.objects.select_related(
            "category"
        ).prefetch_related(
            "gallery"
        ).filter(
            is_active=True
        )

        featured = products.filter(
            is_featured=True
        ).order_by("-created_at")[:12]

        popular = products.filter(
            is_popular=True
        ).order_by("-created_at")[:12]

        latest = products.order_by("-created_at")[:12]

        instagram = InstagramImage.objects.filter(
            is_active=True
        ).order_by("sort_order", "id")[:12]

        news = NewsPost.objects.filter(
            is_active=True
        ).order_by("sort_order", "id")[:6]

        testimonials = Testimonial.objects.filter(
            is_active=True
        ).order_by("sort_order", "id")[:8]

        return Response({
            "site": SiteSettingSerializer(site, context=ctx).data if site else None,
            "site_setting": SiteSettingSerializer(site, context=ctx).data if site else None,

            "navbar_links": NavbarLinkSerializer(
                links,
                many=True,
                context=ctx
            ).data,

            "categories": CategorySerializer(
                categories,
                many=True,
                context=ctx
            ).data,

            "banners": BannerSerializer(
                banners,
                many=True,
                context=ctx
            ).data,

            "promo_cards": PromoCardSerializer(
                promo_cards,
                many=True,
                context=ctx
            ).data,

            "service_features": ServiceFeatureSerializer(
                services,
                many=True,
                context=ctx
            ).data,

            "featured_products": ProductSerializer(
                featured,
                many=True,
                context=ctx
            ).data,

            "popular_products": ProductSerializer(
                popular,
                many=True,
                context=ctx
            ).data,

            "latest_products": ProductSerializer(
                latest,
                many=True,
                context=ctx
            ).data,

            "instagram_images": InstagramImageSerializer(
                instagram,
                many=True,
                context=ctx
            ).data,

            "news_posts": NewsPostSerializer(
                news,
                many=True,
                context=ctx
            ).data,

            "testimonials": TestimonialSerializer(
                testimonials,
                many=True,
                context=ctx
            ).data,
        })



# -----------------------------
# CART PAGE API
# Top banner + related products
# -----------------------------
class CartPageAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        ctx = {"request": request}

        banner = CartPageBanner.objects.filter(
            is_active=True
        ).first()

        related_products = CartRelatedProduct.objects.select_related(
            "product",
            "product__category"
        ).prefetch_related(
            "product__gallery"
        ).filter(
            is_active=True,
            product__is_active=True
        ).order_by("sort_order", "id")[:8]

        active_coupons = CouponCode.objects.filter(
            is_active=True
        ).order_by("code")[:12]

        return Response({
            "banner": CartPageBannerSerializer(
                banner,
                context=ctx
            ).data if banner else None,

            "related_products": CartRelatedProductSerializer(
                related_products,
                many=True,
                context=ctx
            ).data,

            "active_coupons": CouponCodeSerializer(
                active_coupons,
                many=True,
                context=ctx
            ).data,
        })


# -----------------------------
# COUPON APIs
# -----------------------------
class CouponListAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        coupons = CouponCode.objects.filter(
            is_active=True
        ).order_by("code")

        return Response({
            "coupons": CouponCodeSerializer(
                coupons,
                many=True,
                context={"request": request}
            ).data
        })


class CouponApplyAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        code = str(request.data.get("code", "")).strip().upper()

        if not code:
            return Response(
                {"detail": "Coupon code is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        coupon = CouponCode.objects.filter(
            code__iexact=code,
            is_active=True
        ).first()

        if not coupon:
            return Response(
                {"detail": "Invalid coupon code."},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_items = CartItem.objects.filter(
            user=request.user
        ).select_related("product")

        subtotal = sum(
            (item.item_total for item in cart_items),
            Decimal("0.00")
        )

        if subtotal <= 0:
            return Response(
                {"detail": "Your cart is empty."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if subtotal < coupon.minimum_order_amount:
            return Response(
                {
                    "detail": f"Minimum order amount is ₹{coupon.minimum_order_amount}.",
                    "minimum_order_amount": coupon.minimum_order_amount,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        discount_amount = coupon.calculate_discount(subtotal)
        total = subtotal - discount_amount

        return Response({
            "message": "Coupon applied successfully.",
            "coupon": CouponCodeSerializer(coupon).data,
            "code": coupon.code,
            "subtotal": subtotal,
            "discount_amount": discount_amount,
            "shipping": Decimal("0.00"),
            "total": total,
        })



# -----------------------------
# CHECKOUT PAGE + CASHFREE PAYMENT API
# -----------------------------
class CheckoutPageAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        methods = PaymentMethod.objects.filter(
            is_active=True
        ).order_by("sort_order", "id")

        if not methods.exists():
            default_methods = [
                {"title": "Cash on Delivery", "method_type": "Cash on Delivery", "description": "Pay when your order is delivered."},
                {"title": "Cashfree Online Payment", "method_type": "Cashfree", "description": "Pay securely using UPI, card, net banking or wallet."},
            ]
            return Response({"payment_methods": default_methods})

        return Response({
            "payment_methods": PaymentMethodSerializer(methods, many=True).data,
        })


class CashfreeCreateOrderAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart_items = CartItem.objects.filter(
            user=request.user
        ).select_related("product")

        if not cart_items.exists():
            return Response(
                {"detail": "Your cart is empty."},
                status=status.HTTP_400_BAD_REQUEST
            )

        required_fields = ["full_name", "phone", "address", "city", "pincode"]
        for field in required_fields:
            if not str(request.data.get(field, "")).strip():
                return Response(
                    {"detail": f"{field.replace('_', ' ').title()} is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        client_id = getattr(settings, "CASHFREE_CLIENT_ID", "")
        client_secret = getattr(settings, "CASHFREE_CLIENT_SECRET", "")

        if not client_id or not client_secret:
            return Response(
                {"detail": "Cashfree credentials missing. Add CASHFREE_CLIENT_ID and CASHFREE_CLIENT_SECRET in settings or Render environment variables."},
                status=status.HTTP_400_BAD_REQUEST
            )

        subtotal = Decimal("0.00")
        for item in cart_items:
            if item.product.stock < item.quantity:
                return Response(
                    {"detail": f"{item.product.name} has only {item.product.stock} item(s) available."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            subtotal += item.item_total

        coupon_code = str(request.data.get("coupon_code", "") or "").strip()
        discount_amount = Decimal("0.00")

        if coupon_code:
            coupon = CouponCode.objects.filter(
                code__iexact=coupon_code,
                is_active=True
            ).first()

            if not coupon:
                return Response(
                    {"detail": "Invalid coupon code."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if subtotal < coupon.minimum_order_amount:
                return Response(
                    {"detail": f"Minimum order amount is ₹{coupon.minimum_order_amount}."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            discount_amount = coupon.calculate_discount(subtotal)

        total = subtotal - discount_amount

        order = Order.objects.create(
            user=request.user,
            full_name=request.data.get("full_name"),
            phone=request.data.get("phone"),
            email=request.data.get("email", ""),
            address=request.data.get("address"),
            city=request.data.get("city"),
            state=request.data.get("state", ""),
            pincode=request.data.get("pincode"),
            payment_method="Cashfree",
            payment_status="pending",
            status="pending",
            tracking_status="Payment Pending",
            tracking_message="Please complete payment to confirm your order.",
            total_amount=total,
            shipping_charge=Decimal("0.00"),
            discount_amount=discount_amount,
            order_note=request.data.get("order_note", ""),
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                price=item.product.price,
                quantity=item.quantity,
            )

        cashfree_order_id = f"{order.order_number}-{uuid.uuid4().hex[:8]}"
        frontend_url = get_frontend_url(request)
        return_url = f"{frontend_url}/track-order/{order.order_number}?cashfree_order_id={{order_id}}"

        payload = {
            "order_id": cashfree_order_id,
            "order_amount": float(total),
            "order_currency": "INR",
            "customer_details": {
                "customer_id": str(request.user.id),
                "customer_name": order.full_name,
                "customer_email": order.email or f"customer{request.user.id}@example.com",
                "customer_phone": order.phone,
            },
            "order_meta": {
                "return_url": return_url,
            },
            "order_note": order.order_note or "VetriFresh order",
        }

        notify_url = getattr(settings, "CASHFREE_NOTIFY_URL", "")
        if notify_url:
            payload["order_meta"]["notify_url"] = notify_url

        try:
            cf_data = cashfree_request("POST", "/orders", payload)
        except ValueError as exc:
            order.payment_status = "failed"
            order.cashfree_status = str(exc)
            order.save(update_fields=["payment_status", "cashfree_status", "updated_at"])
            return Response(
                {"detail": str(exc), "order": serialize_order(order, request)},
                status=status.HTTP_400_BAD_REQUEST
            )

        payment_session_id = (
            cf_data.get("payment_session_id")
            or cf_data.get("payment_sessions_id")
            or ""
        )

        order.cashfree_order_id = cashfree_order_id
        order.cashfree_payment_session_id = payment_session_id
        order.cashfree_status = cf_data.get("order_status", "CREATED")
        order.save(update_fields=[
            "cashfree_order_id",
            "cashfree_payment_session_id",
            "cashfree_status",
            "updated_at",
        ])

        return Response({
            "order": serialize_order(order, request),
            "cashfree_order_id": cashfree_order_id,
            "payment_session_id": payment_session_id,
            "cashfree_mode": getattr(settings, "CASHFREE_ENV", "sandbox"),
        }, status=status.HTTP_201_CREATED)


class CashfreeVerifyAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, cashfree_order_id):
        order = Order.objects.filter(
            Q(cashfree_order_id=cashfree_order_id) |
            Q(order_number=cashfree_order_id)
        ).first()

        if not order:
            return Response(
                {"detail": "Order not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        cf_order_id = order.cashfree_order_id or cashfree_order_id

        try:
            cf_data = cashfree_request("GET", f"/orders/{cf_order_id}")
        except ValueError as exc:
            return Response(
                {"detail": str(exc), "order": serialize_order(order, request)},
                status=status.HTTP_400_BAD_REQUEST
            )

        cf_status = str(cf_data.get("order_status", "")).upper()
        order.cashfree_status = cf_status

        if cf_status in ["PAID", "SUCCESS"]:
            order.payment_status = "paid"
            order.status = "confirmed"
            order.tracking_status = "Order Confirmed"
            order.tracking_message = "Payment successful. We will knock your door steps shortly."

            for item in order.items.select_related("product"):
                if item.product and item.product.stock >= item.quantity:
                    item.product.stock -= item.quantity
                    item.product.save(update_fields=["stock"])

            CartItem.objects.filter(user=order.user).delete()

        elif cf_status in ["FAILED", "CANCELLED", "CANCELED", "USER_DROPPED", "EXPIRED"]:
            order.payment_status = "failed"
            order.status = "cancelled"
            order.tracking_status = "Payment Failed"
            order.tracking_message = "Payment was not completed. Please try again or choose Cash on Delivery."

        order.save(update_fields=[
            "payment_status",
            "status",
            "tracking_status",
            "tracking_message",
            "cashfree_status",
            "updated_at",
        ])

        return Response({
            "cashfree_status": cf_status,
            "order": serialize_order(order, request),
        })


class TrackOrderAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, identifier):
        order = Order.objects.filter(
            Q(order_number=identifier) |
            Q(invoice_number=identifier) |
            Q(cashfree_order_id=identifier) |
            Q(id=identifier if str(identifier).isdigit() else 0)
        ).prefetch_related("items", "items__product").first()

        if not order:
            return Response(
                {"detail": "Order not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        phone = str(request.query_params.get("phone", "")).strip()
        if phone:
            saved_phone = str(order.phone or "").replace(" ", "").strip()
            entered_phone = phone.replace(" ", "").strip()

            if saved_phone and saved_phone != entered_phone:
                return Response(
                    {"detail": "Phone number does not match this order."},
                    status=status.HTTP_404_NOT_FOUND
                )

        return Response({
            "order": serialize_order(order, request)
        })


class InvoiceAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, identifier):
        order = Order.objects.filter(
            Q(order_number=identifier) |
            Q(invoice_number=identifier) |
            Q(id=identifier if str(identifier).isdigit() else 0)
        ).prefetch_related("items", "items__product").first()

        if not order:
            return Response(
                {"detail": "Invoice not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response({
            "order": serialize_order(order, request)
        })


# -----------------------------
# CONTACT PAGE API
# -----------------------------
class ContactPageAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        ctx = {"request": request}

        banner = ContactPageBanner.objects.filter(
            is_active=True
        ).first()

        form_setting = ContactFormSetting.objects.filter(
            is_active=True
        ).first()

        info_items = ContactInfoItem.objects.filter(
            is_active=True
        ).order_by("sort_order", "id")

        return Response({
            "banner": ContactPageBannerSerializer(
                banner,
                context=ctx
            ).data if banner else None,

            "form_setting": ContactFormSettingSerializer(
                form_setting,
                context=ctx
            ).data if form_setting else None,

            "info_items": ContactInfoItemSerializer(
                info_items,
                many=True
            ).data,
        })


class ContactSubmitAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        message_obj = serializer.save()

        form_setting = ContactFormSetting.objects.filter(
            is_active=True
        ).first()

        default_recipient_email = getattr(
            settings,
            "CONTACT_RECEIVER_EMAIL",
            "padmavathyparasanna4@gmail.com"
        )

        recipient_email = default_recipient_email
        subject_prefix = "VetriFresh Contact Message"
        success_message = "Message sent successfully."

        if form_setting:
            recipient_email = form_setting.recipient_email or recipient_email
            subject_prefix = form_setting.email_subject_prefix or subject_prefix
            success_message = form_setting.success_message or success_message

        from_email = (
            getattr(settings, "DEFAULT_FROM_EMAIL", "")
            or getattr(settings, "EMAIL_HOST_USER", "")
            or default_recipient_email
        )

        subject = f"{subject_prefix} - {message_obj.name}"

        body = (
            "New contact message from VetriFresh website\n\n"
            f"Name: {message_obj.name}\n"
            f"Email: {message_obj.email}\n"
            f"Phone: {message_obj.phone or 'Not provided'}\n\n"
            f"Message:\n{message_obj.message}\n"
        )

        try:
            send_mail(
                subject=subject,
                message=body,
                from_email=from_email,
                recipient_list=[recipient_email],
                fail_silently=False,
            )

            message_obj.email_sent = True
            message_obj.email_error = ""
            message_obj.save(update_fields=[
                "email_sent",
                "email_error",
                "updated_at",
            ])

            return Response({
                "message": success_message,
                "email_sent": True,
            }, status=status.HTTP_201_CREATED)

        except Exception as exc:
            message_obj.email_sent = False
            message_obj.email_error = str(exc)
            message_obj.save(update_fields=[
                "email_sent",
                "email_error",
                "updated_at",
            ])

            return Response({
                "message": (
                    "Message saved, but email was not sent. "
                    "Please check SMTP environment variables."
                ),
                "email_sent": False,
                "email_error": str(exc),
            }, status=status.HTTP_202_ACCEPTED)


# -----------------------------
# ABOUT PAGE API
# -----------------------------
class AboutPageAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        ctx = {"request": request}

        banner = AboutPageBanner.objects.filter(is_active=True).first()
        hero = AboutHeroSection.objects.filter(is_active=True).first()
        feature_section = AboutFeatureSection.objects.filter(is_active=True).first()
        feature_items = AboutFeatureItem.objects.filter(is_active=True).order_by("sort_order", "id")[:8]
        delivery = AboutDeliverySection.objects.filter(is_active=True).first()
        team_members = AboutTeamMember.objects.filter(is_active=True).order_by("sort_order", "id")[:8]
        testimonials = AboutTestimonial.objects.filter(is_active=True).order_by("sort_order", "id")[:8]
        brand_logos = AboutBrandLogo.objects.filter(is_active=True).order_by("sort_order", "id")[:12]

        return Response({
            "banner": AboutPageBannerSerializer(banner, context=ctx).data if banner else None,
            "hero": AboutHeroSectionSerializer(hero, context=ctx).data if hero else None,
            "feature_section": AboutFeatureSectionSerializer(feature_section, context=ctx).data if feature_section else None,
            "feature_items": AboutFeatureItemSerializer(feature_items, many=True).data,
            "delivery": AboutDeliverySectionSerializer(delivery, context=ctx).data if delivery else None,
            "team_members": AboutTeamMemberSerializer(team_members, many=True, context=ctx).data,
            "testimonials": AboutTestimonialSerializer(testimonials, many=True, context=ctx).data,
            "brand_logos": AboutBrandLogoSerializer(brand_logos, many=True, context=ctx).data,
        })


# -----------------------------
# SHOP PAGE API
# Left sidebar + right products
# -----------------------------
class ShopPageAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, category_slug=None):
        ctx = {"request": request}

        banner = ShopPageBanner.objects.filter(
            is_active=True
        ).first()

        categories = Category.objects.filter(
            is_active=True
        ).order_by("sort_order", "name")

        price_filters = ShopPriceFilter.objects.filter(
            is_active=True
        ).order_by("sort_order", "id")

        rating_filters = ShopRatingFilter.objects.filter(
            is_active=True
        ).order_by("sort_order", "id")

        popular_tags = ShopPopularTag.objects.filter(
            is_active=True
        ).order_by("sort_order", "id")

        discount_banner = ShopDiscountBanner.objects.filter(
            is_active=True
        ).first()

        sale_products = ShopSaleProduct.objects.select_related(
            "product",
            "product__category"
        ).prefetch_related(
            "product__gallery"
        ).filter(
            is_active=True,
            product__is_active=True
        ).order_by("sort_order", "id")[:6]

        products = Product.objects.select_related(
            "category"
        ).prefetch_related(
            "gallery"
        ).filter(
            is_active=True
        )

        search = request.query_params.get("search")
        category = request.query_params.get("category")
        if not category and category_slug:
            category = category_slug
        min_price = request.query_params.get("min_price")
        max_price = request.query_params.get("max_price")
        rating = request.query_params.get("rating")
        tag = request.query_params.get("tag")
        sort = request.query_params.get("sort")

        current_category = None

        if search:
            products = products.filter(
                Q(name__icontains=search) |
                Q(short_description__icontains=search) |
                Q(description__icontains=search) |
                Q(tags__icontains=search) |
                Q(category__name__icontains=search)
            )

        if category:
            if str(category).isdigit():
                current_category = Category.objects.filter(
                    id=category,
                    is_active=True
                ).first()
            else:
                current_category = Category.objects.filter(
                    slug=category,
                    is_active=True
                ).first()

            if current_category:
                child_ids = list(
                    current_category.children.filter(
                        is_active=True
                    ).values_list("id", flat=True)
                )

                category_ids = [current_category.id] + child_ids
                products = products.filter(category_id__in=category_ids)

        if min_price:
            products = products.filter(price__gte=min_price)

        if max_price:
            products = products.filter(price__lte=max_price)

        if rating:
            products = products.filter(rating__gte=rating)

        if tag:
            products = products.filter(
                Q(tags__icontains=tag) |
                Q(name__icontains=tag) |
                Q(category__name__icontains=tag)
            )

        if sort == "price_low":
            products = products.order_by("price")
        elif sort == "price_high":
            products = products.order_by("-price")
        elif sort == "name":
            products = products.order_by("name")
        else:
            products = products.order_by("-created_at")

        total_products = products.count()

        try:
            page_size = int(request.query_params.get("page_size", 9))
        except (TypeError, ValueError):
            page_size = 9

        page_size = max(1, min(page_size, 60))

        try:
            page = int(request.query_params.get("page", 1))
        except (TypeError, ValueError):
            page = 1

        total_pages = max((total_products + page_size - 1) // page_size, 1)
        page = max(1, min(page, total_pages))
        start_index = (page - 1) * page_size
        end_index = start_index + page_size

        return Response({
            "banner": ShopPageBannerSerializer(
                banner,
                context=ctx
            ).data if banner else None,

            "categories": CategorySerializer(
                categories,
                many=True,
                context=ctx
            ).data,

            "price_filters": ShopPriceFilterSerializer(
                price_filters,
                many=True
            ).data,

            "rating_filters": ShopRatingFilterSerializer(
                rating_filters,
                many=True
            ).data,

            "popular_tags": ShopPopularTagSerializer(
                popular_tags,
                many=True
            ).data,

            "discount_banner": ShopDiscountBannerSerializer(
                discount_banner,
                context=ctx
            ).data if discount_banner else None,

            "sale_products": ShopSaleProductSerializer(
                sale_products,
                many=True,
                context=ctx
            ).data,

            "current_category": CategorySerializer(
                current_category,
                context=ctx
            ).data if current_category else None,

            "products": ProductSerializer(
                products[start_index:end_index],
                many=True,
                context=ctx
            ).data,

            "total_products": total_products,
            "pagination": {
                "current_page": page,
                "page_size": page_size,
                "total_pages": total_pages,
                "total_products": total_products,
                "has_previous": page > 1,
                "has_next": page < total_pages,
            },
        })




# -----------------------------
# BLOG PAGE API
# Left sidebar + right blog cards
# -----------------------------
class BlogPageAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, category_slug=None):
        ctx = {"request": request}

        banner = BlogPageBanner.objects.filter(
            is_active=True
        ).first()

        categories = BlogCategory.objects.filter(
            is_active=True
        ).order_by("sort_order", "name")

        popular_tags = BlogPopularTag.objects.filter(
            is_active=True
        ).order_by("sort_order", "id")

        discount_banner = BlogDiscountBanner.objects.filter(
            is_active=True
        ).first()

        recent_posts = BlogRecentPost.objects.select_related(
            "post",
            "post__category"
        ).filter(
            is_active=True,
            post__is_active=True
        ).order_by("sort_order", "id")[:5]

        gallery_images = BlogGalleryImage.objects.filter(
            is_active=True
        ).order_by("sort_order", "id")[:9]

        brand_logos = BlogBrandLogo.objects.filter(
            is_active=True
        ).order_by("sort_order", "id")[:8]

        posts = BlogPost.objects.select_related(
            "category"
        ).filter(
            is_active=True
        )

        search = request.query_params.get("search")
        category = request.query_params.get("category")
        if not category and category_slug:
            category = category_slug
        tag = request.query_params.get("tag")
        sort = request.query_params.get("sort")

        current_category = None

        if search:
            posts = posts.filter(
                Q(title__icontains=search) |
                Q(excerpt__icontains=search) |
                Q(author_name__icontains=search) |
                Q(category__name__icontains=search)
            )

        if category:
            if str(category).isdigit():
                current_category = BlogCategory.objects.filter(
                    id=category,
                    is_active=True
                ).first()
            else:
                current_category = BlogCategory.objects.filter(
                    slug=category,
                    is_active=True
                ).first()

            if current_category:
                posts = posts.filter(category=current_category)

        if tag:
            posts = posts.filter(
                Q(title__icontains=tag) |
                Q(excerpt__icontains=tag) |
                Q(category__name__icontains=tag)
            )

        if sort == "oldest":
            posts = posts.order_by("created_at")
        elif sort == "name":
            posts = posts.order_by("title")
        elif sort == "comments":
            posts = posts.order_by("-comments_count")
        else:
            posts = posts.order_by("sort_order", "-created_at")

        total_posts = posts.count()

        return Response({
            "banner": BlogPageBannerSerializer(
                banner,
                context=ctx
            ).data if banner else None,

            "categories": BlogCategorySerializer(
                categories,
                many=True
            ).data,

            "popular_tags": BlogPopularTagSerializer(
                popular_tags,
                many=True
            ).data,

            "discount_banner": BlogDiscountBannerSerializer(
                discount_banner,
                context=ctx
            ).data if discount_banner else None,

            "recent_posts": BlogRecentPostSerializer(
                recent_posts,
                many=True,
                context=ctx
            ).data,

            "gallery_images": BlogGalleryImageSerializer(
                gallery_images,
                many=True,
                context=ctx
            ).data,

            "brand_logos": BlogBrandLogoSerializer(
                brand_logos,
                many=True,
                context=ctx
            ).data,

            "current_category": BlogCategorySerializer(
                current_category
            ).data if current_category else None,

            "posts": BlogPostSerializer(
                posts[:24],
                many=True,
                context=ctx
            ).data,

            "total_posts": total_posts,
        })


# -----------------------------
# FOOTER + NEWSLETTER API
# Sale of Month Banner added here
# -----------------------------
class FooterAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        ctx = {"request": request}

        sale_banner = SaleOfMonthBanner.objects.filter(
            is_active=True
        ).order_by("sort_order", "id").first()

        newsletter = NewsletterSection.objects.filter(
            is_active=True
        ).first()

        footer = FooterSetting.objects.filter(
            is_active=True
        ).first()

        columns = FooterColumn.objects.filter(
            is_active=True
        ).order_by("sort_order", "id")

        instagram_images = FooterInstagramImage.objects.filter(
            is_active=True
        ).order_by("sort_order", "id")[:8]

        return Response({
            "sale_banner": SaleOfMonthBannerSerializer(
                sale_banner,
                context=ctx
            ).data if sale_banner else None,

            "sale_of_month_banner": SaleOfMonthBannerSerializer(
                sale_banner,
                context=ctx
            ).data if sale_banner else None,

            "newsletter": NewsletterSectionSerializer(
                newsletter
            ).data if newsletter else None,

            "footer": FooterSettingSerializer(
                footer,
                context=ctx
            ).data if footer else None,

            "columns": FooterColumnSerializer(
                columns,
                many=True
            ).data,

            "instagram_images": FooterInstagramImageSerializer(
                instagram_images,
                many=True,
                context=ctx
            ).data,
        })


class NewsletterSubscribeAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = NewsletterSubscriberSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {"message": "Subscribed successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# -----------------------------
# CATEGORY
# -----------------------------
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"

    def get_queryset(self):
        qs = Category.objects.all().order_by("sort_order", "name")

        if not (self.request.user and self.request.user.is_staff):
            qs = qs.filter(is_active=True)

        search = self.request.query_params.get("search")
        show_home = self.request.query_params.get("show_in_home")

        if search:
            qs = qs.filter(name__icontains=search)

        if show_home in ["1", "true", "True"]:
            qs = qs.filter(show_in_home=True)

        return qs


# -----------------------------
# BANNERS
# -----------------------------
class BannerViewSet(viewsets.ModelViewSet):
    serializer_class = BannerSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        qs = Banner.objects.all().order_by("sort_order", "id")

        if not (self.request.user and self.request.user.is_staff):
            qs = qs.filter(is_active=True)

        banner_type = self.request.query_params.get("type")

        if banner_type:
            qs = qs.filter(banner_type=banner_type)

        return qs


# -----------------------------
# PROMO CARDS
# -----------------------------
class PromoCardViewSet(viewsets.ModelViewSet):
    serializer_class = PromoCardSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        qs = PromoCard.objects.all().order_by("sort_order", "id")

        if not (self.request.user and self.request.user.is_staff):
            qs = qs.filter(is_active=True)

        return qs


# -----------------------------
# SERVICE FEATURES
# -----------------------------
class ServiceFeatureViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceFeatureSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        qs = ServiceFeature.objects.all().order_by("sort_order", "id")

        if not (self.request.user and self.request.user.is_staff):
            qs = qs.filter(is_active=True)

        return qs


# -----------------------------
# INSTAGRAM
# -----------------------------
class InstagramImageViewSet(viewsets.ModelViewSet):
    serializer_class = InstagramImageSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        qs = InstagramImage.objects.all().order_by("sort_order", "id")

        if not (self.request.user and self.request.user.is_staff):
            qs = qs.filter(is_active=True)

        return qs


# -----------------------------
# NEWS POSTS
# -----------------------------
class NewsPostViewSet(viewsets.ModelViewSet):
    serializer_class = NewsPostSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        qs = NewsPost.objects.all().order_by("sort_order", "id")

        if not (self.request.user and self.request.user.is_staff):
            qs = qs.filter(is_active=True)

        return qs


# -----------------------------
# TESTIMONIALS
# -----------------------------
class TestimonialViewSet(viewsets.ModelViewSet):
    serializer_class = TestimonialSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        qs = Testimonial.objects.all().order_by("sort_order", "id")

        if not (self.request.user and self.request.user.is_staff):
            qs = qs.filter(is_active=True)

        return qs


# -----------------------------
# PRODUCTS
# -----------------------------
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "id"

    def get_queryset(self):
        qs = Product.objects.select_related(
            "category"
        ).prefetch_related(
            "gallery"
        ).all()

        if not (self.request.user and self.request.user.is_staff):
            qs = qs.filter(is_active=True)

        search = self.request.query_params.get("search")
        category = self.request.query_params.get("category")
        featured = self.request.query_params.get("featured")
        popular = self.request.query_params.get("popular")
        sort = self.request.query_params.get("sort")
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")
        rating = self.request.query_params.get("rating")
        tag = self.request.query_params.get("tag")

        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(short_description__icontains=search) |
                Q(description__icontains=search) |
                Q(tags__icontains=search) |
                Q(category__name__icontains=search)
            )

        if category:
            if str(category).isdigit():
                qs = qs.filter(category_id=category)
            else:
                qs = qs.filter(category__slug=category)

        if featured in ["1", "true", "True"]:
            qs = qs.filter(is_featured=True)

        if popular in ["1", "true", "True"]:
            qs = qs.filter(is_popular=True)

        if min_price:
            qs = qs.filter(price__gte=min_price)

        if max_price:
            qs = qs.filter(price__lte=max_price)

        if rating:
            qs = qs.filter(rating__gte=rating)

        if tag:
            qs = qs.filter(
                Q(tags__icontains=tag) |
                Q(name__icontains=tag) |
                Q(category__name__icontains=tag)
            )

        if sort == "price_low":
            qs = qs.order_by("price")
        elif sort == "price_high":
            qs = qs.order_by("-price")
        elif sort == "name":
            qs = qs.order_by("name")
        else:
            qs = qs.order_by("-created_at")

        return qs

    @action(detail=True, methods=["get"])
    def related(self, request, id=None):
        product = self.get_object()

        qs = Product.objects.select_related(
            "category"
        ).prefetch_related(
            "gallery"
        ).filter(
            category=product.category,
            is_active=True
        ).exclude(
            id=product.id
        )[:8]

        return Response(
            self.get_serializer(
                qs,
                many=True,
                context={"request": request}
            ).data
        )


# -----------------------------
# WISHLIST
# -----------------------------
class WishlistItemViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WishlistItem.objects.filter(
            user=self.request.user
        ).select_related(
            "product",
            "product__category"
        ).prefetch_related(
            "product__gallery"
        ).order_by("-created_at")

    def create(self, request, *args, **kwargs):
        product_id = request.data.get("product_id") or request.data.get("product")

        if not product_id:
            return Response(
                {"detail": "product_id is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        product = Product.objects.filter(
            id=product_id,
            is_active=True
        ).first()

        if not product:
            return Response(
                {"detail": "Invalid product."},
                status=status.HTTP_400_BAD_REQUEST
            )

        item, created = WishlistItem.objects.get_or_create(
            user=request.user,
            product=product
        )

        serializer = self.get_serializer(
            item,
            context={"request": request}
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )

    @action(detail=False, methods=["post"])
    def toggle(self, request):
        product_id = request.data.get("product_id") or request.data.get("product")

        if not product_id:
            return Response(
                {"detail": "product_id is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        product = Product.objects.filter(
            id=product_id,
            is_active=True
        ).first()

        if not product:
            return Response(
                {"detail": "Invalid product."},
                status=status.HTTP_400_BAD_REQUEST
            )

        item = WishlistItem.objects.filter(
            user=request.user,
            product=product
        ).first()

        if item:
            item.delete()
            return Response({
                "detail": "Removed from wishlist",
                "in_wishlist": False,
                "product_id": product.id,
            })

        item = WishlistItem.objects.create(
            user=request.user,
            product=product
        )

        return Response({
            "detail": "Added to wishlist",
            "in_wishlist": True,
            "product_id": product.id,
            "item": WishlistItemSerializer(
                item,
                context={"request": request}
            ).data,
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"])
    def clear(self, request):
        self.get_queryset().delete()

        return Response({
            "detail": "Wishlist cleared successfully."
        })


# -----------------------------
# CART
# -----------------------------
class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(
            user=self.request.user
        ).select_related(
            "product",
            "product__category"
        ).prefetch_related(
            "product__gallery"
        )

    def cleanup_unavailable_items(self):
        # Remove stale cart rows that can no longer be purchased. This also
        # cleans rows that may have been created by older add-to-cart code
        # before stock validation happened.
        CartItem.objects.filter(
            user=self.request.user
        ).filter(
            Q(product__is_active=False) |
            Q(product__stock__lte=0) |
            Q(quantity__gt=F("product__stock"))
        ).delete()

    def list(self, request, *args, **kwargs):
        self.cleanup_unavailable_items()
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        product_id = request.data.get("product_id") or request.data.get("product")
        quantity = request.data.get("quantity", 1)

        try:
            quantity = int(quantity)
        except ValueError:
            return Response(
                {"detail": "Quantity must be a valid number."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not product_id:
            return Response(
                {"detail": "product_id is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        product = Product.objects.filter(
            id=product_id,
            is_active=True
        ).first()

        if not product:
            return Response(
                {"detail": "Invalid product."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if quantity < 1:
            return Response(
                {"detail": "Quantity must be at least 1."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if product.stock <= 0:
            return Response(
                {"detail": f"Only {product.stock} item(s) available in stock."},
                status=status.HTTP_400_BAD_REQUEST
            )

        existing_item = CartItem.objects.filter(
            user=request.user,
            product=product
        ).first()

        requested_quantity = quantity + (existing_item.quantity if existing_item else 0)

        if requested_quantity > product.stock:
            return Response(
                {"detail": f"Only {product.stock} item(s) available in stock."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if existing_item:
            item = existing_item
            item.quantity = requested_quantity
            item.save(update_fields=["quantity", "updated_at"])
        else:
            item = CartItem.objects.create(
                user=request.user,
                product=product,
                quantity=quantity
            )

        return Response(
            self.get_serializer(
                item,
                context={"request": request}
            ).data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        item = self.get_object()
        quantity = request.data.get("quantity", item.quantity)

        try:
            quantity = int(quantity)
        except ValueError:
            return Response(
                {"detail": "Quantity must be a valid number."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if quantity < 1:
            return Response(
                {"detail": "Quantity must be at least 1."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if quantity > item.product.stock:
            return Response(
                {"detail": f"Only {item.product.stock} item(s) available in stock."},
                status=status.HTTP_400_BAD_REQUEST
            )

        item.quantity = quantity
        item.save(update_fields=["quantity", "updated_at"])

        return Response(
            self.get_serializer(
                item,
                context={"request": request}
            ).data
        )

    @action(detail=False, methods=["post"])
    def clear(self, request):
        self.get_queryset().delete()

        return Response({
            "detail": "Cart cleared successfully."
        })

    @action(detail=False, methods=["get"])
    def summary(self, request):
        self.cleanup_unavailable_items()
        items = self.get_queryset()

        total = sum(item.item_total for item in items)
        count = sum(item.quantity for item in items)

        return Response({
            "count": count,
            "total": total
        })


# -----------------------------
# ORDERS
# -----------------------------
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        ).prefetch_related(
            "items",
            "items__product"
        ).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save()