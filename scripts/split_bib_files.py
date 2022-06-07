
pathToData = "../data/"
pathToPri = "../data/bibTeX_primary/"
pathToSec = "../data/bibTeX_secondary/"

targetBibPath = "../bibFiles/"
targetBibLink = "https://github.com/OpenITI/bibliography/blob/main/bibFiles/"

import os, re, sys

primaryBibs = os.listdir(pathToPri)
secondaryBibs = os.listdir(pathToSec)

csvConnector = "\t"

def collectBibFiles(bibTexFolder):
    bibFileText = ""
    for f in os.listdir(bibTexFolder):
        if not f.startswith(".") and f.endswith(".bib"):
            with open(bibTexFolder + f, "r", encoding="utf8") as ft:
                bibFileText += ft.read()
    return(bibFileText)

def procesBib(bibTexFolder, var):
    bibDic = {}

    bibTexFile = collectBibFiles(bibTexFolder)

    records = re.sub("\n@preamble[^\n]+", "", bibTexFile)
    records = records.split("\n@")

    for record in records[1:]:
        completeRecord = "\n@" + record
        completeRecord = re.sub("\n\s+file = [^\n]+", "", completeRecord)

        record = record.strip().split("\n")[:-1]

        print(record)

        rType = record[0].split("{")[0].strip()
        rCiteRaw = record[0].split("{")[1].strip().replace(",", "")

        rCite = rCiteRaw.replace("-", "")

        # only valid characters in citeKey:
        if re.search("^[A-Za-z0-9]+$", rCite):
            bibDic[rCite] = {}
            bibDic[rCite]["rCite"] = rCite
            bibDic[rCite]["rType"] = rType
            bibDic[rCite]["complete"] = completeRecord

            for r in record[1:]:
                key = r.split("=")[0].strip()
                val = r.split("=")[1].strip()
                val = re.sub("^\{|\},?", "", val)

                bibDic[rCite][key] = val

                # fix the path to PDF
                if key == "file":
                    if ";" in val:
                        #print(val)
                        temp = val.split(";")

                        for t in temp:
                            if ".pdf" in t:
                                val = t

                        bibDic[rCite][key] = val
        else:
            print("rCiteRaw:", rCiteRaw)
            print(rCite)
            print(completeRecord)
            print("!!! RECORD SKIPPED !!!")
            #sys.exit("\n\tPROCESSING STOPPED: INVALID KEY")

    # filter bibDic: remove records that do not have informatin on authr/editor and date
    bibDicFiltered = {}

    for k,v in bibDic.items():
        if "author" in v or "editor" in v:
            if "date" in v:
                bibDicFiltered[k] = v
            else:
                print("== NO DATE FIELD IN THE RECORD ==")
                print(v["complete"])
                input(k)
        else:
            print(v["complete"])
            input(k)

    if len(bibDicFiltered) > 1:
        print("="*80)
        print("NUMBER OF RECORDS IN BIBLIOGRAPHY         : %d" % len(bibDic))
        print("NUMBER OF RECORDS IN FILTERED BIBLIOGRAPHY: %d" % len(bibDicFiltered))
        print("="*80)

    
    print("="*80)
    print("FINAL RUN")
    print("="*80)
    tsv = []

    for k,v in bibDicFiltered.items():
        aKEY = k
        if "author" in v:
            aREAD = v["author"] + " — " + v["title"]
        else:
            aREAD = "NO AUTHOR" + " — " + v["title"]
        aBIBFILE = targetBibLink + aKEY + ".bib"

        tsv.append("%s\t%s\t%s" % (aKEY, aREAD, aBIBFILE))

        with open(targetBibPath + aKEY + ".bib", "w", encoding="utf8") as f9:
            f9.write(v["complete"].strip())

    tsvFinal = "KEY\tAUTHOR+TITLE\tBIB FILE\n" + "\n".join(sorted(tsv)).replace("{", "").replace("}", "")
    with open("../bibTex_%s.tsv" % var, "w", encoding="utf8") as f9:
        f9.write(tsvFinal)

procesBib(pathToPri, "pri")
procesBib(pathToSec, "sec")


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
    with open("../bibTex_%s.tsv" % var, "w", encoding="utf8") as f9:
        f9.write(csv)


#splitBibs(pathToPri, "pri")
#splitBibs(pathToSec, "sec")

def convertYML(ymlFile):
    with open(pathToData + ymlFile, "r", encoding="utf8")as f1:
        data = '"' + f1.read().replace(":", '","').replace("\n", '"\n"') + '"'

        with open("../" + ymlFile.replace(".yml", ".csv"), "w", encoding="utf8") as f9:
            f9.write("KEY,VALUE\n" + data)

#convertYML("contributors.yml")
#convertYML("references.yml")