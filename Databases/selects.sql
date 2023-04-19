-- Показать работников у которых нет почты или почта не в корпоративном домене (домен dualbootpartners.com)
SELECT * FROM employees
WHERE email is NULL or email NOT LIKE '%@dualbootpartners.com';


-- Получить список работников нанятых в последние 30 дней
SELECT * FROM employees
WHERE hire_date > now() - interval '30 day';


-- Найти максимальную и минимальную зарплату по каждому департаменту
SELECT
    d.name,
    max(e.salary) as max_salary,
    min(e.salary) as min_salary
FROM departments d
LEFT JOIN employees e
    ON d.id = e.department_id
GROUP BY d.name;



-- Посчитать количество работников в каждом регионе
SELECT r.name, count(e.id) FROM employees e
LEFT JOIN departments d
    ON d.id = e.department_id
LEFT JOIN locations l
    ON l.id = d.location_id
LEFT JOIN regions r
    ON r.id = l.region_id
GROUP BY r.name;


-- Показать сотрудников у которых фамилия длиннее 10 символов
SELECT * FROM employees
WHERE length(last_name) > 10;

-- Показать сотрудников с зарплатой выше средней по всей компании
SELECT * FROM employees
WHERE salary > (SELECT avg(salary) from employees);
