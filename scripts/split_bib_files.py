
pathToData = "../data/"
pathToPri = "../data/bibTeX_primary/"
pathToSec = "../data/bibTeX_secondary/"

targetBibPath = "../bibFiles/"
targetBibLink = "https://github.com/OpenITI/bibliography/blob/main/bibFiles/"

import os, re, sys, unicodedata

primaryBibs = os.listdir(pathToPri)
secondaryBibs = os.listdir(pathToSec)

csvConnector = "\t"

translitSimple = {
"ā": "a",
"ṯ": "th",
"ǧ": "j",
"ḥ": "h",
"ḫ": "kh",
"ḏ": "dh",
"š": "sh",
"ṣ": "s",
"ḍ": "d",
"ṭ": "t",
"ẓ": "z",
"ʿ": "",
"ġ": "gh",
"ḳ": "q",
"ū": "u",
"ī": "i",
"Ā": "A",
"Ṯ": "Th",
"Ǧ": "J",
"Ḥ": "H",
"Ḫ": "Kh",
"Ḏ": "Dh",
"Š": "Sh",
"Ṣ": "S",
"Ḍ": "D",
"Ṭ": "T",
"Ẓ": "Z",
"Ġ": "Gh",
"Ḳ": "Q",
"Ū": "U",
"Ī": "I",
}


def simplifyTranslit(text):
    for k,v in translitSimple.items():
        text = text.replace(k, v)
    return(text)


def collectBibFiles(bibTexFolder):
    bibFileText = ""
    for f in os.listdir(bibTexFolder):
        if not f.startswith(".") and f.endswith(".bib"):
            with open(bibTexFolder + f, "r", encoding="utf8") as ft:
                bibFileText = bibFileText + "\n\n" + ft.read()
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
            if len(v["author"]) >= 20:
                author = v["author"][:20] + "..."
            else:
                author = v["author"]
        else:
            author = "NO AUTHOR"
    
        if len(v["title"]) >= 20:
            title = v["title"][:20] + "..."
        else:
            title = v["title"][:20]

        aREAD = author + " --- " + title
        #aREAD = unicodedata.normalize('NFKD', aREAD).encode('ascii', 'ignore').decode('utf8')
        aREAD = simplifyTranslit(aREAD)
        aBIBFILE = targetBibLink + aKEY + ".bib"

        tsv.append("%s\t%s\t%s" % (aKEY, aREAD, aBIBFILE))

        with open(targetBibPath + aKEY + ".bib", "w", encoding="utf8") as f9:
            f9.write(v["complete"].strip())

    tsvFinal = "KEY\tAUTHOR+TITLE\tBIB FILE\n" + "\n".join(sorted(tsv)).replace("{", "").replace("}", "").replace('"', "")
    with open("../bibTex_%s.tsv" % var, "w", encoding="utf8") as f9:
        f9.write(tsvFinal)

procesBib(pathToPri, "pri")
procesBib(pathToSec, "sec")

