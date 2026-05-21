from decimal import Decimal
import random

from playitloud.core.database import SessionLocal

from playitloud.models.user import User
from playitloud.models.address import Address
from playitloud.models.artist import Artist
from playitloud.models.album import Album, MediaType
from playitloud.models.order import Order, OrderStatus
from playitloud.models.order_item import OrderItem
from playitloud.models.invoice import Invoice
from playitloud.models.supplier import Supplier
from playitloud.models.supplier_offer import SupplierOffer
from playitloud.models.supplier_order import SupplierOrder, RestockStatus
from playitloud.models.supplier_order_item import SupplierOrderItem

def seed():
    session = SessionLocal()

    try:
        print("🌱 Starting seed...")

        # =========================================================
        # 👤 USERS
        # =========================================================
        users = [
            User(
                email=f"user{i}@mail.com",
                password_hash="hashed_password",
                first_name=f"User{i}",
                last_name="Test",
            )
            for i in range(1, 16)
        ]

        session.add_all(users)
        session.flush()

        # =========================================================
        # 🏠 ADDRESSES
        # =========================================================
        cities = ["Bruxelles", "Liège", "Namur", "Charleroi", "Mons"]

        addresses = []
        for i, user in enumerate(users):
            for _ in range(random.randint(1, 2)):
                addresses.append(
                    Address(
                        user_id=user.id,
                        street=f"{random.randint(1, 200)} Rue de la Musique",
                        city=random.choice(cities),
                        postal_code=str(random.randint(1000, 9999)),
                        country_code="BE",
                    )
                )

        session.add_all(addresses)
        session.flush()

        # =========================================================
        # 🎸 ARTISTS (16)
        # =========================================================
        artists = [
            Artist(name="Metallica", description="Heavy metal legends"),
            Artist(name="Nirvana", description="Grunge pioneers"),
            Artist(name="David Bowie", description="Rock icon and musical innovator"),
            Artist(name="Pink Floyd", description="Progressive rock icons"),
            Artist(name="Daft Punk", description="French electronic duo"),
            Artist(name="Radiohead", description="Alternative rock band"),
            Artist(name="The Beatles", description="Classic rock band"),
            Artist(name="Led Zeppelin", description="Hard rock pioneers"),
            Artist(name="Queen", description="British rock band"),
            Artist(name="Kendrick Lamar", description="Hip-hop artist"),
            Artist(name="Drake", description="Rap superstar"),
            Artist(name="The Weeknd", description="R&B / pop artist"),
            Artist(name="Eminem", description="Rap legend"),
            Artist(name="Miles Davis", description="Jazz trumpeter"),
            Artist(name="Hans Zimmer", description="Film composer"),
            Artist(name="Arctic Monkeys", description="Indie rock band"),
        ]

        session.add_all(artists)
        session.flush()

        # =========================================================
        # 💿 ALBUMS (23)
        # =========================================================
        albums = [
            Album(name="Master of Puppets", media_type=MediaType.VINYL, price=Decimal("29.99"), stock=12),
            Album(name="Ride the Lightning", media_type=MediaType.VINYL, price=Decimal("27.99"), stock=8),

            Album(name="Nevermind", media_type=MediaType.CD, price=Decimal("19.99"), stock=20),
            Album(name="In Utero", media_type=MediaType.CD, price=Decimal("18.99"), stock=15),

            Album(name="Heroes", media_type=MediaType.VINYL, price=Decimal("28.99"), stock=9),
            Album(name="The Rise and Fall of Ziggy Stardust and the Spiders from Mars", media_type=MediaType.VINYL, price=Decimal("32.99"), stock=7),

            Album(name="The Dark Side of the Moon", media_type=MediaType.VINYL, price=Decimal("34.99"), stock=10),
            Album(name="Wish You Were Here", media_type=MediaType.VINYL, price=Decimal("32.99"), stock=9),

            Album(name="Random Access Memories", media_type=MediaType.VINYL, price=Decimal("35.99"), stock=6),
            Album(name="Discovery", media_type=MediaType.CD, price=Decimal("22.99"), stock=11),

            Album(name="OK Computer", media_type=MediaType.CD, price=Decimal("24.99"), stock=13),
            Album(name="Kid A", media_type=MediaType.VINYL, price=Decimal("29.99"), stock=7),

            Album(name="Abbey Road", media_type=MediaType.VINYL, price=Decimal("31.99"), stock=14),
            Album(name="The Beatles (White Album)", media_type=MediaType.VINYL, price=Decimal("33.99"), stock=5),

            Album(name="Led Zeppelin IV", media_type=MediaType.VINYL, price=Decimal("30.99"), stock=10),

            Album(name="A Night at the Opera", media_type=MediaType.VINYL, price=Decimal("28.99"), stock=12),

            Album(name="DAMN.", media_type=MediaType.CD, price=Decimal("21.99"), stock=18),
            Album(name="good kid, m.A.A.d city", media_type=MediaType.CD, price=Decimal("23.99"), stock=10),

            Album(name="Scorpion", media_type=MediaType.CD, price=Decimal("19.99"), stock=25),

            Album(name="After Hours", media_type=MediaType.CD, price=Decimal("26.99"), stock=17),

            Album(name="The Eminem Show", media_type=MediaType.CD, price=Decimal("22.99"), stock=13),

            Album(name="Kind of Blue", media_type=MediaType.VINYL, price=Decimal("27.99"), stock=8),

            Album(name="Interstellar OST", media_type=MediaType.VINYL, price=Decimal("29.99"), stock=6),
        ]

        session.add_all(albums)
        session.flush()

        # =========================================================
        # 🔗 ALBUM ↔ ARTISTS
        # =========================================================
        mapping = {
            "Metallica": ["Master of Puppets", "Ride the Lightning"],
            "Nirvana": ["Nevermind", "In Utero"],
            "David Bowie": ["Heroes", "The Rise and Fall of Ziggy Stardust and the Spiders from Mars"],
            "Pink Floyd": ["The Dark Side of the Moon", "Wish You Were Here"],
            "Daft Punk": ["Random Access Memories", "Discovery"],
            "Radiohead": ["OK Computer", "Kid A"],
            "The Beatles": ["Abbey Road", "The Beatles (White Album)"],
            "Led Zeppelin": ["Led Zeppelin IV"],
            "Queen": ["A Night at the Opera"],
            "Kendrick Lamar": ["DAMN.", "good kid, m.A.A.d city"],
            "Drake": ["Scorpion"],
            "The Weeknd": ["After Hours"],
            "Eminem": ["The Eminem Show"],
            "Miles Davis": ["Kind of Blue"],
            "Hans Zimmer": ["Interstellar OST"],
        }

        for artist in artists:
            if artist.name in mapping:
                for album in albums:
                    if album.name in mapping[artist.name]:
                        album.artists.append(artist)

        # =========================================================
        # 🏬 SUPPLIERS (10)
        # =========================================================
        suppliers = [
            Supplier(name="Vinyl Haven", contact_email="contact@vinylhaven.com"),
            Supplier(name="Music World EU", contact_email="sales@musicworld.eu"),
            Supplier(name="Disc Supply", contact_email="info@discsupply.com"),
            Supplier(name="AudioStock", contact_email="support@audiostock.com"),
            Supplier(name="EuroMusic Distribution", contact_email="sales@euromusic.com"),
            Supplier(name="Beat Supply Co", contact_email="contact@beatsupply.com"),
            Supplier(name="Retro Records", contact_email="hello@retrorecords.com"),
            Supplier(name="Global Sound Supply", contact_email="info@globalsound.com"),
            Supplier(name="CD Universe EU", contact_email="eu@cdu.com"),
            Supplier(name="Pure Vinyl Traders", contact_email="contact@purevinyl.com"),
        ]

        session.add_all(suppliers)
        session.flush()

        # =========================================================
        # 📦 SUPPLIER OFFERS
        # =========================================================
        offers = []
        for album in albums:
            supplier = random.choice(suppliers)
            offers.append(
                SupplierOffer(
                    supplier_id=supplier.id,
                    album_id=album.id,
                    unit_price=album.price * Decimal("0.6"),
                )
            )

        session.add_all(offers)

        # =========================================================
        # 🛒 ORDERS (150–200)
        # =========================================================
        orders = []
        order_items = []
        invoices = []

        for i in range(180):
            user = random.choice(users)
            addresses_by_user = {}
            
            for a in addresses:
                addresses_by_user.setdefault(a.user_id, []).append(a)
                
            address = random.choice(addresses_by_user[user.id])

            order = Order(
                user_id=user.id,
                address_id=address.id,
                status=random.choice(list(OrderStatus)),
                total_price=Decimal("1.00"),
            )

            session.add(order)
            session.flush()

            total = Decimal("0.00")

            for album in random.sample(albums, random.randint(1, 4)):
                qty = random.randint(1, 2)

                order_items.append(
                    OrderItem(
                        order_id=order.id,
                        album_id=album.id,
                        quantity=qty,
                        unit_price=album.price,
                    )
                )

                total += album.price * qty

            order.total_price = total

            if order.status != OrderStatus.PENDING:
                invoices.append(
                    Invoice(
                        order_id=order.id,
                        invoice_number=f"INV-2026-{i:05d}",
                        total_amount=total,
                    )
                )

            orders.append(order)

        session.add_all(order_items)
        session.add_all(invoices)

        # =========================================================
        # 🚚 SUPPLIER ORDERS (30–40)
        # =========================================================
        supplier_orders = []
        supplier_items = []

        for i in range(35):
            supplier = random.choice(suppliers)

            so = SupplierOrder(
                supplier_id=supplier.id,
                status=random.choice(list(RestockStatus)),
                total_price=Decimal("1.00"),
            )

            session.add(so)
            session.flush()

            total = Decimal("0.00")

            for album in random.sample(albums, random.randint(1, 3)):
                qty = random.randint(2, 8)
                price = album.price * Decimal("0.5")

                supplier_items.append(
                    SupplierOrderItem(
                        supplier_order_id=so.id,
                        album_id=album.id,
                        quantity=qty,
                        unit_price=price,
                    )
                )

                total += price * qty

            so.total_price = total

        session.add_all(supplier_items)

        # =========================================================
        # COMMIT
        # =========================================================
        session.commit()
        print("✅ Seed completed successfully")

    except Exception as e:
        session.rollback()
        print("❌ Seed failed:", e)

    finally:
        session.close()


if __name__ == "__main__":
    seed()