import os, shutil, SQL, vals


def copy(twoStrNum, srcNum):
    num = len(SQL.metaSQL()[twoStrNum])
    for i in range(num):
        try:
            os.mkdir("./temp/" + SQL.metaSQL()[twoStrNum][i])
        except:
            pass
        copyPath = "./temp/" + SQL.metaSQL()[twoStrNum][i] + "/" + SQL.metaSQL()[srcNum][1].replace(vals.path, "").replace("dat/", "") + ".awb"
        if "oke" in SQL.metaSQL()[srcNum][0]:
            vals.okeCopyPathList.append(copyPath)
        else:
            vals.soundCopyPathList.append(copyPath)
        shutil.copyfile(SQL.metaSQL()[srcNum][1], copyPath)
