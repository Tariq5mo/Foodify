
#!/usr/bin/python3
"""This module instantiates an object of classes FileStorage and DBStorage"""

from models.engine.db_storage import DBStorage
storage = DBStorage()

storage.reload()
