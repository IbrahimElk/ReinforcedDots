class Transposition_Table:
    def __init__(self):
        self.cache = {}
        self.hits = 0
        self.misses = 0

    def get(self, key):
        if key in self.cache:
            self.hits += 1
            return self.cache[key]
        else:
            self.misses += 1
            return None

    def set(self, key, value):
        self.cache[key] = value

    def get_hits(self):
        return self.hits
    
    def get_misses(self):
        return self.misses
    
    def get_cache(self) -> dict:
        return self.cache