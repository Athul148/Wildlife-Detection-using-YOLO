CREATE DATABASE wildguard_ai;
USE wildguard_ai;

CREATE TABLE detection_results1 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    species_name VARCHAR(100),
    count INT,
    animal_count Int, 
    human_count INT,
    vehicle_count INT,
    risk_score INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

alter table detection_results1 add rare_found int;
describe detection_results1;

create table species_results(detection_id INT AUTO_INCREMENT PRIMARY KEY,species_name VARCHAR(100),count INT);


select * from detection_results1;
select * from species_results;

