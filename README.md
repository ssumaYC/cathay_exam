# cathay_exam

## flask_api
A RESTful API to get renting house data

### API schema
- GET /rentingHouses/<post_id>
```
{
    "source": "591",
    "post_id": "8939775",
    "poster_title": "胡先生",
    "poster_gender": "male",
    "poster_identity": "broker",
    "tel": "0963877969",
    "house_type": "公寓",
    "room_type": "獨立套房",
    "gender_acception": "both",
    "house_description": "以西門捷運站為中心，附近有家樂福.....",
    "region": "台北市"
}
```
- GET /rentingHouses
  - avaiable query strings

| field | available value | description |
| ------ | ----------- | ------ |
| gender-accept   | male-only, male, female-only, female | the gender restriction of the house
| region | 台北市, 新北市 | the region of the house
| phone    | Phone number in the format of ordinary Taiwanese phone numbers, ex:  0223145678, 0987654321, 0911234567#12345  | search house by phone number
|is-owner| 1, 0| is the renting infomation posted by the house owner|
|poster-gender|male, female|the gender of the poster
|poster-lname|陳, 吳, 黃...... |the last name of the poster|

  - example 【臺北】【屋主為女性】【姓氏為吳】所刊登的所有租屋物件
  - /rentingHouses?region=台北市&is-owner=1&poster-gender=female&poster-lname=吳
```
{
    "success": true,
    "num_data": 53,
    "data": [
        {
            "source": "591",
            "post_id": "8885500",
            "poster_title": "吳小姐",
            "poster_gender": "female",
            "poster_identity": "owner",
            "tel": "0936798759",
            "house_type": "公寓",
            "room_type": "雅房",
            "gender_acception": "both",
            "house_description": "暫未添加說明",
            "region": "台北市"
        },
        {
            "source": "591",
            "post_id": "8734366",
            "poster_title": "吳媽媽",
            "poster_gender": "female",
            "poster_identity": "owner",
            "tel": "0936506277",
            "house_type": "公寓",
            "room_type": "分租套房",
            "gender_acception": "both",
            "house_description": "生活機能方便，電話預約時間中午12點到7點...",
            "region": "台北市"
        },.....
}
```

## spider_home
A Scrapy project to crawl renting houses data

## hadoop_ecosystem
A environment with Hadoop, Hive, Spark and ELK Stack

- How to use
1. Downloads the tars list below into hadoop_eco/downloads/tars.  
    - Python-3.6.5.tgz
    - hadoop-2.8.5.tar.gz
    - scala-2.12.8.tgz
    - apache-hive-1.2.2-bin.tar.gz
    - jdk-8u241-linux-x64.tar.gz
    - spark-2.4.5-bin-hadoop2.7.tgz
2.  Downloads the jars list below into hadoop_eco/downloads/jars
    - json-serde-1.3.8-jar-with-dependencies.jar
    - json-udf-1.3.8-jar-with-dependencies.jar
    - mysql-connector-java-5.1.48.jar
3.  Get renting house data from Mongo in flask_api with /hadoop_ecosystem/hadoop_eco/get_renting_house_json.py
4.  docker-compose up in /hadoop_ecosystem 
