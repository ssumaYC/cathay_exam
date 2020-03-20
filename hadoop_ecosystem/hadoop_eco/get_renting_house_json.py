import json
from pymongo import MongoClient


def main():
    mc = MongoClient("localhost:27017")
    col = mc['cathay_exam']['renting_houses']
    docs = col.find({}, {"_id": 0})
    docs_str = [json.dumps(d) for d in docs]
    text = "\n".join(docs_str)
    with open("data/renting_house.json", "wb") as f:
        f.write(text.encode("utf-8"))


if __name__ == "__main__":
    main()
