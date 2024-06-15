-- Create database
CREATE DATABASE consequence_db;

-- Create consequence_data table
CREATE TABLE consequence_data(
  公司代码  char(6)  NOT NULL,
  日期  char(10)  NOT NULL,
  值   float  NOT NULL,
  PRIMARY KEY (公司代码, 日期)
)ENGINE=InnoDB;