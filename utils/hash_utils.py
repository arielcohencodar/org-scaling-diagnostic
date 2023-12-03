import hashlib

def get_industry_hash(selected_industry):
    return int(hashlib.sha256(selected_industry.encode('utf-8')).hexdigest(), 16) % (10**8)