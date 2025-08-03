## Installing necessary packages:  
* `pip install fastapi`
* `pip install "uvicorn[standard]"`  
* `pip install sqlalchemy`  
* `pip install pymysql`
* `pip install pytest`
* `pip install pytest-mock`
* `pip install httpx`
* `pip install cryptography`
* `pip install pydantic`
* `pip install requests`
* `pip install redis`

### BEFORE RUNNING SERVER:
* Ensure that database name matches name found in *api/dependencies/config.py*
# If database already exists:
* Drop the schema and reinitialize it

### Run the server:
`uvicorn api.main:app --reload`
### Test API by built-in docs:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)


### KEY API ENDPOINTS SUMMARY:

**CUSTOMER ENDPOINTS:**
* POST /customer_actions/orders/guest - Place order without account
* GET /customer_actions/orders/track/{tracking_number} - Track order
* GET /customer_actions/menu/search - Search menu with filters
* GET /menu_items/search - Alternative menu search

**STAFF ENDPOINTS:**
* GET /staff_actions/inventory/low-stock - Check low inventory
* GET /staff_actions/revenue/daily?target_date=YYYY-MM-DD - Daily revenue
* GET /staff_actions/analytics/menu-performance - Menu item performance
* GET /staff_actions/analytics/review-insights - Review analysis
* GET /staff_actions/orders/date-range - Orders by date
* POST /staff_actions/inventory/check-availability - Verify stock

**ORDER MANAGEMENT:**
* POST /orders/guest - Create guest order
* GET /orders/track/{tracking_number} - Track any order
* PUT /orders/{id}/confirm - Confirm order (staff)
* POST /orders/{id}/check-inventory - Check if order can be fulfilled

**PAYMENT PROCESSING:**
* POST /payments/process/{order_id} - Process payment
* GET /payments/order/{order_id} - Get payment status
