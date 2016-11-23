DROP TABLE if EXISTS users;
DROP TABLE if EXISTS wishlists;

CREATE TABLE users (
  username text,
  email text,
  password text
);

CREATE TABLE wishlists (
  wish integer primary key autoincrement,
  title text not null,
  quantity number not null,
  price text not null,
  details text not null
);

