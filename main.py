import sqlite3, os, subprocess, shutil
from pydub import AudioSegment

user = os.getlogin()
path = "C:/Users/" + user + "/AppData/LocalLow/Cygames/umamusume/"
masterPath = path + "master/master.mdb"
meta = path + "meta"
master = sqlite3.connect(masterPath)
meta = sqlite3.connect(meta)
def masterSql():
    charaList = [] 
    soundNameList = []
    charaQ = master.execute('SELECT "index", text FROM text_data WHERE category = 170')
    soundNameQ = master.execute('SELECT "index", text FROM text_data WHERE category = 16')
    for i in charaQ:
        chara = list(i)
        charaList.append(chara)
    for i in soundNameQ:
        sound = list(i)
        soundNameList.append(sound)
    return charaList, soundNameList
def metaSql():
    soundList = []
    okeList = []
    twoStrOkeList = []
    twoStrSoundList = []
    soundSrcQ = meta.execute("SELECT  n ,h FROM a where n like 'sound/l/%chara%awb'")
    okeSrcQ = meta.execute("SELECT  n ,h FROM a where n like 'sound/l/%oke_01.awb'")
    for i in soundSrcQ:
        soundSrc = list(i)
        twoStrSound = soundSrc[1][0:2]
        soundSrc[1] = path + "dat/" + twoStrSound + "/" + soundSrc[1]
        soundList.append(soundSrc)
        twoStrSoundList.append(twoStrSound)
    for i in okeSrcQ:
        okeSrc = list(i)
        twoStrOke = okeSrc[1][0:2]
        okeSrc[1] = path + "dat/" + twoStrOke + "/" + okeSrc[1]
        okeList.append(okeSrc)
        twoStrOkeList.append(twoStrOke)
    return soundList, okeList, twoStrOkeList, twoStrSoundList

okeCopyPathList = []
soundCopyPathList = []
os.mkdir("./temp/")
print("Copying files...")
for i in range(len(metaSql()[0])):
    try:
        os.mkdir("./temp/" + metaSql()[3][i])
    except FileExistsError:
        pass
    songCopyPath = "./temp/" + metaSql()[0][i][1].replace(path, "").replace("dat/", "") + ".awb"
    soundCopyPathList.append(songCopyPath)
    shutil.copyfile(metaSql()[0][i][1], songCopyPath)

for i in range(len(metaSql()[1])):
    try:
        os.mkdir("./temp/" + metaSql()[2][i])
    except FileExistsError:
        pass
    okeCopyPath = "./temp/" + metaSql()[1][i][1].replace(path, "").replace("dat/", "") + ".awb"
    okeCopyPathList.append(okeCopyPath)
    shutil.copyfile(metaSql()[1][i][1], okeCopyPath)
print("Converting Oke...")
okeNameList = []
okeSaveName = []
#oke
os.mkdir("./temp/oke")
for i in range(len(metaSql()[1])):
    okeName = metaSql()[1][i][0].split("/")[-1].replace("snd_bgm_live_","").replace("_oke_01.awb","")
    okeNameList.append(okeName)
for i in range(len(masterSql()[1])):
    for j in range(len(metaSql()[1])):
        if masterSql()[1][i][0] == int(okeNameList[j]):
            okeSaveName.append(["./temp/oke/" + masterSql()[1][i][1] + ".wav", okeCopyPathList[j]])
for i in range(len(okeSaveName)):
    subprocess.run(("vgmstream", "-o", okeSaveName[i][0], okeSaveName[i][1]), shell=True)
print("Converting Chara voices...")
#キャラボイス
charaSongList = []
firstList = []
secondList = []
for i in range(len(masterSql()[1])):
    os.makedirs("./temp/songs/" + masterSql()[1][i][1])
    os.makedirs("./songs/" + masterSql()[1][i][1])
for i in range(len(metaSql()[0])):
    charaSong = metaSql()[0][i][0].split("/")[-1].replace("snd_bgm_live_","").replace("_chara_",":").replace("_01.awb","")
    charaSongList.append(charaSong)
for i in range(len(charaSongList)):
    for j in range(len(masterSql()[1])):
        if int(charaSongList[i].split(":")[0]) == masterSql()[1][j][0]:
            thefirst = masterSql()[1][j][1]
            firstList.append(thefirst)
    for j in range(len(masterSql()[0])):
        if int(charaSongList[i].split(":")[1]) == masterSql()[0][j][0]:
            thesecond = masterSql()[0][j][1]
            secondList.append(thesecond)
num = len(charaSongList)
charaSongList.clear()
for i in range(num):
    os.mkdir("./temp/songs/" + firstList[i] + "/" + secondList[i])
    charaSongList.append(["./temp/songs/" + firstList[i] + "/" + secondList[i]+ "/" + secondList[i], soundCopyPathList[i]])
    saveSongPath = "./songs/" + firstList[i] + "/" + firstList[i] + "_" + secondList[i] + ".mp3"
    okePath = "./temp/oke/" + firstList[i] + ".wav"
    subprocess.run(("vgmstream", "-o", charaSongList[i][0] + "-1.wav", "-s", "1", charaSongList[i][1]), shell=True)
    subprocess.run(("vgmstream", "-o", charaSongList[i][0] + "-2.wav","-s", "2", charaSongList[i][1]), shell=True)
    dir = os.listdir("./temp/songs/" + firstList[i] + "/" + secondList[i])
    if len(dir) > 1:
        sound1 = AudioSegment.from_file(charaSongList[i][0] + "-1.wav")
        sound2 = AudioSegment.from_file(charaSongList[i][0] + "-2.wav")
        sound1.overlay(sound2).export(charaSongList[i][0] + "-3.wav", format="wav")
        sound3 = AudioSegment.from_file(charaSongList[i][0] + "-3.wav")
        oke = AudioSegment.from_file(okePath)
        oke.overlay(sound3).export(saveSongPath, format="mp3", bitrate="128k")
    else:
        sound1 = AudioSegment.from_file(charaSongList[i][0] + "-1.wav")
        oke = AudioSegment.from_file(okePath)
        oke.overlay(sound1).export(saveSongPath, format="mp3", bitrate="128k")
shutil.rmtree("./temp")
for i in range(len(masterSql()[1])):
    path = "./songs/" + masterSql()[1][i][1]
    dir = os.listdir(path)
    if len(dir) == 0:
        os.rmdir(path)
meta.close()
master.close()
print("Converted successfully!")