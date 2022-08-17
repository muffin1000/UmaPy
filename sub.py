import shutil, os,SQL, convert, copy, os

os.mkdir("./temp/")
print("Copying files...")
copy.copy(0, 2)
copy.copy(1, 3)
print("Prepare for converting Sound...")
for i in SQL.masterSQL()[1]:
    os.makedirs("./temp/SONGS/" + i[1])
    os.makedirs("./SONGS/" + i[1])
convert.sound()
print("converting oke...")
os.mkdir("./temp/OKE")
convert.oke()
print("mixing oke and sound...")
convert.mix()
shutil.rmtree("./temp/")
for i in range(len(SQL.masterSQL()[1])):
    path = "./songs/" + SQL.masterSQL()[1][i][1]
    dir = os.listdir(path)
    if len(dir) == 0:
        os.rmdir(path)