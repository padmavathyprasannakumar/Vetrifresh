from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from core.models import (
    Banner, Category, InstagramImage, NavbarLink, NewsPost, Product, PromoCard,
    ServiceFeature, SiteSetting, Testimonial,
)


def svg_file(title, color='#00B207', text_color='#ffffff', width=800, height=500):
    safe = title.replace('&', '&amp;')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{color}"/><stop offset="1" stop-color="#84D187"/></linearGradient></defs>
<rect width="100%" height="100%" fill="url(#g)"/>
<circle cx="{width-120}" cy="110" r="90" fill="rgba(255,255,255,.25)"/>
<circle cx="120" cy="{height-95}" r="65" fill="rgba(255,255,255,.2)"/>
<text x="50%" y="48%" text-anchor="middle" font-family="Arial" font-size="42" font-weight="700" fill="{text_color}">{safe}</text>
<text x="50%" y="60%" text-anchor="middle" font-family="Arial" font-size="22" fill="{text_color}">VetriFresh Organic</text>
</svg>'''
    return ContentFile(svg.encode('utf-8'), name=f'{slugify(title) or "image"}.svg')


class Command(BaseCommand):
    help = 'Create VetriFresh demo data for admin/API/frontend testing.'

    def handle(self, *args, **options):
        site, _ = SiteSetting.objects.get_or_create(site_name='VetriFresh')
        site.phone = '+91 93738 34940'
        site.currency_symbol = '₹'
        site.currency_code = 'INR'
        site.language = 'Eng'
        site.location_placeholder = 'Pincode'
        if not site.logo:
            site.logo.save('vetrifresh-logo.svg', svg_file('VetriFresh', '#ffffff', '#2C742F', 420, 120), save=False)
        site.save()

        for order, title, url, dropdown in [
            (1, 'Shop', '/shop', True),
            (2, 'Blog', '/blog', False),
            (3, 'About Us', '/about', False),
            (4, 'Contact Us', '/contact', False),
        ]:
            NavbarLink.objects.update_or_create(
                title=title,
                defaults={'url': url, 'sort_order': order, 'is_category_dropdown': dropdown, 'is_active': True},
            )

        categories = []
        category_data = [
            ('Fresh Fruit', '#b3e35b'), ('Fresh Vegetables', '#00B207'), ('Meat & Fish', '#d86565'),
            ('Snacks', '#f0bd49'), ('Beverages', '#63b8ff'), ('Beauty & Health', '#ff91c8'),
            ('Bread & Bakery', '#d2a26f'), ('Baking Needs', '#a879d8'), ('Cooking', '#ffd15c'),
            ('Diabetic Food', '#abe7ff'), ('Dish Detergents', '#81d686'), ('Oil', '#ffd24d'),
        ]
        for idx, (name, color) in enumerate(category_data, start=1):
            cat, created = Category.objects.update_or_create(
                slug=slugify(name),
                defaults={'name': name, 'sort_order': idx, 'is_active': True, 'show_in_home': True},
            )
            if not cat.image:
                cat.image.save(f'{slugify(name)}.svg', svg_file(name, color, '#002603', 320, 240), save=True)
            categories.append(cat)

        def make_banner(title, btype, color, text, order, subtitle='', badge='', discount='', size=(980, 520)):
            b, _ = Banner.objects.update_or_create(
                title=title,
                banner_type=btype,
                defaults={
                    'subtitle': subtitle,
                    'badge': badge,
                    'discount_label': discount,
                    'button_text': 'Shop Now',
                    'button_link': '/shop',
                    'bg_color': color,
                    'text_color': text,
                    'is_active': True,
                    'sort_order': order,
                },
            )
            if not b.image:
                b.image.save(f'{slugify(title)}.svg', svg_file(title, color, text, size[0], size[1]), save=True)
            return b

        make_banner('Fresh & Healthy Organic Food', 'main', '#00B207', '#FFFFFF', 1, 'Free shipping on all your order.', 'Sale up to', '30% OFF')
        make_banner('75% OFF', 'side', '#f7f7f7', '#000000', 2, 'Only Fruit & Vegetable', 'Summer Sale', '')
        make_banner('Special Products Deal of the Month', 'side', '#002603', '#FFFFFF', 3, 'Best Deal', 'Best Deal', '')
        make_banner('Get ₹100 Off On Your First Order', 'wide', '#84D187', '#002603', 4, 'Freshness Score Guaranteed Quality Products', '', '')
        make_banner('Flash Sale - Today Only', 'wide', '#2C742F', '#FFFFFF', 5, 'From 9 AM - 10 AM!', '', '')

        for idx, (title, subtitle, badge, color) in enumerate([
            ('Sale of the Month', '00 : 02 : 18 : 46', 'Best Deals', '#002603'),
            ('Low-Fat Meat', 'Started at ₹79.99', '85% Fat Free', '#000000'),
            ('100% Fresh Fruit', 'Up to 64% OFF', 'Summer Sale', '#FFD400'),
        ], start=1):
            promo, _ = PromoCard.objects.update_or_create(
                title=title,
                defaults={'subtitle': subtitle, 'badge': badge, 'bg_color': color, 'text_color': '#000000' if color == '#FFD400' else '#FFFFFF', 'is_active': True, 'sort_order': idx},
            )
            if not promo.image:
                promo.image.save(f'{slugify(title)}.svg', svg_file(title, color, '#000000' if color == '#FFD400' else '#FFFFFF', 480, 520), save=True)

        for idx, (icon, title, subtitle) in enumerate([
            ('🚚', 'Free Shipping', 'Free shipping on all your order'),
            ('🎧', 'Customer Support 24/7', 'Instant access to Support'),
            ('🔒', '100% Secure Payment', 'We ensure your money is safe'),
            ('📦', 'Money-Back Guarantee', '30 Days Money-Back Guarantee'),
        ], start=1):
            ServiceFeature.objects.update_or_create(title=title, defaults={'icon': icon, 'subtitle': subtitle, 'is_active': True, 'sort_order': idx})

        products = [
            ('Green Apple', categories[0], 199, 320.99, '#b6e84d'),
            ('Orange Imported', categories[0], 300, 320.99, '#ff9b21'),
            ('Chinese Cabbage', categories[1], 50, 90.99, '#00B207'),
            ('Green Lettuce', categories[1], 90, 180.99, '#62cf55'),
            ('Big Potatoes', categories[1], 30, 32.99, '#d6b56b'),
            ('Brinjal / Eggplant', categories[1], 300, 320.99, '#351457'),
            ('Fresh Cauliflower', categories[1], 30, 32.99, '#e4e0ba'),
            ('Fresh Capsicum', categories[1], 30, 32.99, '#6bb65d'),
        ]
        for name, cat, price, old, color in products:
            prod, _ = Product.objects.update_or_create(
                slug=slugify(name),
                defaults={
                    'name': name, 'category': cat, 'price': price, 'old_price': old, 'sale_label': 'Sale 50%',
                    'short_description': f'Fresh organic {name}.', 'description': f'{name} is selected and packed fresh for VetriFresh customers.',
                    'stock': 50, 'rating': 4.5, 'reviews_count': 4, 'tags': f'{cat.name}, fresh, organic',
                    'is_active': True, 'is_featured': True, 'is_popular': True,
                },
            )
            if not prod.image:
                prod.image.save(f'{slugify(name)}.svg', svg_file(name, color, '#002603', 500, 420), save=True)

        for idx, name in enumerate(['Tomatoes', 'Leaves', 'Bitter Gourd', 'Capsicum', 'Spinach', 'Orange Water'], start=1):
            img, _ = InstagramImage.objects.update_or_create(title=name, defaults={'is_active': True, 'sort_order': idx, 'instagram_url': 'https://instagram.com/'})
            if not img.image:
                img.image.save(f'instagram-{idx}.svg', svg_file(name, ['#d93434','#2C742F','#84D187','#ff8a00','#00B207','#9de8ff'][idx-1], '#ffffff', 240, 240), save=True)

        for idx, title in enumerate(['Benefits Of Orange Juice For Skin and Health', 'Protein Rich Food for Dieting', 'Rich in minerals found in the Veggies'], start=1):
            news, _ = NewsPost.objects.update_or_create(title=title, defaults={'excerpt': 'Read our latest healthy food tips from VetriFresh.', 'date_label': f'{18+idx} NOV', 'is_active': True, 'sort_order': idx})
            if not news.image:
                news.image.save(f'news-{idx}.svg', svg_file(title, ['#ff9b21','#2C742F','#84D187'][idx-1], '#ffffff', 420, 260), save=True)

        for idx, name in enumerate(['Ananth', 'Krishna Kumar', 'Suresh'], start=1):
            Testimonial.objects.update_or_create(
                name=name,
                defaults={'role': 'Customer', 'message': 'The freshness score feature is something I have never seen before. I know exactly where my vegetables come from and how fresh they are.', 'rating': 5, 'is_active': True, 'sort_order': idx},
            )

        self.stdout.write(self.style.SUCCESS('VetriFresh demo data created successfully.'))
