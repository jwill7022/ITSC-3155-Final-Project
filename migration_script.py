from sqlalchemy import text
from api.dependencies.database import engine, SessionLocal


def migrate_database():
    """
    Add new columns to existing tables
    Run this script once to update your database schema
    """
    with engine.connect() as connection:
        try:
            print("Starting database migration...")

            # Add new columns to orders table
            migration_queries = [
                # Orders table updates
                "ALTER TABLE orders ADD COLUMN tracking_number VARCHAR(20) UNIQUE",
                "ALTER TABLE orders ADD COLUMN subtotal DECIMAL(10,2)",
                "ALTER TABLE orders ADD COLUMN tax_amount DECIMAL(10,2)",
                "ALTER TABLE orders ADD COLUMN discount_amount DECIMAL(10,2) DEFAULT 0",
                "ALTER TABLE orders ADD COLUMN total_amount DECIMAL(10,2)",
                "ALTER TABLE orders ADD COLUMN promotion_code VARCHAR(50)",
                "ALTER TABLE orders ADD COLUMN guest_name VARCHAR(100)",
                "ALTER TABLE orders ADD COLUMN guest_phone VARCHAR(20)",
                "ALTER TABLE orders ADD COLUMN guest_email VARCHAR(100)",
                "ALTER TABLE orders MODIFY COLUMN customer_id INT NULL",

                # Add index for tracking number
                "CREATE INDEX idx_orders_tracking_number ON orders(tracking_number)",

                # Update existing orders with tracking numbers
                """UPDATE orders
                   SET tracking_number = CONCAT('ORD', LPAD(id, 6, '0'))
                   WHERE tracking_number IS NULL""",
            ]

            for query in migration_queries:
                try:
                    connection.execute(text(query))
                    print(f"✓ Executed: {query[:50]}...")
                except Exception as e:
                    if "Duplicate column name" in str(e) or "already exists" in str(e):
                        print(f"⚠ Column already exists, skipping: {query[:50]}...")
                    else:
                        print(f"✗ Error executing {query[:50]}...: {e}")

            connection.commit()
            print("Database migration completed successfully!")

        except Exception as e:
            connection.rollback()
            print(f"Migration failed: {e}")


if __name__ == "__main__":
    migrate_database()