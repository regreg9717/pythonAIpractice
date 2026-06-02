import json
user={
    "name":"峰哥",
    "age":30,
    "gender":"male",
    "hobbies":["reading","talking"]
}
with open("user.json", "w", encoding="utf-8") as f:
    json.dump(user,f,ensure_ascii=False,indent=2)