# bibliography

- Bibliography of the OpenITI Project (primary and secondary sources)
- URIs of contributors for AUTHORITY statements
- URIs of references for PROVENANCE statements


## STAR-like Assertions

- the idea is from Tara Andrews: instead of traditional SPO model, we may benefit from using a "structured assertion record" (the proposed CDOC-CRM standard is too complex though for collecting data):
	- ASSERTION:
		- SUBJECT
		- PREDICATE
		- OBJECT (OObject, OGeo, and OTime)
		- AUTHORITY
		- PROVENANCE

(./scripts/STAR_examples.png)[./scripts/STAR_examples.png]

## Adaptation to OpenITI YML files:

- ASSERTION: can be given in the `COMMENT` field, especially if it has some ambiguities.
	- SUBJECT: not coded, since the URI of the YML file is the SUBJECT
	- PREDICATE: free vocabulary to be normalized during metadata revisions; always in first position
		- **format**: `englishWords[_arabicWords]?`
	- OBJECT (OObject, OGeo, and OTime); each following a specific REGEX pattern (below); separated with commas
		- **format**:
			- OObject: `AuthorURI` from OpenITI (if not in OpenITI, must be suggested using the same pattern);
			- OGeo: `Althurayya_URI` (if not in Althurayya, must be suggested using the same pattern);
			- OTime:
				- `YYYY_MMM_DD`, unknown elements are coded with `X`; codes for Islamic months are defined;
				- `YYYY_MMM_DD::YYYY_MMM_DD` for periods; unknown elements are coded with `X`; codes for Islamic months are defined;
	- AUTHORITY: follows a pattern;
		- **format:** `AUTH_ContrURI`, where `ContrURI` is the unique identifier of contributors to the OpenITI project;
		- a YML file is required for storing these `INITIALS` with detailed descriptions as values;
	- PROVENANCE:
		- **format:** `PROV_REFCODE`, where `REFCODE` is a URI of reference;
		- types of references, all explained in YML file
			- `PRI_YYMMDDHHMMSS` :: reference to a primary source, details are to be found in `bibTeX_PRI.bib`; can be given with volumes and pages, using PANDOC format
			- `SEC_YYMMDDHHMMSS` :: reference to a secondary source, details are to be found in `bibTeX_SEC.bib`; can be given with volumes and pages, using PANDOC format
			- `MSC_YYMMDDHHMMSS` :: free reference, given directly in the YML file (URLs, free-running comments, etc.)
		- a YML file is required to collect and keep track of references:
			- `timestamp: detailed reference`, where anything can go into detailed reference;

**NB:** where do we keep these additional YML files? We can probably keep them in separate repositories and automatically format them into some kinds of HTML bibliographies that are easy to navigate online:
	- github.com/openiti/bibliography
	- github.com/openiti/contributors
	
	
### Coding example

**Assertion**: "He had a great many excellent pupils, among whom we particularly mention ʿAbd al-Wahhāb al-Subkī, the author of the _Ṭabaḳāt al-S̲h̲āfiʿiyya al-Kubrā_ , whose father Taḳī al-Dīn al-Subkī, the famous S̲h̲āfiʿī doctor of law, was his most intimate friend. [Dhahabi was his teacher from 699 till 715 AH]". (Source: EI2)

**STAR_Record** --- packed TRIPLE with implied SUBJECT:

`teacherOf_tafaqqahaCalayhi@0771Subki,DIMASHQ_363E335N_S,699_XXX_XX::715_XXX_XX@AUTH_MGR@MSC_220607114500,SEC_220607114501,PRIV_220607114502`

- SUBJECT is implied by the NAME of the YML file; 
- the PREDICATE is always in the first position;
- OBJECTS: follow specific patterns; omitted if not known;
- AUTH and MSC/PRI/SEC may be omitted;

#### YML CONTRIBUTORS:

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

#### bibTeX_SEC.bib File

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

#### bibTeX_PRI.bib File

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

- `AuthorTitleYEAR` for secondary;
- `XXXXAuthorTitleEditionYEAR` for primary, where `XXXXAuthorTitle` is the OpenITI URI `XXXXAuthor.Title`, but without a dot;
