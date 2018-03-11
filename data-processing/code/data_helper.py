
# with open("keys.txt", "r") as file, open("f.csv" ,"w") as out:
#     for line in file:
#         line = line.strip()
#         a, b = line.split(": ")
#         out.write(b + "," + a + "\n")
l = []
with open("f.csv" ,"r") as out:
    for line in out:
        line = line.strip()
        a, b = line.split(",")
        l.append(b)
    print(l)