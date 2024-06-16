# Online Library on FastAPI
## Setup
Clone a project
```bash
git clone https://github.com/WISPukh/fastApi_Project.git
```
Create virtual environment and activate it
```bash
python -m venv venv
source venv/bin/activate
```
Then install dependencies
```bash
pip install -r requirements.txt
```
in `alembic.ini` change that line to your database url:
```alembic
sqlalchemy.url = postgresql://user:password@host/database_name
```
Once `pip` has finished downloading the dependencies create and fill your `.env` file using `.env.sample`

The last thing to do is to apply alembic migration:
```bash
alembic upgrade head
```

Once migrations have applied, you can start the server:
```bash
python -m main
```