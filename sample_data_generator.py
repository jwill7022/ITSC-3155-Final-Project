#!/usr/bin/env python3
"""
Sample Data Generator for Restaurant Order System
Run this script to populate your database with realistic test data
"""

import requests
import json
from datetime import datetime, timedelta
import random

# Configuration
BASE_URL = "http://localhost:8000"  # Adjust if your API runs on different port
SAMPLE_SIZE = {
    "customers": 20,
    "resources": 30,
    "menu_items": 25,
    "promotions": 5,
    "orders": 50,
    "reviews": 100
}

class SampleDataGenerator:

    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.created_ids = {
            "customers": [],
            "resources": [],
            "menu_items": [],
            "promotions": [],
            "orders": [],
            "menu_item_ingredients": [],
            "order_details": [],
            "payments": []
        }

    def create_customers(self):
        """Create sample customers"""
        print("Creating customers...")
        customers = [
            {"customer_name": "John Smith", "customer_email": "john.smith@email.com", "customer_phone": 9195551234, "customer_address": "123 Main St, Clayton, NC"},
            {"customer_name": "Sarah Johnson", "customer_email": "sarah.j@email.com", "customer_phone": 9195551235, "customer_address": "456 Oak Ave, Clayton, NC"},
            {"customer_name": "Mike Wilson", "customer_email": "mike.wilson@email.com", "customer_phone": 9195551236, "customer_address": "789 Pine St, Clayton, NC"},
            {"customer_name": "Emily Davis", "customer_email": "emily.davis@email.com", "customer_phone": 9195551237, "customer_address": "321 Elm St, Clayton, NC"},
            {"customer_name": "Chris Brown", "customer_email": "chris.brown@email.com", "customer_phone": 9195551238, "customer_address": "654 Maple Dr, Clayton, NC"},
            {"customer_name": "Jessica Garcia", "customer_email": "jessica.garcia@email.com", "customer_phone": 9195551239, "customer_address": "987 Cedar Ln, Clayton, NC"},
            {"customer_name": "David Miller", "customer_email": "david.miller@email.com", "customer_phone": 9195551240, "customer_address": "147 Birch Rd, Clayton, NC"},
            {"customer_name": "Lisa Anderson", "customer_email": "lisa.anderson@email.com", "customer_phone": 9195551241, "customer_address": "258 Spruce Way, Clayton, NC"},
            {"customer_name": "Robert Taylor", "customer_email": "robert.taylor@email.com", "customer_phone": 9195551242, "customer_address": "369 Willow St, Clayton, NC"},
            {"customer_name": "Amanda Martinez", "customer_email": "amanda.martinez@email.com", "customer_phone": 9195551243, "customer_address": "741 Poplar Ave, Clayton, NC"},
            {"customer_name": "Kevin Lee", "customer_email": "kevin.lee@email.com", "customer_phone": 9195551244, "customer_address": "852 Hickory Dr, Clayton, NC"},
            {"customer_name": "Rachel White", "customer_email": "rachel.white@email.com", "customer_phone": 9195551245, "customer_address": "963 Ash Ln, Clayton, NC"},
            {"customer_name": "Brian Thompson", "customer_email": "brian.thompson@email.com", "customer_phone": 9195551246, "customer_address": "159 Dogwood St, Clayton, NC"},
            {"customer_name": "Michelle Lewis", "customer_email": "michelle.lewis@email.com", "customer_phone": 9195551247, "customer_address": "357 Magnolia Way, Clayton, NC"},
            {"customer_name": "Jason Clark", "customer_email": "jason.clark@email.com", "customer_phone": 9195551248, "customer_address": "468 Peach St, Clayton, NC"},
            {"customer_name": "Nicole Young", "customer_email": "nicole.young@email.com", "customer_phone": 9195551249, "customer_address": "579 Cherry Ave, Clayton, NC"},
            {"customer_name": "Mark Rodriguez", "customer_email": "mark.rodriguez@email.com", "customer_phone": 9195551250, "customer_address": "680 Plum Dr, Clayton, NC"},
            {"customer_name": "Stephanie Walker", "customer_email": "stephanie.walker@email.com", "customer_phone": 9195551251, "customer_address": "791 Apple Ln, Clayton, NC"},
            {"customer_name": "Andrew Hall", "customer_email": "andrew.hall@email.com", "customer_phone": 9195551252, "customer_address": "802 Orange St, Clayton, NC"},
            {"customer_name": "Jennifer Allen", "customer_email": "jennifer.allen@email.com", "customer_phone": 9195551253, "customer_address": "913 Pecan Way, Clayton, NC"}
        ]

        for customer in customers:
            response = requests.post(f"{self.base_url}/customers/", json=customer)
            if response.status_code == 200:
                self.created_ids["customers"].append(response.json()["id"])
                print(f"✓ Created customer: {customer['customer_name']}")
            else:
                print(f"✗ Failed to create customer: {customer['customer_name']} - {response.text}")

    def create_resources(self):
        """Create sample inventory resources"""
        print("\nCreating resources (ingredients)...")
        resources = [
            {"item": "Ground Beef", "amount": 500},
            {"item": "Chicken Breast", "amount": 300},
            {"item": "Salmon Fillet", "amount": 200},
            {"item": "Shrimp", "amount": 150},
            {"item": "Lettuce", "amount": 100},
            {"item": "Tomatoes", "amount": 200},
            {"item": "Onions", "amount": 150},
            {"item": "Cheese", "amount": 300},
            {"item": "Bread Rolls", "amount": 400},
            {"item": "Pizza Dough", "amount": 100},
            {"item": "Pasta", "amount": 250},
            {"item": "Rice", "amount": 300},
            {"item": "Potatoes", "amount": 400},
            {"item": "Mushrooms", "amount": 80},
            {"item": "Bell Peppers", "amount": 120},
            {"item": "Carrots", "amount": 100},
            {"item": "Broccoli", "amount": 80},
            {"item": "Spinach", "amount": 60},
            {"item": "Garlic", "amount": 50},
            {"item": "Olive Oil", "amount": 200},
            {"item": "Salt", "amount": 500},
            {"item": "Black Pepper", "amount": 100},
            {"item": "Italian Seasoning", "amount": 50},
            {"item": "Hot Sauce", "amount": 75},
            {"item": "Ranch Dressing", "amount": 100},
            {"item": "Mayonnaise", "amount": 150},
            {"item": "Ketchup", "amount": 200},
            {"item": "Mustard", "amount": 100},
            {"item": "Bacon", "amount": 200},
            {"item": "Eggs", "amount": 300}
        ]

        for resource in resources:
            response = requests.post(f"{self.base_url}/resources/", json=resource)
            if response.status_code == 200:
                self.created_ids["resources"].append(response.json()["id"])
                print(f"✓ Created resource: {resource['item']}")
            else:
                print(f"✗ Failed to create resource: {resource['item']} - {response.text}")

    def create_menu_items(self):
        """Create sample menu items"""
        print("\nCreating menu items...")
        menu_items = [
            {"name": "Classic Burger", "description": "Beef patty with lettuce, tomato, onion", "price": 12.99, "calories": 650, "food_category": "regular"},
            {"name": "Chicken Caesar Salad", "description": "Grilled chicken breast over romaine lettuce", "price": 11.49, "calories": 420, "food_category": "regular"},
            {"name": "Margherita Pizza", "description": "Fresh mozzarella, tomatoes, and basil", "price": 14.99, "calories": 850, "food_category": "vegetarian"},
            {"name": "Grilled Salmon", "description": "Atlantic salmon with seasonal vegetables", "price": 18.99, "calories": 480, "food_category": "regular"},
            {"name": "Veggie Wrap", "description": "Fresh vegetables wrapped in spinach tortilla", "price": 9.99, "calories": 320, "food_category": "vegan"},
            {"name": "BBQ Ribs", "description": "Slow-cooked pork ribs with BBQ sauce", "price": 22.99, "calories": 920, "food_category": "regular"},
            {"name": "Shrimp Pasta", "description": "Linguine with garlic shrimp in white wine sauce", "price": 16.99, "calories": 680, "food_category": "regular"},
            {"name": "Garden Salad", "description": "Mixed greens with seasonal vegetables", "price": 8.99, "calories": 180, "food_category": "vegan"},
            {"name": "Chicken Wings", "description": "Buffalo wings with ranch dipping sauce", "price": 13.99, "calories": 720, "food_category": "regular"},
            {"name": "Mushroom Risotto", "description": "Creamy arborio rice with wild mushrooms", "price": 15.99, "calories": 560, "food_category": "vegetarian"},
            {"name": "Fish Tacos", "description": "Grilled fish with cabbage slaw in corn tortillas", "price": 14.49, "calories": 420, "food_category": "regular"},
            {"name": "Quinoa Bowl", "description": "Quinoa with roasted vegetables and tahini", "price": 12.99, "calories": 380, "food_category": "vegan"},
            {"name": "Steak Frites", "description": "Grilled sirloin with french fries", "price": 24.99, "calories": 890, "food_category": "regular"},
            {"name": "Caprese Sandwich", "description": "Fresh mozzarella, tomato, and basil on ciabatta", "price": 10.99, "calories": 450, "food_category": "vegetarian"},
            {"name": "Thai Curry", "description": "Coconut curry with vegetables and jasmine rice", "price": 13.99, "calories": 520, "food_category": "vegan"},
            {"name": "Lobster Roll", "description": "Fresh lobster meat on toasted brioche", "price": 28.99, "calories": 480, "food_category": "regular"},
            {"name": "Black Bean Burger", "description": "House-made veggie patty with avocado", "price": 11.99, "calories": 420, "food_category": "vegan"},
            {"name": "Chicken Parmesan", "description": "Breaded chicken breast with marinara and cheese", "price": 17.99, "calories": 780, "food_category": "regular"},
            {"name": "Greek Salad", "description": "Tomatoes, cucumbers, olives, and feta cheese", "price": 10.49, "calories": 320, "food_category": "vegetarian"},
            {"name": "Pad Thai", "description": "Rice noodles with shrimp, peanuts, and lime", "price": 15.49, "calories": 640, "food_category": "regular"},
            {"name": "Stuffed Bell Peppers", "description": "Bell peppers stuffed with quinoa and vegetables", "price": 13.49, "calories": 380, "food_category": "vegan"},
            {"name": "Fish and Chips", "description": "Beer-battered cod with hand-cut fries", "price": 16.99, "calories": 820, "food_category": "regular"},
            {"name": "Acai Bowl", "description": "Acai smoothie bowl with granola and berries", "price": 11.99, "calories": 340, "food_category": "vegan"},
            {"name": "Lamb Gyro", "description": "Seasoned lamb with tzatziki in pita bread", "price": 14.99, "calories": 580, "food_category": "regular"},
            {"name": "Eggplant Parmesan", "description": "Breaded eggplant with marinara and mozzarella", "price": 14.99, "calories": 520, "food_category": "vegetarian"}
        ]

        for item in menu_items:
            response = requests.post(f"{self.base_url}/menu_items/", json=item)
            if response.status_code == 200:
                self.created_ids["menu_items"].append(response.json()["id"])
                print(f"✓ Created menu item: {item['name']}")
            else:
                print(f"✗ Failed to create menu item: {item['name']} - {response.text}")

    def create_menu_item_ingredients(self):
        """Create ingredient relationships for menu items"""
        print("\nCreating menu item ingredients...")

        # Define ingredient mappings (menu_item_id: [(resource_id, amount), ...])
        # This assumes resource IDs 1-30 and menu_item IDs 1-25
        ingredient_mappings = [
            (1, [(1, 1), (5, 2), (6, 1), (7, 1), (9, 1)]),  # Classic Burger
            (2, [(2, 1), (5, 3), (8, 1)]),  # Chicken Caesar Salad
            (3, [(8, 2), (6, 2), (10, 1)]),  # Margherita Pizza
            (4, [(3, 1), (15, 2), (17, 1)]),  # Grilled Salmon
            (5, [(5, 2), (6, 1), (15, 1), (16, 1)]),  # Veggie Wrap
            (6, [(1, 2), (24, 1)]),  # BBQ Ribs (assuming ground beef for ribs)
            (7, [(4, 1), (11, 1), (19, 1)]),  # Shrimp Pasta
            (8, [(5, 3), (6, 1), (16, 1)]),  # Garden Salad
            (9, [(2, 2), (25, 1)]),  # Chicken Wings
            (10, [(14, 2), (12, 1), (8, 1)]),  # Mushroom Risotto
            (11, [(3, 1), (5, 1), (6, 1)]),  # Fish Tacos
            (12, [(12, 1), (15, 1), (17, 1)]),  # Quinoa Bowl (using rice for quinoa)
            (13, [(1, 2), (13, 2)]),  # Steak Frites
            (14, [(8, 1), (6, 1), (9, 1)]),  # Caprese Sandwich
            (15, [(15, 2), (17, 1), (12, 1)]),  # Thai Curry
            (16, [(4, 2), (9, 1)]),  # Lobster Roll (using shrimp for lobster)
            (17, [(5, 2), (6, 1), (9, 1)]),  # Black Bean Burger
            (18, [(2, 1), (8, 2), (11, 1)]),  # Chicken Parmesan
            (19, [(6, 2), (8, 1), (5, 1)]),  # Greek Salad
            (20, [(4, 1), (11, 1)]),  # Pad Thai
            (21, [(15, 3), (12, 1)]),  # Stuffed Bell Peppers
            (22, [(3, 1), (13, 2)]),  # Fish and Chips
            (23, [(18, 2)]),  # Acai Bowl (using spinach as substitute)
            (24, [(1, 1), (6, 1), (7, 1)]),  # Lamb Gyro (using ground beef)
            (25, [(15, 2), (8, 1), (11, 1)])  # Eggplant Parmesan
        ]

        for menu_item_id, ingredients in ingredient_mappings:
            for resource_id, amount in ingredients:
                ingredient_data = {
                    "menu_item_id": menu_item_id,
                    "resource_id": resource_id,
                    "amount": amount
                }
                response = requests.post(f"{self.base_url}/menu_item_ingredients/", json=ingredient_data)
                if response.status_code == 200:
                    self.created_ids["menu_item_ingredients"].append(response.json()["id"])
                    print(f"✓ Added ingredient to menu item {menu_item_id}")
                else:
                    print(f"✗ Failed to add ingredient to menu item {menu_item_id} - {response.text}")

    def create_promotions(self):
        """Create sample promotions"""
        print("\nCreating promotions...")
        promotions = [
            {
                "code": "WELCOME10",
                "description": "10% off for new customers",
                "discount_percent": 10,
                "expiration_date": (datetime.now() + timedelta(days=30)).isoformat()
            },
            {
                "code": "LUNCH15",
                "description": "15% off lunch orders",
                "discount_percent": 15,
                "expiration_date": (datetime.now() + timedelta(days=60)).isoformat()
            },
            {
                "code": "WEEKEND20",
                "description": "20% off weekend orders",
                "discount_percent": 20,
                "expiration_date": (datetime.now() + timedelta(days=90)).isoformat()
            },
            {
                "code": "STUDENT5",
                "description": "5% student discount",
                "discount_percent": 5,
                "expiration_date": (datetime.now() + timedelta(days=365)).isoformat()
            },
            {
                "code": "EXPIRED",
                "description": "Expired promotion for testing",
                "discount_percent": 25,
                "expiration_date": (datetime.now() - timedelta(days=1)).isoformat()
            }
        ]

        for promo in promotions:
            response = requests.post(f"{self.base_url}/promotions/", json=promo)
            if response.status_code == 200:
                self.created_ids["promotions"].append(response.json()["id"])
                print(f"✓ Created promotion: {promo['code']}")
            else:
                print(f"✗ Failed to create promotion: {promo['code']} - {response.text}")

    def create_orders(self):
        """Create sample orders with order details and payments"""
        print("\nCreating orders...")

        order_types = ["dine_in", "takeout", "delivery"]
        promo_codes = ["WELCOME10", "LUNCH15", None, None, None]  # Some orders without promos

        for i in range(SAMPLE_SIZE["orders"]):
            # For simplicity, let's create all orders as regular orders and handle guest vs customer differently
            use_customer = random.choice([True, False]) and self.created_ids["customers"]

            if use_customer:
                # Registered customer order
                order_data = {
                    "customer_id": random.choice(self.created_ids["customers"]),
                    "order_type": random.choice(order_types),
                    "description": f"Sample order {i+1}",
                    "promotion_code": random.choice(promo_codes)
                }
            else:
                # Guest order (customer_id will be None)
                guest_names = ["Alex Guest", "Sam Visitor", "Jordan Traveler", "Casey Tourist", "Riley Passerby"]
                order_data = {
                    "customer_id": None,
                    "order_type": random.choice(order_types),
                    "description": f"Guest order {i+1}",
                    "promotion_code": random.choice(promo_codes),
                    "guest_name": random.choice(guest_names) + f" {random.randint(1, 999)}",
                    "guest_phone": f"919555{random.randint(1000, 9999)}",
                    "guest_email": f"guest{i}@example.com"
                }

            response = requests.post(f"{self.base_url}/orders/", json=order_data)

            if response.status_code == 200:
                order_id = response.json()["id"]
                self.created_ids["orders"].append(order_id)
                order_type = "customer" if use_customer else "guest"
                print(f"✓ Created {order_type} order {order_id}")

                # Add order details for all orders
                self.create_order_details(order_id)

                # Create payment for some orders (skip for some to test unpaid orders)
                if random.choice([True, True, False]):  # 2/3 probability
                    self.create_payment(order_id)

            else:
                print(f"✗ Failed to create order {i+1} - {response.text}")

    def create_orders(self):
        """Create sample orders with order details and payments"""
        print("\nCreating orders...")

        order_types = ["dine_in", "takeout", "delivery"]
        promo_codes = ["WELCOME10", "LUNCH15", None, None, None]  # Some orders without promos

        for i in range(SAMPLE_SIZE["orders"]):
            # For simplicity, let's create all orders as regular orders and handle guest vs customer differently
            use_customer = random.choice([True, False]) and self.created_ids["customers"]

            if use_customer:
                # Registered customer order
                order_data = {
                    "customer_id": random.choice(self.created_ids["customers"]),
                    "order_type": random.choice(order_types),
                    "description": f"Sample order {i+1}",
                    "promotion_code": random.choice(promo_codes)
                }
            else:
                # Guest order (customer_id will be None)
                guest_names = ["Alex Guest", "Sam Visitor", "Jordan Traveler", "Casey Tourist", "Riley Passerby"]
                order_data = {
                    "customer_id": None,
                    "order_type": random.choice(order_types),
                    "description": f"Guest order {i+1}",
                    "promotion_code": random.choice(promo_codes),
                    "guest_name": random.choice(guest_names) + f" {random.randint(1, 999)}",
                    "guest_phone": f"919555{random.randint(1000, 9999)}",
                    "guest_email": f"guest{i}@example.com"
                }

            response = requests.post(f"{self.base_url}/orders/", json=order_data)

            if response.status_code == 200:
                order_id = response.json()["id"]
                self.created_ids["orders"].append(order_id)
                order_type = "customer" if use_customer else "guest"
                print(f"✓ Created {order_type} order {order_id}")

                # Add order details for all orders
                self.create_order_details(order_id)

                # Create payment for some orders (skip for some to test unpaid orders)
                if random.choice([True, True, False]):  # 2/3 probability
                    self.create_payment(order_id)

            else:
                print(f"✗ Failed to create order {i+1} - {response.text}")

    def create_order_details(self, order_id):
        """Create order details for a specific order"""
        if not self.created_ids["menu_items"]:
            return

        num_items = random.randint(1, 4)
        for _ in range(num_items):
            detail_data = {
                "order_id": order_id,
                "menu_item_id": random.choice(self.created_ids["menu_items"]),
                "amount": random.randint(1, 3)
            }
            response = requests.post(f"{self.base_url}/orderdetails/", json=detail_data)
            if response.status_code == 200:
                self.created_ids["order_details"].append(response.json()["id"])

    def create_payment(self, order_id):
        """Create payment for a specific order"""
        payment_types = ["cash", "credit_card", "debit_card"]
        payment_data = {
            "order_id": order_id,
            "amount": round(random.uniform(10.0, 50.0), 2),
            "payment_type": random.choice(payment_types),
            "status": random.choice(["completed", "pending", "completed", "completed"])  # Mostly completed
        }

        response = requests.post(f"{self.base_url}/payments/", json=payment_data)
        if response.status_code == 200:
            self.created_ids["payments"].append(response.json()["id"])

    def create_reviews(self):
        """Create sample reviews"""
        print("\nCreating reviews...")

        if not self.created_ids["menu_items"]:
            print("No menu items found, skipping reviews")
            return

        reviewer_names = [
            "Alice Johnson", "Bob Smith", "Carol Williams", "David Brown",
            "Emma Davis", "Frank Miller", "Grace Wilson", "Henry Moore",
            "Ivy Taylor", "Jack Anderson", "Kate Thomas", "Liam Jackson",
            "Mia White", "Noah Harris", "Olivia Martin", "Paul Thompson"
        ]

        review_texts = [
            "Absolutely delicious! Will definitely order again.",
            "Good food, but service was a bit slow.",
            "Amazing flavors and great presentation!",
            "Not bad, but could use more seasoning.",
            "Perfect portion size and very tasty.",
            "Outstanding quality, highly recommend!",
            "Food was cold when it arrived.",
            "Fresh ingredients and excellent preparation.",
            "A bit overpriced for the portion size.",
            "Fantastic taste, cooked to perfection!",
            "Average food, nothing special.",
            "Loved the creative combination of flavors.",
            "Would have been better if it was warmer.",
            "Exceptional quality and service!",
            "Too salty for my taste.",
            "Beautiful presentation and great taste!",
            None,  # Some reviews without text
            None,
            None
        ]

        for i in range(SAMPLE_SIZE["reviews"]):
            review_data = {
                "menu_item_id": random.choice(self.created_ids["menu_items"]),
                "customer_name": random.choice(reviewer_names),
                "rating": random.choices([1, 2, 3, 4, 5], weights=[5, 10, 20, 35, 30])[0],  # Weighted toward higher ratings
                "review_text": random.choice(review_texts)
            }

            response = requests.post(f"{self.base_url}/reviews/", json=review_data)
            if response.status_code == 200:
                print(f"✓ Created review {i+1}")
            else:
                print(f"✗ Failed to create review {i+1} - {response.text}")

    def generate_all_data(self):
        """Generate all sample data in correct order"""
        print("🚀 Starting sample data generation...\n")

        try:
            # First, clear existing data (optional)
            # self.clear_database()  # Uncomment if you want to clear first

            # Create data in dependency order
            self.create_customers()
            self.create_resources()
            self.create_menu_items()
            self.create_menu_item_ingredients()
            self.create_promotions()
            self.create_orders()
            self.create_reviews()

            print(f"\n✅ Sample data generation completed!")
            print(f"Created:")
            for entity, ids in self.created_ids.items():
                if ids:
                    print(f"  - {len(ids)} {entity}")

        except Exception as e:
            print(f"\n❌ Error during data generation: {e}")

    def clear_database(self):
        """Clear all data from database (use with caution!)"""
        print("⚠️  Clearing database...")
        response = requests.delete(
            f"{self.base_url}/administrator_actions/purge-db",
            params={"confirm": "DELETE_ALL_DATA"}
        )
        if response.status_code == 200:
            print("✓ Database cleared")
        else:
            print(f"✗ Failed to clear database: {response.text}")


def main():
    """Main function to run the sample data generator"""
    generator = SampleDataGenerator()

    print("Restaurant Order System - Sample Data Generator")
    print("=" * 50)

    # Ask user if they want to clear existing data
    clear_data = input("Do you want to clear existing data first? (y/N): ").lower().strip()
    if clear_data == 'y':
        generator.clear_database()
        print()

    # Generate all sample data
    generator.generate_all_data()

    print("\n🎉 Sample data generation completed!")
    print("\nYou can now:")
    print("- Browse the API at http://localhost:8000/docs")
    print("- Test customer actions like placing orders")
    print("- View staff analytics and reports")
    print("- Test inventory management features")


if __name__ == "__main__":
    main()