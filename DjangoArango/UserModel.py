from arango_orm import Collection
from arango_orm.fields import String, Date, Integer, Boolean, DateTime
from datetime import datetime

# Arango 
from arango import ArangoClient
from arango_orm import Database

# connect
client = ArangoClient(hosts='http://localhost:8529')
sys_db = client.db("_system", username="root", password="Abcd@123")
test_db = client.db('test', username='root', password='Abcd@123')
db = Database(test_db)

def valid_username(username):
    """
    return True if username is valid
    """
    users = db.query(User).all()
    for user in users:
        if user.username == username:
            return False
    return True


class User(Collection):

    __collection__ = 'user'
    _index = [{'type': 'hash', 'unique': False, 'fields': ['username']}]
    # _key = String(required=True)

    # firstname = String(required=True, allow_none=True)
    # lastname = String(required=True, allow_none=True)
    username = String(required=True, allow_none=False)
    password = String(required=True, allow_none=False)
    email = String(required=True, allow_none=False)
    is_active = Boolean(required=True, default=False, allow_none=False)
    is_superuser = Boolean(required=True, default=False, allow_none=False)
    dob = Date(required=True, allow_none=True)
    # createdate = DateTime(required=True, allow_none=False)

    @property
    def key(self):
        return self._key