CREATE DATABASE crm_system;
USE crm_system;

CREATE TABLE master (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255),
    firm VARCHAR(255),
    title VARCHAR(255),
    region VARCHAR(100),
    location_ VARCHAR(255),
    function_ VARCHAR(100),
    group_name VARCHAR(100),
    focus VARCHAR(255),
    prior_firm VARCHAR(255),
    notes TEXT,
    sr VARCHAR(10),
    off_limits VARCHAR(50),
    ix INT,
    date_added DATE,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
