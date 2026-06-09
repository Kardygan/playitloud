import random
from decimal import Decimal

from playitloud.core.database import SessionLocal
from playitloud.core.security import hash_password
from playitloud.models import (
    Address,
    Album,
    Artist,
    Invoice,
    Order,
    OrderItem,
    Supplier,
    SupplierOffer,
    SupplierOrder,
    SupplierOrderItem,
    User,
)
from playitloud.models.album import MediaType
from playitloud.models.order import OrderStatus
from playitloud.models.supplier_order import RestockStatus

CD = MediaType.CD
VINYL = MediaType.VINYL

USERS = [
    ("Lucas", "Dubois"),
    ("Emma", "Lambert"),
    ("Noah", "Martin"),
    ("Mila", "Janssens"),
    ("Liam", "Peeters"),
    ("Olivia", "Maes"),
    ("Hugo", "Dupont"),
    ("Lina", "Wouters"),
    ("Jules", "Lemaire"),
    ("Sofia", "Claes"),
    ("Arthur", "Simon"),
    ("Nora", "Goossens"),
]

CITIES = [
    ("Bruxelles", "1000"),
    ("Antwerpen", "2000"),
    ("Leuven", "3000"),
    ("Liège", "4000"),
    ("Namur", "5000"),
    ("Charleroi", "6000"),
    ("Brugge", "8000"),
    ("Gent", "9000"),
]

SUPPLIERS = [
    ("Vinyl Haven", "contact@vinylhaven.com"),
    ("EuroSound Distribution", "sales@eurosound.eu"),
    ("Disc & Co", "info@discandco.com"),
    ("Retro Records Supply", "hello@retrorecords.com"),
    ("Northern Press Co", "orders@northernpress.com"),
    ("Global Music Supply", "contact@globalmusic.com"),
]

ARTISTS = [
    {
        "name": "David Bowie",
        "image": "david_bowie.jpg",
        "description": "English singer-songwriter and a leading figure in popular music for five decades.",
        "albums": [
            {
                "name": "Blackstar",
                "image": "blackstar.jpg",
                "media_type": CD,
                "price": Decimal("21.99"),
                "description": "Released 8 January 2016. Bowie's final album, issued two days before his death and praised as a haunting farewell.",
            },
            {
                "name": '"Heroes"',
                "image": "heroes.jpg",
                "media_type": VINYL,
                "price": Decimal("28.99"),
                "description": "Released 14 October 1977. The centerpiece of Bowie's Berlin Trilogy, recorded with Brian Eno.",
            },
            {
                "name": "The Rise and Fall of Ziggy Stardust and the Spiders from Mars",
                "image": "ziggy_stardust.jpg",
                "media_type": VINYL,
                "price": Decimal("31.99"),
                "description": "Released 16 June 1972. A concept album that introduced Bowie's Ziggy Stardust persona.",
            },
        ],
    },
    {
        "name": "Nirvana",
        "image": "nirvana.jpg",
        "description": "American grunge band that brought alternative rock into the mainstream.",
        "albums": [
            {
                "name": "Nevermind",
                "image": "nevermind.jpg",
                "media_type": VINYL,
                "price": Decimal("26.99"),
                "description": "Released 24 September 1991. The album that broke grunge worldwide.",
            },
            {
                "name": "In Utero",
                "image": "in_utero.jpg",
                "media_type": CD,
                "price": Decimal("18.99"),
                "description": "Released 21 September 1993. Nirvana's raw, uncompromising final studio album.",
            },
        ],
    },
    {
        "name": "The Beatles",
        "image": "beatles.jpg",
        "description": "English rock band widely regarded as the most influential act of the 1960s.",
        "albums": [
            {
                "name": "Abbey Road",
                "image": "abbey_road.jpg",
                "media_type": VINYL,
                "price": Decimal("32.99"),
                "description": "Released 26 September 1969. The band's penultimate album, famous for its side-two medley.",
            },
            {
                "name": "Revolver",
                "image": "revolver.jpg",
                "media_type": CD,
                "price": Decimal("22.99"),
                "description": "Released 5 August 1966. A studio landmark that broadened the band's sonic range.",
            },
        ],
    },
    {
        "name": "R.E.M.",
        "image": "rem.jpg",
        "description": "American alternative rock band from Athens, Georgia.",
        "albums": [
            {
                "name": "Automatic for the People",
                "image": "automatic_for_the_people.jpg",
                "media_type": CD,
                "price": Decimal("19.99"),
                "description": "Released 5 October 1992. A somber, reflective career highlight.",
            },
            {
                "name": "Document",
                "image": "document.jpg",
                "media_type": VINYL,
                "price": Decimal("25.99"),
                "description": "Released 31 August 1987. The band's commercial breakthrough.",
            },
            {
                "name": "Monster",
                "image": "monster.jpg",
                "media_type": CD,
                "price": Decimal("18.99"),
                "description": "Released 27 September 1994. A loud, glam-influenced departure.",
            },
        ],
    },
    {
        "name": "Pink Floyd",
        "image": "pink_floyd.jpg",
        "description": "English progressive rock band known for concept albums and elaborate live shows.",
        "albums": [
            {
                "name": "The Wall",
                "image": "wall.jpg",
                "media_type": VINYL,
                "price": Decimal("36.99"),
                "description": "Released 30 November 1979. A sprawling rock opera and double album.",
            },
            {
                "name": "Wish You Were Here",
                "image": "wish_you_were_here.jpg",
                "media_type": VINYL,
                "price": Decimal("32.99"),
                "description": "Released 12 September 1975. A tribute to former member Syd Barrett.",
            },
        ],
    },
    {
        "name": "Metallica",
        "image": "metallica.jpg",
        "description": "American heavy metal band and one of the founders of thrash metal.",
        "albums": [
            {
                "name": "Master of Puppets",
                "image": "master_of_puppets.jpg",
                "media_type": VINYL,
                "price": Decimal("29.99"),
                "description": "Released 3 March 1986. A defining thrash metal record and the band's first gold album.",
            },
            {
                "name": "Ride the Lightning",
                "image": "ride_the_lightning.jpg",
                "media_type": CD,
                "price": Decimal("19.99"),
                "description": "Released 27 July 1984. The band's ambitious and acclaimed second album.",
            },
        ],
    },
    {
        "name": "Ghost",
        "image": "ghost.jpg",
        "description": "Swedish rock band known for theatrical performances and melodic hard rock.",
        "albums": [
            {
                "name": "Meliora",
                "image": "meliora.jpg",
                "media_type": CD,
                "price": Decimal("20.99"),
                "description": "Released 21 August 2015. Won a Grammy for the single 'Cirice'.",
            },
            {
                "name": "Prequelle",
                "image": "prequelle.jpg",
                "media_type": VINYL,
                "price": Decimal("28.99"),
                "description": "Released 1 June 2018. A loose concept album themed around the Black Death.",
            },
            {
                "name": "Impera",
                "image": "impera.jpg",
                "media_type": CD,
                "price": Decimal("23.99"),
                "description": "Released 11 March 2022. The band's chart-topping fifth studio album.",
            },
        ],
    },
    {
        "name": "Radiohead",
        "image": "radiohead.jpg",
        "description": "English rock band acclaimed for their experimental, genre-defying approach.",
        "albums": [
            {
                "name": "OK Computer",
                "image": "ok_computer.jpg",
                "media_type": CD,
                "price": Decimal("24.99"),
                "description": "Released 16 June 1997. A landmark album exploring modern alienation.",
            },
            {
                "name": "Kid A",
                "image": "kid_a.jpg",
                "media_type": VINYL,
                "price": Decimal("29.99"),
                "description": "Released 2 October 2000. A bold electronic reinvention of the band's sound.",
            },
        ],
    },
    {
        "name": "The Rolling Stones",
        "image": "rolling_stones.jpg",
        "description": "English rock band and one of the most enduring acts in rock history.",
        "albums": [
            {
                "name": "Let It Bleed",
                "image": "let_it_bleed.jpg",
                "media_type": VINYL,
                "price": Decimal("30.99"),
                "description": "Released 28 November 1969. A cornerstone of the band's golden era.",
            },
            {
                "name": "Sticky Fingers",
                "image": "sticky_fingers.jpg",
                "media_type": VINYL,
                "price": Decimal("33.99"),
                "description": "Released 23 April 1971. The first album released on the band's own label.",
            },
        ],
    },
    {
        "name": "System of a Down",
        "image": "system_of_a_down.jpg",
        "description": "American-Armenian metal band known for eclectic, politically charged music.",
        "albums": [
            {
                "name": "Toxicity",
                "image": "toxicity.jpg",
                "media_type": CD,
                "price": Decimal("21.99"),
                "description": "Released 4 September 2001. The band's chart-topping breakthrough.",
            },
            {
                "name": "Mezmerize",
                "image": "mezmerize.jpg",
                "media_type": CD,
                "price": Decimal("20.99"),
                "description": "Released 17 May 2005. The first half of a two-part release.",
            },
        ],
    },
    {
        "name": "The War on Drugs",
        "image": "war_on_drugs.jpg",
        "description": "American rock band blending heartland rock with atmospheric production.",
        "albums": [
            {
                "name": "Lost in the Dream",
                "image": "lost_in_the_dream.jpg",
                "media_type": VINYL,
                "price": Decimal("27.99"),
                "description": "Released 18 March 2014. The album that earned the band wide critical acclaim.",
            },
            {
                "name": "A Deeper Understanding",
                "image": "deeper_understanding.jpg",
                "media_type": CD,
                "price": Decimal("22.99"),
                "description": "Released 25 August 2017. Won the Grammy for Best Rock Album.",
            },
        ],
    },
    {
        "name": "Low Roar",
        "image": "low_roar.jpg",
        "description": "Atmospheric indie and electronic project founded by Ryan Karazija.",
        "albums": [
            {
                "name": "Once in a Long, Long While...",
                "image": "once_in_a_long_long_while.jpg",
                "media_type": VINYL,
                "price": Decimal("26.99"),
                "description": "Released 14 April 2017. Widely noted for its use in the game Death Stranding.",
            },
        ],
    },
    {
        "name": "Bruce Springsteen",
        "image": "bruce_springsteen.jpg",
        "description": "American rock singer-songwriter known as 'The Boss'.",
        "albums": [
            {
                "name": "Born to Run",
                "image": "born_to_run.jpg",
                "media_type": VINYL,
                "price": Decimal("28.99"),
                "description": "Released 25 August 1975. The breakthrough record that made Springsteen a star.",
            },
            {
                "name": "Nebraska",
                "image": "nebraska.jpg",
                "media_type": CD,
                "price": Decimal("19.99"),
                "description": "Released 30 September 1982. A stark, home-recorded acoustic album.",
            },
        ],
    },
    {
        "name": "The Clash",
        "image": "clash.jpg",
        "description": "English punk rock band formed in London in 1976.",
        "albums": [
            {
                "name": "London Calling",
                "image": "london_calling.jpg",
                "media_type": VINYL,
                "price": Decimal("31.99"),
                "description": "Released 14 December 1979. A genre-spanning double album and punk touchstone.",
            },
            {
                "name": "Combat Rock",
                "image": "combat_rock.jpg",
                "media_type": CD,
                "price": Decimal("20.99"),
                "description": "Released 14 May 1982. The band's most commercially successful album.",
            },
        ],
    },
    {
        "name": "Hällas",
        "image": "hallas.jpg",
        "description": "Swedish progressive rock band with an adventurous, retro-leaning sound.",
        "albums": [
            {
                "name": "Excerpts from a Future Past",
                "image": "excerpts_from_a_future_past.jpg",
                "media_type": VINYL,
                "price": Decimal("27.99"),
                "description": "Released 17 November 2017. The band's debut full-length concept album.",
            },
        ],
    },
]

ORDER_STATUS_WEIGHTS = {
    OrderStatus.DELIVERED: 5,
    OrderStatus.SHIPPED: 3,
    OrderStatus.PAID: 3,
    OrderStatus.PENDING: 2,
    OrderStatus.CANCELLED: 1,
}
INVOICED_STATUSES = {OrderStatus.PAID, OrderStatus.SHIPPED, OrderStatus.DELIVERED}


def seed():
    session = SessionLocal()

    try:
        hashed_password = hash_password("seed-placeholder")

        users = [
            User(
                email=f"{first}.{last}@example.com".lower(),
                hashed_password=hashed_password,
                first_name=first,
                last_name=last,
            )
            for first, last in USERS
        ]
        session.add_all(users)
        session.flush()

        addresses = []
        for user in users:
            for _ in range(random.randint(1, 2)):
                city, postal_code = random.choice(CITIES)
                addresses.append(
                    Address(
                        user_id=user.id,
                        street=f"{random.randint(1, 200)} Rue de la Musique",
                        city=city,
                        postal_code=postal_code,
                        country_code="BE",
                    )
                )
        session.add_all(addresses)
        session.flush()

        addresses_by_user: dict[int, list[Address]] = {}
        for address in addresses:
            addresses_by_user.setdefault(address.user_id, []).append(address)

        albums: list[Album] = []
        for entry in ARTISTS:
            artist = Artist(
                name=entry["name"],
                description=entry["description"],
                picture_url=f"/static/images/artists/{entry['image']}",
            )
            for album_data in entry["albums"]:
                album = Album(
                    name=album_data["name"],
                    description=album_data["description"],
                    cover_url=f"/static/images/albums/{album_data['image']}",
                    media_type=album_data["media_type"],
                    price=album_data["price"],
                    stock=random.randint(5, 25),
                )
                album.artists.append(artist)
                albums.append(album)
            session.add(artist)
        session.add_all(albums)
        session.flush()

        suppliers = [Supplier(name=name, contact_email=email) for name, email in SUPPLIERS]
        session.add_all(suppliers)
        session.flush()

        offers = []
        for album in albums:
            for supplier in random.sample(suppliers, random.randint(1, 2)):
                offers.append(
                    SupplierOffer(
                        supplier_id=supplier.id,
                        album_id=album.id,
                        unit_price=(album.price * Decimal("0.55")).quantize(Decimal("0.01")),
                    )
                )
        session.add_all(offers)

        status_pool = [
            status for status, weight in ORDER_STATUS_WEIGHTS.items() for _ in range(weight)
        ]

        orders = []
        for index in range(50):
            user = random.choice(users)
            address = random.choice(addresses_by_user[user.id])
            status = random.choice(status_pool)

            total_price = Decimal("0.00")
            order_items = []
            for album in random.sample(albums, random.randint(1, 4)):
                quantity = random.randint(1, 3)
                order_items.append(
                    OrderItem(album_id=album.id, quantity=quantity, unit_price=album.price)
                )
                total_price += album.price * quantity

            order = Order(
                user_id=user.id,
                address_id=address.id,
                status=status,
                total_price=total_price,
            )
            order.order_items = order_items
            session.add(order)
            orders.append((index, order, status, total_price))
        session.flush()

        invoices = [
            Invoice(
                order_id=order.id,
                invoice_number=f"INV-2026-{index:04d}",
                total_amount=total_price,
            )
            for index, order, status, total_price in orders
            if status in INVOICED_STATUSES
        ]
        session.add_all(invoices)

        supplier_orders = []
        for _ in range(15):
            supplier = random.choice(suppliers)

            total_price = Decimal("0.00")
            supplier_items = []
            for album in random.sample(albums, random.randint(1, 3)):
                quantity = random.randint(5, 20)
                unit_price = (album.price * Decimal("0.5")).quantize(Decimal("0.01"))
                supplier_items.append(
                    SupplierOrderItem(
                        album_id=album.id, quantity=quantity, unit_price=unit_price
                    )
                )
                total_price += unit_price * quantity

            supplier_order = SupplierOrder(
                supplier_id=supplier.id,
                status=random.choice(list(RestockStatus)),
                total_price=total_price,
            )
            supplier_order.supplier_order_items = supplier_items
            session.add(supplier_order)
            supplier_orders.append(supplier_order)

        session.commit()
        print(
            f"Seed complete: {len(users)} users, {len(albums)} albums, "
            f"{len(orders)} orders, {len(supplier_orders)} supplier orders."
        )

    except Exception as exc:
        session.rollback()
        print(f"Seed failed: {exc}")
        raise

    finally:
        session.close()


if __name__ == "__main__":
    seed()
