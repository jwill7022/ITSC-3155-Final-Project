### Installing necessary packages:  
* `pip install fastapi`
* `pip install "uvicorn[standard]"`  
* `pip install sqlalchemy`  
* `pip install pymysql`
* `pip install pytest`
* `pip install pytest-mock`
* `pip install httpx`
* `pip install cryptography`

### BEFORE RUNNING SERVER:
* Ensure that database name matches name found in *api/dependencies/config.py*
## If database already exists:
* Run file **migration_script.py** to ensure that all proper columns are added to the database.

### Run the server:
`uvicorn api.main:app --reload`
### Test API by built-in docs:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
