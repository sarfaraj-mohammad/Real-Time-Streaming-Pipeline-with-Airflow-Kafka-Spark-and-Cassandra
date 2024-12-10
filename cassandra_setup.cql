CREATE KEYSPACE IF NOT EXISTS social_network WITH replication = {'class': 'SimpleStrategy', 'replication_factor':1};

CREATE TABLE IF NOT EXISTS social_network.users(
    full_name TEXT PRIMARY KEY,
    email TEXT,
    contact_number BIGINT,
    username TEXT,
    password TEXT,
    date_of_birth TIMESTAMP,
    age INT,
    gender TEXT,
    street_address TEXT,
    city TEXT,
    state TEXT,
    country TEXT,
    postcode TEXT
);
