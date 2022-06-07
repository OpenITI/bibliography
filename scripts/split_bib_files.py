
pathToData = "../data/"
pathToPri = "../data/bibTeX_primary/"
pathToSec = "../data/bibTeX_secondary/"

targetBibPath = "../bibFiles/"
targetBibLink = "https://github.com/OpenITI/bibliography/blob/main/bibFiles/"

import os, re

primaryBibs = os.listdir(pathToPri)
secondaryBibs = os.listdir(pathToSec)

csvConnector = "\t"

def splitBibs(path, var):
    csv = []
    for f in os.listdir(path):
        if not f.startswith(".") and f.endswith(".bib"):
            with open(path + f, "r", encoding="utf8") as ft:
                data = ft.read().split("\n@")

                for d in data:
                    if d.strip() != "":
                        key = d.split("\n")[0].split("{")[1].replace(",", "")
                        if var == "pri":
                            if re.search("^\d\d\d\d\w+$", key):
                                print(key)

                                bib = ("@" + d).strip()

                                with open(targetBibPath + key + ".bib", "w", encoding="utf8") as f9:
                                    f9.write(bib)

                                csv.append("%s%s%s%s" % (key, csvConnector, targetBibLink, key+".bib"))
                        else:
                            if re.search("^\w+$", key):
                                print(key)

                                bib = ("@" + d).strip()

                                with open(targetBibPath + key + ".bib", "w", encoding="utf8") as f9:
                                    f9.write(bib)

                                csv.append("%s%s%s%s" % (key, csvConnector, targetBibLink, key+".bib"))

    csv = "bibTeX Key%sLink to bibTeX File\n" % csvConnector + "\n".join(sorted(csv))
    with open("../bibTex_%s.csv" % var, "w", encoding="utf8") as f9:
        f9.write(csv)


splitBibs(pathToPri, "pri")
splitBibs(pathToSec, "sec")

def convertYML(ymlFile):
    with open(pathToData + ymlFile, "r", encoding="utf8")as f1:
        data = '"' + f1.read().replace(":", '","').replace("\n", '"\n"') + '"'

        with open("../" + ymlFile.replace(".yml", ".csv"), "w", encoding="utf8") as f9:
            f9.write("KEY,VALUE\n" + data)

#convertYML("contributors.yml")
#convertYML("references.yml")