CREATE TABLE "employees" (
  id serial PRIMARY KEY,
  name varchar,
  last_name varchar,
  hire_date DATE,
  salary int,
  email varchar,
  manager_id int,
  department_id int
);

CREATE TABLE "departments" (
  id serial PRIMARY KEY,
  name varchar,
  location_id int,
  manager_id int
);

CREATE TABLE "locations" (
  id serial PRIMARY KEY,
  address varchar,
  region_id int
);

CREATE TABLE "regions" (
  id serial PRIMARY KEY,
  name varchar
);
