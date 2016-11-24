DROP TABLE if EXISTS users;
DROP TABLE if EXISTS wishlists;

CREATE TABLE users (
  id integer primary key autoincrement,
  username text not null,
  email text not null,
  password text not null
);

CREATE TABLE wishlists (
  wish integer primary key autoincrement,
  title text not null,
  quantity number not null,
  price text not null,
  details text not null
);

