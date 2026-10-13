# PROBLEM: In-Memory Database
#
# Implement an in-memory database that stores records.
#
# Each record has:
#   - A unique string key
#   - Multiple fields, each mapped to an integer value
#
# Implement the following operations:
#
# 1. set(key, field, value)
#    - Insert or update a field in a record.
#    - Create the record if it doesn't exist.
#
# 2. get(key, field)
#    - Return the field's value.
#    - Return None if the key or field doesn't exist.
#
# 3. delete(key, field)
#    - Delete the specified field.
#    - Return True if deleted, otherwise False.
#    - Remove the record if no fields remain.
#
# 4. scan(key)
#    - Return all fields and values for a record.
#    - Sort fields alphabetically.
#    - Return a list of (field, value) tuples.
#    - Return [] if the record doesn't exist.
#
# EXAMPLE:
#
# db = InMemoryDB()
#
# db.set("user1", "age", 21)
# db.set("user1", "score", 95)
# db.set("user2", "age", 25)
#
# db.get("user1", "age")     -> 21
# db.get("user1", "name")    -> None
# db.scan("user1")          -> [("age", 21), ("score", 95)]
# db.delete("user1", "age")  -> True
# db.delete("user1", "age")  -> False
# db.scan("user1")          -> [("score", 95)]
#
# REQUIREMENTS:
# - All data must be stored in memory.
# - No external databases or third-party packages.
# - Aim for efficient operations.
#
# FOLLOW-UPS (DO NOT IMPLEMENT YET):
# Level 2: Prefix-based field scanning
# Level 3: TTL and automatic expiration
# Level 4: Backup and restore
#
# TARGET: 20 minutes for Level 1.
class InMemoryDB:
    def __init__(self):
        self.records = {}

    def set(self, key, field, value):
        if key not in self.records:
            self.records[key] = {}
        self.records[key][field] = value
    
    def get(self, key, field):
        if key not in self.records or field not in self.records[key]:
            return False
        return self.records[key][field]


    def delete(self, key, field):
        if key not in self.records or field not in self.records[key]:
            return False
        
        del self.records[key][field]

        if self.records[key] == {}:
            del self.records[key]

        return True
        
    def scan(self, key):
        if key in self.records:
            res = self.records[key]
            res = list(res.items())
            res.sort(key=lambda tup: (tup[0]))
            return res
        return []

    def scan_by_prefix(self, key, prefix):
        valid = []
        for field, value in self.scan(key):
            if field.startswith(prefix):
                valid.append((field, value))

        return valid

    def set_at(self, key, field, value, timestamp):
        if key not in self.records:
            self.records[key] = {}
        self.records[key][field] = (value, timestamp, float("inf"))

    def set_at_with_ttl(self, key, field, value, timestamp, ttl):
        self.set_at(key, field, value, timestamp)
        value, start_time, expiry = self.records[key][field]
        self.records[key][field] = (value, start_time, timestamp + ttl)

    def get_at(self, key, field, timestamp):
        if key not in self.records or field not in self.records[key]:
            return None

        value, start_time, expiry = self.records[key][field]
        if timestamp >= expiry or start_time > timestamp:
            return None
        return value


db = InMemoryDB()

db.set("user1", "age", 21)
db.set("user1", "address", 100)
db.set("user1", "account", 500)
db.set("user1", "score", 95)

print(db.scan_by_prefix("user1", "a"))
# [("account", 500), ("address", 100), ("age", 21)]

print(db.scan_by_prefix("user1", "addr"))
# [("address", 100)]

print(db.scan_by_prefix("user1", "xyz"))
# []

print(db.scan_by_prefix("missing", "a"))
# []

db.set_at_with_ttl("user1", "score", 95, 10, 5)

print(db.get_at("user1", "score", 12))  # 95
print(db.get_at("user1", "score", 14))  # 95
print(db.get_at("user1", "score", 15))  # None

db.set_at("user1", "score", 100, 20)

print(db.get_at("user1", "score", 100))  # 100