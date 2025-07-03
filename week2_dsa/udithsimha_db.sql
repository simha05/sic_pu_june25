CREATE DATABASE udithsimha_db;
USE udithsimha_db;
CREATE TABLE employees (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(30) NOT NULL,
    designation VARCHAR(30),
    phone_number BIGINT UNIQUE,
    salary FLOAT,
    commission FLOAT DEFAULT 0,
    years_of_experience TINYINT,
    technology VARCHAR(30) NOT NULL
);
INSERT INTO employees (name, designation, phone_number, salary, commission, years_of_experience, technology) VALUES
('Alice Johnson', 'Developer', 9876543210, 85000, 5000, 5, 'Java'),
('Bob Smith', 'Manager', 9123456789, 120000, 15000, 10, 'Project Management'),
('Charlie Brown', 'Tester', 9988776655, 60000, 0, 3, 'Selenium'),
('Diana Prince', 'Developer', 9234567890, 90000, 7000, 7, 'Python'),
('Ethan Hunt', 'DevOps Engineer', 9345678901, 95000, 4000, 6, 'AWS');
INSERT INTO employees (name, designation, phone_number, salary, years_of_experience, technology) VALUES
('Fiona Glenanne', 'Developer', 9456789012, 88000, 4, 'JavaScript'),
('George Miller', NULL, 9567890123, 70000, 2, 'Ruby'),
('Hannah Baker', 'QA Engineer', NULL, 65000, 3, 'Manual Testing'),
('Ian Curtis', 'Developer', 9678901234, 85000, 5, 'C#'),
('Jane Eyre', NULL, 9789012345, 72000, 3, 'PHP');
INSERT INTO employees (name, years_of_experience, technology) VALUES
('Kevin Hart', 1, 'Go'),
('Lana Del Rey', 2, 'Swift'),
('Mike Tyson', 4, 'Kotlin'),
('Nina Simone', 3, 'Scala'),
('Oscar Wilde', 2, 'Perl');
INSERT INTO employees (name, designation, phone_number, salary, commission, years_of_experience, technology) VALUES
('Paul Newman', 'Architect', NULL, 110000, NULL, 12, 'C++'),
('Quinn Fabray', NULL, 9898989898, NULL, 0, 3, 'React'),
('Rachel Green', 'Designer', 9797979797, 75000, NULL, 4, 'UX/UI'),
('Steve Rogers', 'Developer', NULL, 80000, 3000, 6, 'Java'),
('Tina Turner', 'Manager', 9696969696, 100000, 10000, 8, 'Scrum');
