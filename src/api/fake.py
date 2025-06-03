
import random
import string
from faker import Faker
from sqlalchemy import create_engine, text

fake = Faker()
engine = create_engine("postgresql+psycopg://myuser:mypassword2@localhost:5433/mydatabase2")

NUM_USERS = 300_000
NUM_RESTAURANTS = 1000
NUM_PREFERENCES = 50
NUM_REVIEWS = 700_000
NUM_CUISINES = 30

def insert_batch(query, values):
    with engine.begin() as conn:
        conn.execute(text(query), values)

def fake_users(n):
    print("Creating 300,000 fake users")
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE"))
    users = []

    while len(users) < n:
        name = fake.name()
        username = fake.unique.user_name() + ''.join(random.choices(string.digits, k=4))
        email = fake.unique.email()
        
        users.append({
            "name": name,
            "username": username,
            "email": email,
            "permissions": 1
        })

    insert_batch("""
        INSERT INTO users (name, username, email, permissions)
        VALUES (:name, :username, :email, :permissions)
    """, users)


def restaurant_cuisines():
    print("Created 30 cuisines")
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE cuisines RESTART IDENTITY CASCADE"))
    
    cuisine_names = [
        "Italian", "Chinese", "Mexican", "Indian", "Thai", "Japanese", "French", "Greek",
        "Spanish", "Korean", "Vietnamese", "Turkish", "Ethiopian", "Lebanese", "Moroccan",
        "Caribbean", "Brazilian", "Cuban", "German", "Persian", "Russian", "American",
        "Filipino", "Indonesian", "Malaysian", "Pakistani", "Afghan", "Argentine", "Polish", "Ukrainian"
    ]
    
    insert_batch("""
        INSERT INTO cuisines (name) VALUES (:name)
    """, [{"name": name} for name in cuisine_names])


def fake_restaurants(n):
    print("Creating fake restaurants")
    with engine.connect() as conn:
        cuisine_ids = [row[0] for row in conn.execute(text("SELECT id FROM cuisines")).fetchall()]
    restaurants = []
    for _ in range(n):
        restaurants.append({
            "name": fake.company(),
            "cuisine_id": random.choice(cuisine_ids),
            "address": fake.street_address(),
            "city": fake.city(),
            "state": fake.state_abbr(),
            "zipcode": fake.zipcode(),
            "phone": fake.phone_number(),
        })
    insert_batch("""
        INSERT INTO restaurants (name, cuisine_id, address, city, state, zipcode, phone)
        VALUES (:name, :cuisine_id, :address, :city, :state, :zipcode, :phone)
    """, restaurants)

def user_preferences():
    print("50 user preferences created")
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE preferences RESTART IDENTITY CASCADE"))

    preference_names = [
        "Vegan", "Vegetarian", "Gluten-Free", "Keto", "Halal", "Kosher", "Paleo",
        "Dairy-Free", "Nut-Free", "Low-Carb", "High-Protein", "Organic", "Pescatarian",
        "Sugar-Free", "Low-Sodium", "Low-Fat", "Raw", "Whole30", "Flexitarian", "Carnivore",
        "No MSG", "No Soy", "No Shellfish", "No Red Meat", "No Pork", "Alcohol-Free",
        "Farm-to-Table", "Locally-Sourced", "Sustainable", "Non-GMO", "Spicy Lover",
        "Mild Only", "Kids Menu", "Dog-Friendly", "Outdoor Seating", "Fast Service",
        "Late Night", "Breakfast All Day", "BYOB", "Romantic", "Casual", "Fine Dining",
        "Buffet", "Food Truck", "Takeout", "Delivery", "Reservations", "Live Music",
        "Wheelchair Accessible", "Quiet Atmosphere"
    ][:NUM_PREFERENCES]  
    
    insert_batch("""
        INSERT INTO preferences (name) VALUES (:name)
    """, [{"name": name} for name in preference_names])

def fake_user_preferences():
    print("Assigning exactly one fake user preference per user")
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE user_preferences RESTART IDENTITY CASCADE"))
        user_ids = [r[0] for r in conn.execute(text("SELECT id FROM users")).fetchall()]
        preference_ids = [r[0] for r in conn.execute(text("SELECT id FROM preferences")).fetchall()]

    rows = []
    for user_id in user_ids:
        pref_id = random.choice(preference_ids)
        rows.append({
            "user_id": user_id,
            "preference_id": pref_id
        })

    insert_batch("""
        INSERT INTO user_preferences (user_id, preference_id)
        VALUES (:user_id, :preference_id)
    """, rows)


def fake_restaurant_preferences():
    print("Creating fake restaurant preferences")
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE restaurant_preferences RESTART IDENTITY CASCADE"))
        restaurant_ids = [r[0] for r in conn.execute(text("SELECT id FROM restaurants")).fetchall()]
        preference_ids = [r[0] for r in conn.execute(text("SELECT id FROM preferences")).fetchall()]

    rows = []
    for rid in restaurant_ids:
        pref_id = random.choice(preference_ids)  
        rows.append({
            "restaurant_id": rid,
            "preference_id": pref_id
        })

    insert_batch("""
        INSERT INTO restaurant_preferences (restaurant_id, preference_id)
        VALUES (:restaurant_id, :preference_id)
    """, rows)


def fake_reviews(n):
    print("Writing fake reviews")
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE reviews RESTART IDENTITY CASCADE"))
        restaurant_ids = [r[0] for r in conn.execute(text("SELECT id FROM restaurants")).fetchall()]
        user_ids = [r[0] for r in conn.execute(text("SELECT id FROM users")).fetchall()]

    seen_pairs = set()
    rows = []

    while len(rows) < n:
        restaurant_id = random.choice(restaurant_ids)
        user_id = random.choice(user_ids)
        pair = (restaurant_id, user_id)
        if pair in seen_pairs:
            continue
        seen_pairs.add(pair)

        rows.append({
            "user_id": user_id,
            "restaurant_id": restaurant_id,
            "overall_rating": round(random.uniform(0.0, 5.0), 1),
            "food_rating": round(random.uniform(0.0, 5.0), 1),
            "service_rating": round(random.uniform(0.0, 5.0), 1),
            "price_rating": round(random.uniform(0.0, 5.0), 1),
            "cleanliness_rating": round(random.uniform(0.0, 5.0), 1),
            "written_review": fake.text(max_nb_chars=random.randint(50, 250)) if random.random() < 0.5 else None
        })

    insert_batch("""
        INSERT INTO reviews (user_id, restaurant_id, overall_rating, food_rating, service_rating, price_rating, cleanliness_rating, written_review)
        VALUES (:user_id, :restaurant_id, :overall_rating, :food_rating, :service_rating, :price_rating, :cleanliness_rating, :written_review)
    """, rows)


if __name__ == "__main__":
    print("Creating fake data")
    restaurant_cuisines()
    fake_users(NUM_USERS)
    user_preferences()
    fake_restaurants(NUM_RESTAURANTS)
    fake_user_preferences()
    fake_restaurant_preferences()
    fake_reviews(NUM_REVIEWS)
    print("Completed fake data")
