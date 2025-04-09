CREATE OR REPLACE SCHEMA cortex_analyst_demo.employee_demo;

CREATE TABLE employee_dim (
  emp_id STRING PRIMARY KEY,
  emp_name STRING,
  emp_firstname STRING,
  emp_lastname STRING,
  doj DATE,
  original_doj DATE,
  on_probation STRING,
  probation_end_date DATE,
  manager_emp_id STRING,
  gender STRING,
  employment_status STRING,
  designation STRING,
  business_area STRING,
  department STRING,
  team_name STRING,
  marital_status STRING,
  dob DATE,
  official_mail_id STRING,
  personal_mail_id STRING,
  primary_language STRING,
  primary_phone STRING,
  base_location STRING
);

CREATE TABLE ctc_dim (
  emp_id STRING PRIMARY KEY,
  fixed_ctc NUMBER(10, 2),
  ctc_effective_date DATE,
  ctc_revision_reason STRING,
  variable_ctc NUMBER(10, 2),
  variable_ctc_effective_date DATE
);

CREATE TABLE designation_dim (
  emp_id STRING PRIMARY KEY,
  previous_org STRING,
  designation STRING,
  designation_effective_date DATE,
  designation_end_date DATE
);



INSERT INTO cortex_analyst_demo.employee_demo.employee_dim (
  emp_id, emp_name, emp_firstname, emp_lastname, doj, original_doj, on_probation, probation_end_date,
  manager_emp_id, gender, employment_status, designation, business_area, department, team_name,
  marital_status, dob, official_mail_id, personal_mail_id, primary_language, primary_phone, base_location
) VALUES
('E001', 'Amit Kulkarni', 'Amit', 'Kulkarni', '2023-02-10', '2023-02-10', 'No', NULL, 'E004', 'Male', 'Active', 'Developer', 'Engineering', 'Data', 'Data Platform', 'Single', '1996-04-14', 'amit.kulkarni@xyz.com', 'amit.k@gmail.com', 'English', '9876543210', 'Pune'),
('E002', 'Sneha Patil', 'Sneha', 'Patil', '2022-08-15', '2022-08-15', 'No', NULL, 'E004', 'Female', 'Active', 'Developer', 'Engineering', 'Data', 'Data Platform', 'Married', '1994-06-22', 'sneha.patil@xyz.com', 'sneha.p@gmail.com', 'English', '9876543211', 'Bangalore'),
('E003', 'Rahul Nair', 'Rahul', 'Nair', '2021-11-01', '2021-11-01', 'No', NULL, 'E005', 'Male', 'Active', 'Developer', 'Engineering', 'App Dev', 'Mobile Apps', 'Single', '1995-12-10', 'rahul.nair@xyz.com', 'rahul.n@gmail.com', 'English', '9876543212', 'Chennai'),
('E004', 'Neha Sharma', 'Neha', 'Sharma', '2020-06-01', '2020-06-01', 'No', NULL, 'E006', 'Female', 'Active', 'Lead', 'Engineering', 'Data', 'Data Platform', 'Married', '1990-02-18', 'neha.sharma@xyz.com', 'nehasharma@yahoo.com', 'Hindi', '9876543213', 'Pune'),
('E005', 'Rohan Joshi', 'Rohan', 'Joshi', '2019-03-15', '2019-03-15', 'No', NULL, 'E006', 'Male', 'Active', 'Lead', 'Engineering', 'App Dev', 'Mobile Apps', 'Married', '1989-07-04', 'rohan.joshi@xyz.com', 'rohan.j@gmail.com', 'Marathi', '9876543214', 'Mumbai'),
('E006', 'Anjali Mehta', 'Anjali', 'Mehta', '2016-01-01', '2016-01-01', 'No', NULL, NULL, 'Female', 'Active', 'Manager', 'Engineering', 'Data', 'Data Org', 'Married', '1985-08-09', 'anjali.mehta@xyz.com', 'anjali.mehta@gmail.com', 'English', '9876543215', 'Pune'),
('E007', 'Vinod Singh', 'Vinod', 'Singh', '2024-01-10', '2024-01-10', 'Yes', '2024-07-10', 'E005', 'Male', 'Active', 'Developer', 'Engineering', 'App Dev', 'Mobile Apps', 'Single', '1997-05-01', 'vinod.singh@xyz.com', 'vinod.s@gmail.com', 'Hindi', '9876543216', 'Bangalore'),
('E008', 'Isha Khatri', 'Isha', 'Khatri', '2023-09-05', '2023-09-05', 'No', NULL, 'E004', 'Female', 'Active', 'Developer', 'Engineering', 'Data', 'Analytics', 'Single', '1998-11-11', 'isha.khatri@xyz.com', 'isha.k@gmail.com', 'English', '9876543217', 'Hyderabad'),
('E009', 'Kunal Rao', 'Kunal', 'Rao', '2022-03-20', '2022-03-20', 'No', NULL, 'E006', 'Male', 'Active', 'Lead', 'Engineering', 'Web Dev', 'Frontend', 'Married', '1993-09-14', 'kunal.rao@xyz.com', 'kunal.rao@gmail.com', 'Kannada', '9876543218', 'Bangalore'),
('E010', 'Tanya Kapoor', 'Tanya', 'Kapoor', '2023-06-12', '2023-06-12', 'Yes', '2023-12-12', 'E009', 'Female', 'Active', 'Developer', 'Engineering', 'Web Dev', 'Frontend', 'Single', '1999-03-03', 'tanya.kapoor@xyz.com', 'tanyakapoor@hotmail.com', 'English', '9876543219', 'Delhi');


INSERT INTO ctc_dim (
  emp_id, fixed_ctc, ctc_effective_date, ctc_revision_reason, variable_ctc, variable_ctc_effective_date
) VALUES
('E001', 700000, '2023-02-10', 'New Hire', 100000, '2023-02-10'),
('E002', 750000, '2022-08-15', 'New Hire', 120000, '2022-08-15'),
('E003', 720000, '2021-11-01', 'New Hire', 100000, '2021-11-01'),
('E004', 950000, '2020-06-01', 'Promotion', 150000, '2020-06-01'),
('E005', 960000, '2019-03-15', 'Promotion', 150000, '2019-03-15'),
('E006', 1200000, '2016-01-01', 'Manager Role', 200000, '2016-01-01'),
('E007', 680000, '2024-01-10', 'New Hire', 90000, '2024-01-10'),
('E008', 710000, '2023-09-05', 'New Hire', 95000, '2023-09-05'),
('E009', 980000, '2022-03-20', 'Internal Movement', 140000, '2022-03-20'),
('E010', 690000, '2023-06-12', 'New Hire', 80000, '2023-06-12');

INSERT INTO designation_dim (
  emp_id, previous_org, designation, designation_effective_date, designation_end_date
) VALUES
('E001', 'TCS', 'Developer', '2023-02-10', NULL),
('E002', 'Infosys', 'Developer', '2022-08-15', NULL),
('E003', 'Cognizant', 'Developer', '2021-11-01', NULL),
('E004', 'Accenture', 'Lead', '2020-06-01', NULL),
('E005', 'Wipro', 'Lead', '2019-03-15', NULL),
('E006', 'IBM', 'Manager', '2016-01-01', NULL),
('E007', 'Capgemini', 'Developer', '2024-01-10', NULL),
('E008', 'Fresher', 'Developer', '2023-09-05', NULL),
('E009', 'Infosys', 'Lead', '2022-03-20', NULL),
('E010', 'TCS', 'Developer', '2023-06-12', NULL);

CREATE TABLE cortex_analyst_demo.employee_demo.rating_dim (
  emp_id VARCHAR(10),
  rating_cycle VARCHAR(20),
  review_period_start_date DATE,
  review_period_end_date DATE,
  rating INT,
  emp_id_of_rater VARCHAR(10),
  date_of_review DATE
);


INSERT INTO cortex_analyst_demo.employee_demo.rating_dim (
  emp_id, rating_cycle, review_period_start_date, review_period_end_date, rating, emp_id_of_rater, date_of_review
) VALUES
('E001', 'Half Yearly', '2024-01-01', '2024-06-30', 4, 'E004', '2024-07-10'),
('E002', 'Half Yearly', '2024-01-01', '2024-06-30', 5, 'E004', '2024-07-11'),
('E003', 'Half Yearly', '2024-01-01', '2024-06-30', 3, 'E005', '2024-07-12'),
('E007', 'Half Yearly', '2024-01-10', '2024-06-30', 4, 'E005', '2024-07-05'),
('E004', 'Half Yearly', '2024-01-01', '2024-06-30', 5, 'E006', '2024-07-15'),
('E005', 'Half Yearly', '2024-01-01', '2024-06-30', 4, 'E006', '2024-07-14'),
('E008', 'Half Yearly', '2024-01-01', '2024-06-30', 4, 'E004', '2024-07-08'),
('E009', 'Half Yearly', '2024-01-01', '2024-06-30', 5, 'E006', '2024-07-13'),
('E010', 'Half Yearly', '2024-01-01', '2024-06-30', 4, 'E009', '2024-07-09');


