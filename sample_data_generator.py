#!/usr/bin/env python3
"""
Sample Data Generator for Restaurant Order System
Generates realistic test data for all tables in the database
"""

import random
import secrets
from datetime import datetime, timedelta, date
from decimal import Decimal
from typing import List, Dict
from faker import Faker
from sqlalchemy.orm import Session

# Import all models
from api.models.customers import Customer
from api.models.resources import Resource
from api.models.menu_items import MenuItem, FoodCategory
from api.models.menu_item_ingredients import MenuItemIngredient
from api.models.orders import Order, OrderType, StatusType
from api.models.order_details import OrderDetail
from api.models.payments import Payment, PaymentType, PaymentStatus
from api.models.promotions import Promotion
from api.models.reviews import Reviews
from api.dependencies.database import get_db, engine
from api.models.model_loader import index

# Initialize Faker
fake = Faker()


class SampleDataGenerator:
    def __init__(self, db: Session):
        self.db = db

    def generate_all_data(self):
        """Generate all sample data in the correct order"""
        print("🚀 Starting sample data generation...")

        # Create database tables
        print("📋 Creating database tables...")
        index()

        # Generate data in dependency order
        self.generate_customers()
        self.generate_resources()
        self.generate_menu_items()
        self.generate_menu_item_ingredients()
        self.generate_promotions()
        self.generate_orders()
        self.generate_order_details()
        self.generate_payments()
        self.generate_reviews()

        print("✅ Sample data generation completed!")

    def generate_customers(self, count: int = 50):
        """Generate sample customers"""
        print(f"👥 Generating {count} customers...")

        customers = []
        for _ in range(count):
            # Generate valid 10-digit US phone number
            area_code = random.choice([919, 704, 828, 910, 252, 336, 984])  # NC area codes
            exchange = random.randint(200, 999)  # Valid exchange codes
            number = random.randint(1000, 9999)
            phone = f"{area_code}{exchange:03d}{number:04d}"

            customer = Customer(
                customer_name=fake.name(),
                customer_email=fake.email(),
                customer_phone=phone,
                customer_address=fake.address().replace('\n', ', ')
            )
            customers.append(customer)

        self.db.add_all(customers)
        self.db.commit()
        print(f"✅ Created {count} customers")

    def generate_resources(self):
        """Generate sample ingredients/resources"""
        print("🥕 Generating resources (ingredients)...")

        # Common restaurant ingredients with realistic stock levels
        ingredients_data = [
            # Proteins
            ("Chicken Breast", random.randint(200, 500)),
            ("Ground Beef", random.randint(150, 400)),
            ("Salmon Fillet", random.randint(100, 250)),
            ("Shrimp", random.randint(80, 200)),
            ("Bacon", random.randint(100, 300)),
            ("Eggs", random.randint(500, 1000)),

            # Vegetables
            ("Lettuce", random.randint(50, 150)),
            ("Tomatoes", random.randint(100, 300)),
            ("Onions", random.randint(80, 200)),
            ("Bell Peppers", random.randint(60, 180)),
            ("Mushrooms", random.randint(40, 120)),
            ("Spinach", random.randint(30, 100)),
            ("Avocado", random.randint(50, 150)),
            ("Carrots", random.randint(80, 200)),
            ("Broccoli", random.randint(60, 180)),

            # Carbs
            ("Pasta", random.randint(200, 500)),
            ("Rice", random.randint(300, 800)),
            ("Bread", random.randint(100, 400)),
            ("Potatoes", random.randint(200, 600)),
            ("Tortillas", random.randint(100, 300)),

            # Dairy
            ("Cheese", random.randint(100, 400)),
            ("Mozzarella", random.randint(80, 250)),
            ("Milk", random.randint(50, 200)),
            ("Butter", random.randint(40, 120)),
            ("Cream", random.randint(30, 100)),

            # Pantry items
            ("Olive Oil", random.randint(20, 80)),
            ("Salt", random.randint(50, 200)),
            ("Black Pepper", random.randint(30, 100)),
            ("Garlic", random.randint(40, 150)),
            ("Flour", random.randint(100, 400)),
            ("Sugar", random.randint(80, 300)),

            # Specific items
            ("Pizza Dough", random.randint(50, 200)),
            ("Hamburger Buns", random.randint(100, 300)),
            ("French Fries", random.randint(200, 600)),
            ("Coffee Beans", random.randint(50, 200)),
            ("Ice Cream", random.randint(30, 100)),
        ]

        resources = []
        for item_name, amount in ingredients_data:
            resource = Resource(
                item=item_name,
                amount=amount
            )
            resources.append(resource)

        self.db.add_all(resources)
        self.db.commit()
        print(f"✅ Created {len(resources)} resources")

    def generate_menu_items(self):
        """Generate sample menu items"""
        print("🍽️ Generating menu items...")

        menu_items_data = [
            # Appetizers
            ("Buffalo Wings", "Crispy chicken wings with buffalo sauce", 12.99, 380, FoodCategory.REGULAR),
            ("Mozzarella Sticks", "Golden fried mozzarella with marinara", 8.99, 320, FoodCategory.VEGETARIAN),
            ("Caesar Salad", "Romaine lettuce with caesar dressing", 9.99, 250, FoodCategory.VEGETARIAN),
            ("Spinach Artichoke Dip", "Creamy dip with tortilla chips", 10.99, 420, FoodCategory.VEGETARIAN),

            # Main Courses
            ("Classic Burger", "Beef patty with lettuce, tomato, cheese", 14.99, 650, FoodCategory.REGULAR),
            ("Grilled Chicken Breast", "Seasoned chicken with vegetables", 16.99, 450, FoodCategory.REGULAR),
            ("Salmon Teriyaki", "Grilled salmon with teriyaki glaze", 22.99, 520, FoodCategory.REGULAR),
            ("Margherita Pizza", "Fresh mozzarella, basil, tomato sauce", 18.99, 580, FoodCategory.VEGETARIAN),
            ("Pepperoni Pizza", "Classic pepperoni with mozzarella", 19.99, 620, FoodCategory.REGULAR),
            ("Chicken Alfredo", "Fettuccine with creamy alfredo sauce", 17.99, 720, FoodCategory.REGULAR),
            ("Vegetable Stir Fry", "Mixed vegetables with rice", 13.99, 320, FoodCategory.VEGAN),
            ("Fish and Chips", "Beer battered cod with fries", 15.99, 680, FoodCategory.REGULAR),

            # Healthy Options
            ("Quinoa Bowl", "Quinoa with roasted vegetables", 14.99, 380, FoodCategory.VEGAN),
            ("Keto Chicken Salad", "Grilled chicken with avocado", 15.99, 420, FoodCategory.KETO),
            ("Gluten-Free Pasta", "Rice pasta with marinara sauce", 16.99, 450, FoodCategory.GLUTEN_FREE),
            ("Vegan Burger", "Plant-based patty with vegan cheese", 13.99, 480, FoodCategory.VEGAN),

            # Desserts
            ("Chocolate Cake", "Rich chocolate layer cake", 7.99, 540, FoodCategory.VEGETARIAN),
            ("Vanilla Ice Cream", "Premium vanilla ice cream", 4.99, 220, FoodCategory.VEGETARIAN),
            ("Apple Pie", "Classic apple pie with cinnamon", 6.99, 380, FoodCategory.VEGETARIAN),

            # Beverages
            ("Coffee", "Freshly brewed coffee", 2.99, 5, FoodCategory.VEGAN),
            ("Soft Drink", "Choice of cola, sprite, etc.", 2.49, 150, FoodCategory.VEGAN),
            ("Fresh Orange Juice", "Squeezed daily", 3.99, 110, FoodCategory.VEGAN),
        ]

        menu_items = []
        for name, desc, price, calories, category in menu_items_data:
            menu_item = MenuItem(
                name=name,
                description=desc,
                price=Decimal(str(price)),
                calories=calories,
                food_category=category,
                is_available=random.choice([True, True, True, False])  # 75% available
            )
            menu_items.append(menu_item)

        self.db.add_all(menu_items)
        self.db.commit()
        print(f"✅ Created {len(menu_items)} menu items")

    def generate_menu_item_ingredients(self):
        """Generate ingredient relationships for menu items"""
        print("🔗 Generating menu item ingredients...")

        # Get all menu items and resources
        menu_items = self.db.query(MenuItem).all()
        resources = self.db.query(Resource).all()

        # Create a mapping of resource names to IDs
        resource_map = {resource.item: resource.id for resource in resources}

        # Define ingredient recipes for menu items
        recipes = {
            "Buffalo Wings": [("Chicken Breast", 8), ("Butter", 2), ("Hot Sauce", 1)],
            "Mozzarella Sticks": [("Mozzarella", 6), ("Flour", 2), ("Eggs", 2)],
            "Caesar Salad": [("Lettuce", 4), ("Cheese", 2), ("Eggs", 1)],
            "Classic Burger": [("Ground Beef", 6), ("Hamburger Buns", 1), ("Cheese", 2), ("Lettuce", 1),
                               ("Tomatoes", 1)],
            "Grilled Chicken Breast": [("Chicken Breast", 8), ("Broccoli", 3), ("Carrots", 2)],
            "Salmon Teriyaki": [("Salmon Fillet", 8), ("Rice", 4), ("Garlic", 1)],
            "Margherita Pizza": [("Pizza Dough", 1), ("Mozzarella", 4), ("Tomatoes", 3)],
            "Pepperoni Pizza": [("Pizza Dough", 1), ("Mozzarella", 4), ("Pepperoni", 3)],
            "Chicken Alfredo": [("Chicken Breast", 6), ("Pasta", 4), ("Cream", 3), ("Cheese", 2)],
            "Vegetable Stir Fry": [("Bell Peppers", 2), ("Broccoli", 3), ("Carrots", 2), ("Rice", 4)],
            "Fish and Chips": [("Cod", 8), ("Potatoes", 6), ("Flour", 2)],
            "Quinoa Bowl": [("Quinoa", 4), ("Bell Peppers", 2), ("Spinach", 2)],
            "Keto Chicken Salad": [("Chicken Breast", 6), ("Avocado", 2), ("Spinach", 3)],
            "Chocolate Cake": [("Flour", 4), ("Sugar", 3), ("Eggs", 2), ("Butter", 3)],
            "Vanilla Ice Cream": [("Ice Cream", 3), ("Milk", 2)],
            "Coffee": [("Coffee Beans", 1)],
        }

        ingredients = []
        for menu_item in menu_items:
            if menu_item.name in recipes:
                for ingredient_name, amount in recipes[menu_item.name]:
                    if ingredient_name in resource_map:
                        ingredient = MenuItemIngredient(
                            menu_item_id=menu_item.id,
                            resource_id=resource_map[ingredient_name],
                            amount=amount
                        )
                        ingredients.append(ingredient)
            else:
                # For items not in recipes, add random ingredients
                num_ingredients = random.randint(2, 5)
                selected_resources = random.sample(resources, min(num_ingredients, len(resources)))
                for resource in selected_resources:
                    ingredient = MenuItemIngredient(
                        menu_item_id=menu_item.id,
                        resource_id=resource.id,
                        amount=random.randint(1, 8)
                    )
                    ingredients.append(ingredient)

        self.db.add_all(ingredients)
        self.db.commit()
        print(f"✅ Created {len(ingredients)} menu item ingredients")

    def generate_promotions(self, count: int = 10):
        """Generate sample promotions"""
        print(f"🎟️ Generating {count} promotions...")

        promo_codes = [
            ("WELCOME10", "Welcome discount for new customers", 10),
            ("SAVE15", "15% off your order", 15),
            ("STUDENT20", "Student discount", 20),
            ("WEEKEND25", "Weekend special", 25),
            ("LOYALTY5", "Loyalty customer discount", 5),
            ("FIRSTORDER", "First order discount", 12),
            ("FAMILY30", "Family meal discount", 30),
            ("EARLYBIRD", "Early bird special", 18),
            ("LATENIGHT", "Late night discount", 8),
            ("VEGGIE15", "Vegetarian meal discount", 15),
        ]

        promotions = []
        for i, (code, desc, discount) in enumerate(promo_codes[:count]):
            # Some promotions have expiration dates, some don't
            expiry_date = None
            if i % 3 == 0:  # Every third promotion has an expiry
                expiry_date = fake.date_time_between(start_date='+1d', end_date='+90d')

            promotion = Promotion(
                code=code,
                description=desc,
                discount_percent=discount,
                expiration_date=expiry_date
            )
            promotions.append(promotion)

        self.db.add_all(promotions)
        self.db.commit()
        print(f"✅ Created {count} promotions")

    def generate_orders(self, count: int = 100):
        """Generate sample orders"""
        print(f"📋 Generating {count} orders...")

        customers = self.db.query(Customer).all()
        promotions = self.db.query(Promotion).all()

        orders = []
        for _ in range(count):
            # 70% customer orders, 30% guest orders
            is_guest = random.random() < 0.3

            if is_guest:
                customer_id = None
                guest_name = fake.name()
                # Generate valid 10-digit phone for guest orders
                area_code = random.choice([919, 704, 828, 910, 252, 336, 984])
                exchange = random.randint(200, 999)
                number = random.randint(1000, 9999)
                guest_phone = f"{area_code}{exchange:03d}{number:04d}"
                guest_email = fake.email() if random.random() < 0.7 else None
            else:
                customer_id = random.choice(customers).id
                guest_name = None
                guest_phone = None
                guest_email = None

            # Random order date within last 90 days
            order_date = fake.date_time_between(start_date='-90d', end_date='now')

            # Random promotion code (20% chance)
            promo_code = random.choice(promotions).code if random.random() < 0.2 else None

            order = Order(
                customer_id=customer_id,
                guest_name=guest_name,
                guest_phone=guest_phone,
                guest_email=guest_email,
                order_date=order_date,
                description=fake.sentence() if random.random() < 0.3 else None,
                status=random.choice(list(StatusType)),
                order_type=random.choice(list(OrderType)),
                promotion_code=promo_code
            )
            orders.append(order)

        self.db.add_all(orders)
        self.db.commit()
        print(f"✅ Created {count} orders")

    def generate_order_details(self):
        """Generate order details for all orders"""
        print("📝 Generating order details...")

        orders = self.db.query(Order).all()
        menu_items = self.db.query(MenuItem).filter(MenuItem.is_available == True).all()

        order_details = []
        for order in orders:
            # Each order has 1-5 items
            num_items = random.randint(1, 5)
            selected_items = random.sample(menu_items, min(num_items, len(menu_items)))

            subtotal = Decimal('0')
            for menu_item in selected_items:
                quantity = random.randint(1, 3)
                detail = OrderDetail(
                    order_id=order.id,
                    menu_item_id=menu_item.id,
                    amount=quantity
                )
                order_details.append(detail)
                subtotal += menu_item.price * quantity

            # Update order totals
            discount = Decimal('0')
            if order.promotion_code:
                promotion = self.db.query(Promotion).filter(
                    Promotion.code == order.promotion_code
                ).first()
                if promotion:
                    discount = subtotal * (Decimal(str(promotion.discount_percent)) / 100)

            tax_rate = Decimal('0.07')  # 7% NC sales tax
            tax_amount = (subtotal - discount) * tax_rate
            total = subtotal - discount + tax_amount

            order.subtotal = subtotal
            order.discount_amount = discount
            order.tax_amount = tax_amount
            order.total_amount = total

        self.db.add_all(order_details)
        self.db.commit()
        print(f"✅ Created {len(order_details)} order details")

    def generate_payments(self):
        """Generate payments for orders"""
        print("💳 Generating payments...")

        orders = self.db.query(Order).filter(
            Order.status.in_([StatusType.CONFIRMED, StatusType.COMPLETED])
        ).all()

        payments = []
        for order in orders:
            # 95% of confirmed/completed orders have payments
            if random.random() < 0.95:
                payment_type = random.choice(list(PaymentType))

                # Most payments are completed
                if order.status == StatusType.COMPLETED:
                    status = PaymentStatus.COMPLETED
                else:
                    status = random.choice([
                        PaymentStatus.COMPLETED,
                        PaymentStatus.COMPLETED,
                        PaymentStatus.PENDING,
                        PaymentStatus.FAILED
                    ])

                payment = Payment(
                    order_id=order.id,
                    amount=float(order.total_amount),
                    payment_type=payment_type,
                    status=status,
                    payment_date=order.order_date + timedelta(minutes=random.randint(1, 30))
                )
                payments.append(payment)

        self.db.add_all(payments)
        self.db.commit()
        print(f"✅ Created {len(payments)} payments")

    def generate_reviews(self, count: int = 200):
        """Generate sample reviews"""
        print(f"⭐ Generating {count} reviews...")

        menu_items = self.db.query(MenuItem).all()

        # Sample review texts by rating
        review_templates = {
            5: [
                "Absolutely amazing! Best {} I've ever had.",
                "Perfect! Will definitely order {} again.",
                "Outstanding quality and taste. Highly recommend the {}.",
                "Exceeded expectations! The {} was fantastic.",
            ],
            4: [
                "Really good {}. Would order again.",
                "Great taste, good portion size for the {}.",
                "Very satisfied with the {}. Good value.",
                "Solid choice. The {} was well prepared.",
            ],
            3: [
                "The {} was okay, nothing special.",
                "Average {}. Not bad but not great either.",
                "Decent {} for the price.",
                "The {} was fine, could be better.",
            ],
            2: [
                "Disappointed with the {}. Expected better.",
                "The {} was below average.",
                "Not impressed with the {}. Bland taste.",
                "The {} was cold when it arrived.",
            ],
            1: [
                "Terrible {}. Waste of money.",
                "The {} was awful. Very disappointed.",
                "Poor quality {}. Will not order again.",
                "The {} was inedible. Horrible experience.",
            ]
        }

        reviews = []
        for _ in range(count):
            menu_item = random.choice(menu_items)
            rating = random.choices([1, 2, 3, 4, 5], weights=[5, 10, 25, 35, 25])[0]  # Weighted towards higher ratings

            # Generate review text
            template = random.choice(review_templates[rating])
            review_text = template.format(menu_item.name.lower())

            # Some reviews have no text
            if random.random() < 0.2:
                review_text = None

            review = Reviews(
                menu_item_id=menu_item.id,
                customer_name=fake.name(),
                rating=rating,
                review_text=review_text,
                created_at=fake.date_time_between(start_date='-60d', end_date='now')
            )
            reviews.append(review)

        self.db.add_all(reviews)
        self.db.commit()
        print(f"✅ Created {count} reviews")

    def print_summary(self):
        """Print a summary of generated data"""
        print("\n📊 DATA GENERATION SUMMARY")
        print("=" * 50)

        counts = {
            "Customers": self.db.query(Customer).count(),
            "Resources": self.db.query(Resource).count(),
            "Menu Items": self.db.query(MenuItem).count(),
            "Menu Item Ingredients": self.db.query(MenuItemIngredient).count(),
            "Orders": self.db.query(Order).count(),
            "Order Details": self.db.query(OrderDetail).count(),
            "Payments": self.db.query(Payment).count(),
            "Promotions": self.db.query(Promotion).count(),
            "Reviews": self.db.query(Reviews).count(),
        }

        for table, count in counts.items():
            print(f"{table:<25}: {count:>5}")

        print("=" * 50)
        print("🎉 All sample data generated successfully!")


def main():
    """Main function to run the data generator"""
    try:
        # Get database session
        db = next(get_db())

        # Create generator and run
        generator = SampleDataGenerator(db)
        generator.generate_all_data()
        generator.print_summary()

    except Exception as e:
        print(f"❌ Error generating data: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()