from sqlalchemy import text, inspect
from api.dependencies.database import engine


def check_and_add_columns():
    """
    Check if columns exist before adding them
    """
    inspector = inspect(engine)

    with engine.connect() as connection:
        try:
            print("🔍 Checking existing database structure...")

            # Get existing columns for orders table
            existing_columns = [col['name'] for col in inspector.get_columns('orders')]
            print(f"Existing columns in orders table: {existing_columns}")

            # Define new columns to add
            new_columns = {
                'tracking_number': "ALTER TABLE orders ADD COLUMN tracking_number VARCHAR(20)",
                'subtotal': "ALTER TABLE orders ADD COLUMN subtotal DECIMAL(10,2)",
                'tax_amount': "ALTER TABLE orders ADD COLUMN tax_amount DECIMAL(10,2)",
                'discount_amount': "ALTER TABLE orders ADD COLUMN discount_amount DECIMAL(10,2) DEFAULT 0",
                'total_amount': "ALTER TABLE orders ADD COLUMN total_amount DECIMAL(10,2)",
                'promotion_code': "ALTER TABLE orders ADD COLUMN promotion_code VARCHAR(50)",
                'guest_name': "ALTER TABLE orders ADD COLUMN guest_name VARCHAR(100)",
                'guest_phone': "ALTER TABLE orders ADD COLUMN guest_phone VARCHAR(20)",
                'guest_email': "ALTER TABLE orders ADD COLUMN guest_email VARCHAR(100)"
            }

            # Add missing columns
            for column_name, query in new_columns.items():
                if column_name not in existing_columns:
                    try:
                        connection.execute(text(query))
                        print(f"✓ Added column: {column_name}")
                    except Exception as e:
                        print(f"⚠ Error adding {column_name}: {e}")
                else:
                    print(f"⚠ Column {column_name} already exists, skipping...")

            # Make customer_id nullable
            try:
                connection.execute(text("ALTER TABLE orders MODIFY COLUMN customer_id INT NULL"))
                print("✓ Made customer_id nullable")
            except Exception as e:
                print(f"⚠ customer_id modification: {e}")

            # Add unique constraint and index for tracking_number
            try:
                connection.execute(text("ALTER TABLE orders ADD UNIQUE INDEX idx_tracking_number (tracking_number)"))
                print("✓ Added unique index for tracking_number")
            except Exception as e:
                print(f"⚠ Index creation: {e}")

            # Update existing orders with tracking numbers
            try:
                connection.execute(text("""
                                        UPDATE orders
                                        SET tracking_number = CONCAT('ORD', LPAD(id, 6, '0'))
                                        WHERE tracking_number IS NULL
                                        """))
                print("✓ Updated existing orders with tracking numbers")
            except Exception as e:
                print(f"⚠ Tracking number update: {e}")

            connection.commit()
            print("✅ Migration completed successfully!")

        except Exception as e:
            connection.rollback()
            print(f"❌ Migration failed: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    check_and_add_columns()