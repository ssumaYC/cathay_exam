CREATE DATABASE IF NOT EXISTS cathay_exam;
USE cathay_exam;
CREATE EXTERNAL TABLE renting_house ( source string, post_id string, poster_title string, poster_gender string, poster_identity string, tel string, house_type string, room_type string, gender_restriction string, house_description string, region string)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION '/data';
