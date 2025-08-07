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
* The `db_password` in `config.py` must match your MySQL root password
# If database already exists:
* Drop the schema and reinitialize it

### Run the server:
`uvicorn api.main:app --reload`
### Test API by built-in docs:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)



