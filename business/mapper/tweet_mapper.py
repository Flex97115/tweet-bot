

def to_json(tweet):
    if tweet:
        return tweet._json


def flatten_cursor(cursor):
    items = []
    for item in cursor.items():
        items.append(item)
    return items
