import SQL, vals, subprocess, os, shutil
from pydub import AudioSegment
def sound():
    for i in range(len(SQL.metaSQL()[0])):
        soundNum = SQL.metaSQL()[0][i][0].split("/")[-1].replace("snd_bgm_live_","").replace("_chara_",":").replace("_01.awb","")
        vals.soundNumList.append(soundNum)
    for i in range(len(vals.soundNumList)):
        for j in range(len(SQL.masterSQL()[1])):
            if int(vals.soundNumList[i].split(":")[0]) == SQL.masterSQL()[1][j][0]:
                vals.theFirstList.append(SQL.masterSQL()[1][j][1])
        for j in range(len(SQL.masterSQL()[0])):
            if int(vals.soundNumList[i].split(":")[1]) == SQL.masterSQL()[0][j][0]:
                vals.theSecondList.append(SQL.masterSQL()[0][j][1])

def oke():
    for src in SQL.metaSQL()[1]:
        okeNum = src[0].split("/")[-1].replace("snd_bgm_live_","").replace("_oke_01.awb","")
        vals.okeNumList.append(okeNum)
    for i in range(len(SQL.masterSQL()[1])):
        for j in range(len(SQL.metaSQL()[1])):
            if SQL.masterSQL()[1][0] == int(vals.okeNumList[j]):
                vals.okeSaveList.append(["./temp/OKE/" + SQL.masterSQL()[1][1] + ".wav", vals.okeCopyPathList[j]])
    for i in range(len(vals.okeSaveList)):
        subprocess.run(("vgmstream", "-o", vals.okeSaveList[i][0], vals.okeSaveList[i][1]), shell=True)

num = len(vals.soundNumList)
vals.soundNumList.clear()
def mix():
    for i in range(num):
        os.mkdir("./temp/songs/" + vals.theFirstList[i] + "/" + vals.theSecondList[i])
        vals.soundNumList.append(["./temp/SONGS/" + vals.theFirstList[i] + "/" + vals.theSecondList[i]+ "/" + vals.theSecondList[i], vals.soundCopyPathList[i]])
        saveSongPath = "./songs/" + vals.theFirstList[i] + "/" + vals.theFirstList[i] + "_" + vals.theSecondList[i] + ".mp3"
        okePath = "./temp/OKE/" + vals.theFirstList[i] + ".wav"
        subprocess.run(("vgmstream", "-o", vals.soundNumList[i][0] + "-1.wav", "-s", "1", vals.soundNumList[i][1]), shell=True)
        subprocess.run(("vgmstream", "-o", vals.soundNumList[i][0] + "-2.wav","-s", "2", vals.soundNumList[i][1]), shell=True)
        dir = os.listdir("./temp/songs/" + vals.theFirstList[i] + "/" + vals.theSecondList[i])
        if len(dir) > 1:
            sound1 = AudioSegment.from_file(vals.soundNumList[i][0] + "-1.wav")
            sound2 = AudioSegment.from_file(vals.soundNumList[i][0] + "-2.wav")
            sound1.overlay(sound2).export(vals.soundNumList[i][0] + "-3.wav", format="wav")
            sound3 = AudioSegment.from_file(vals.soundNumList[i][0] + "-3.wav")
            oke = AudioSegment.from_file(okePath)
            oke.overlay(sound3).export(saveSongPath, format="mp3", bitrate="128k")
        else:
            sound1 = AudioSegment.from_file(vals.soundNumList[i][0] + "-1.wav")
            oke = AudioSegment.from_file(okePath)
            oke.overlay(sound1).export(saveSongPath, format="mp3", bitrate="128k")
