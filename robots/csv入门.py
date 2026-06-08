# with open("csv_data/01.csv","w",encoding="utf-8") as f:
#     f.write("姓名,年龄,性别,爱好\n")
#     f.write("敖诚,18,男,python\n")
# print("运行结束")

# with open("csv_data/01.csv","r",encoding="utf-8") as f:
#     for i in f:
#         print(i.strip())

import csv
with open("csv_data/02.csv","w",encoding="utf-8",newline="") as f:
    writer=csv.DictWriter(f,fieldnames=["姓名","年龄","性别","爱好"])
    writer.writeheader()
    writer.writerow({"姓名":"敖诚","年龄":18,"性别":"男","爱好":"python,原神"})
    writer.writerow({"姓名":"张三","年龄":18,"性别":"男","爱好":"python"})
    writer.writerow({"姓名":"王五","年龄":18,"性别":"男","爱好":"python"})
    writer.writerow({"姓名":"赵六","年龄":18,"性别":"男","爱好":"python"})

with open("csv_data/02.csv","r",encoding="utf-8") as f:
    reader=csv.DictReader(f)
    for i in reader:
        print(i)