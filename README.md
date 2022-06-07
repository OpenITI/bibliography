# bibliography

In fact, this is a little more than just a bibliography. This repository is to keep track of:

- bibliography of primary and secondary sources;
- identifiers of contributors;

# Structure

- `./bibFiles/` :: bib files for individual records, named using their bibTeX keys; automatically generated from large bibTeX files added to `./data/bibTeX_primary/` and `./data/bibTeX_secondary/`.
- `./data/` :: subfolders `./data/bibTeX_primary/` and `./data/bibTeX_secondary/` for uploading large bibTeX files;
- `./scripts/` :: contains `split_bib_files.py` script that parses large bibliographies into individual bib files and aggregates browsable `bibTex_pri.tsv` and `bibTex_sec.tsv` files;
- `bibTex_pri.tsv` can be used to find a reference to a primary source; generated automatically;
- `bibTex_sec.tsv` can be used to find a reference to a secondary source; generated automatically;
- `contributors.yml` file for keeping track of contributor URIs; can be edited directly on github;
- `references.yml` file to keep track of references; can be edited directly on github;
- `README.md` is this file;


## STAR-like Assertions

- the idea is from Tara Andrews: instead of traditional SPO model, we may benefit from using a "structured assertion record" (the proposed CDOC-CRM standard is too complex though for collecting data):
	- ASSERTION:
		- SUBJECT
		- PREDICATE
		- OBJECT (OObject, OGeo, and OTime)
		- AUTHORITY
		- PROVENANCE

![./scripts/STAR_examples.png](./scripts/STAR_examples.png)

## Adaptation to OpenITI YML files:

- ASSERTION: can be given in the `COMMENT` field of the YML file, especially if the coded assertion has some ambiguities.
	- SUBJECT: not coded, since the URI of the YML file is the SUBJECT; implied by the filename;
	- PREDICATE: free vocabulary to be normalized during metadata revisions; always in first position;
		- **format**: `englishWords[_arabicWords]?`
	- OBJECT (OObject, OGeo, and OTime); each following a specific REGEX pattern (below); separated with commas;
		- **format**:
			- OObject: `AuthorURI` from OpenITI (if not in OpenITI, must be suggested using the same pattern);
			- OGeo: `Althurayya_URI` (if not in Althurayya, must be suggested using the same pattern);
			- OTime:
				- `YYYY_MMM_DD`, unknown elements are coded with `X`; codes for Islamic months are defined;
				- `YYYY_MMM_DD::YYYY_MMM_DD` for periods; unknown elements are coded with `X`; codes for Islamic months are defined;
	- AUTHORITY: follows a pattern;
		- **format:** `AUTH_ContrURI`, where `ContrURI` is the unique identifier of contributors to the OpenITI project;
		- a YML file is required for storing these `ContrURI` with detailed descriptions as values;
	- PROVENANCE:
		- **format:** `PROV_REFCODE`, where `REFCODE` is a URI of reference;
		- types of references, all explained in the corresponding YML file;
			- `PRI_YYMMDDHHMMSS` :: reference to a primary source, details are to be found in `*.bib` files in `./data/bibTeX_primary/` (multiple files can be added to that folder; references can also be pasted into already existing files); can be given with volumes and pages, using PANDOC format; 
			- `SEC_YYMMDDHHMMSS` :: reference to a secondary source, details are to be found in `*.bib` files in `./data/bibTeX_secondary/` (multiple files can be added to that folder; references can also be pasted into already existing files); can be given with volumes and pages, using PANDOC format;
			- `MSC_YYMMDDHHMMSS` :: free reference, given directly in the YML file (URLs, free-running comments, etc.)
		- a YML file is required to collect and keep track of references:
			- `(PRI|SEC|MSC)_timestamp: detailed reference`, where anything can go into detailed reference;	
	
### Coding example

**Assertion**: "[al-Dhahabī] had a great many excellent pupils, among whom we particularly mention ʿAbd al-Wahhāb al-Subkī, the author of the _Ṭabaḳāt al-S̲h̲āfiʿiyya al-Kubrā_. [Dhahabi was his teacher from 699 till 715 AH]". (Source: EI2)

**STAR_Record** --- packed TRIPLE with implied SUBJECT:

`teacherOf_tafaqqahaCalayhi@0771Subki,DIMASHQ_363E335N_S,699_XXX_XX::715_XXX_XX@AUTH_MGR@MSC_220607114500,SEC_220607114501,PRIV_220607114502`

- SUBJECT is implied by the NAME of the YML file; 
- the PREDICATE is always in the first position;
- OBJECTS: follow specific patterns; omitted if not known;
- AUTH and MSC/PRI/SEC may be omitted;

#### YML CONTRIBUTORS:

I chose to go with initials, but it does not really matter --- feel free to add yours.

```yml
SBS: Sarah Bowen Savant
MGR: Maxim G. Romanov
```

#### YML REFERENCES



```yml
MSC_220607114500: <http://dx.doi.org/10.1163/1573-3912_islam_COM_0159>
SEC_220607114501: MacrufDahabi1976s, 45
PRI_220607114502: 0748DhahabiTarikhIslamMacruf2003

```

#### *.bib File for secondary sources

```
@book{MacrufDahabi1976s,
  title = {al-{{Ḏahabī}} wa-manhaju-hu fī kitābi-hi \textit{{{Taʾrīḫ}} al-{{Islām}}}},
  shorttitle = {al-{{Ḏahabī}} wa-manhaju-hu},
  author = {Maʿrūf, Baššār ʿAwwād},
  year = 1976,
  edition = {al-Ṭabʿaŧ al-ūlá},
  publisher = {{Maṭbaʿaŧ ʿĪsá al-Bābī al-Ḥalabī}},
  location = {{al-Qāhiraŧ}},
  langid = {arabic},
}

```

#### *.bib File for primary sources

```
@mvbook{0748DhahabiTarikhIslamMacruf2003,
  title = {Taʾrīḫ al-islām wa-wafayāt al-mašāhīr wa-al-aʿlām},
  shorttitle = {Taʾrīḫ al-islām (Maʿrūf)},
  author = {{Ḏahabī (al-)}},
  editor = {Maʿrūf, Baššār ʿAwwād},
  date = {2003},
  edition = {1},
  publisher = {{Dār al-Ġarb al-Islāmī}},
  location = {{Bayrūt}},
  langid = {arabic},
  volumes = {17},
}

```

#### bibTeX Key Format

- `AuthorTitleYEAR` for secondary sources;
- `XXXXAuthorTitleEditionYEAR` for primary sources, where `XXXXAuthorTitle` is the OpenITI URI `XXXXAuthor.Title`, but without a dot;
