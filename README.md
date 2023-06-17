# DBLP SAX Parser

<p align="center">
    <a href="https://www.python.org/downloads/release/python-3113/" alt="python">
      <img src="https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue"/></a>
    <a href="https://pypi.org/project/dblp-sax-parser/" alt="pypi version">
      <img src="https://img.shields.io/badge/Pypi-v1.0.0-blue"/></a>
    <a href="https://pypi.org/project/dblp-sax-parser/" alt="status">
      <img src="https://img.shields.io/badge/status-experimental-yellow"/></a>
</p>

- [DBLP SAX Parser](#dblp-sax-parser)
    - [What is it?](#what-is-it)
    - [Context and Purpose](#context-and-purpose)
    - [Usage](#usage)
    - [DBLP Methods](#dblp-methods)
    - [License](#license)
    - [References](#references)

### What is it?
A parsing package using the [Simple API for XML (SAX)](https://docs.python.org/3/library/xml.sax.html).

There are a total of 10 elements: "article", "inproceedings", "proceedings", "book", "incollection", "phdthesis", "mastersthesis", "www", "person", "data".

Across the elements, these are the feature types available: "address", "author", "booktitle","cdrom", "chapter", "cite", "crossref", "editor", "ee", "isbn", "journal", "month", "note", "number", "pages", "publisher", "publnr", "school", "series", "title", "url", "volume", "year".

**Features**
- download dblp files from the dblp website directly
- parse throught the dblp xml file into a dataframe, exported with either csv or pickle format. 

**Future features for consideration**
- add more methods to parse data from a specific attribute. E.g. only for years in 2016
- select which elements or features to be included/excluded 

### Context and Purpose
I created this package when working on a project as part of a course module. The aim of this package is to provide a quick way to parse DBLP elements directly, with the contents exported as a csv file for further preprocessing based on individual's use case.

Installation
```
pip install dblp-sax-parser

# import package
from dblp_parser import DBLP_Parser as dp
```

### Usage

First step to using this parser is to instantiate the dblp_parser
```
# Instantiate the dblp class 
dblp = dp()
```

You can also DBLP_Parser to download the dblp data assets from the dblp website
```
# download latest data sets from dblp website
dblp.download_latest_dump()
```

Parsing the xml file
```
filename = 'dblp.xml'

# execute the parser from the dblp class
parser, handler = dblp.execute_parser(filename=<filename>)

# you can use the handler to convert the handler output to dataframe
handler.to_df()

# the dataframe can be persisted as a pickle file or exported as csv file
handler.to_csv() # export to csv
handler.save() # persist as pickle
```

### DBLP Methods

*class* DBLP_Parser  
- This is the main class to be instantiated when before using the parser

*class* DBLP_Parser.**download_latest_dump**    
- Begins downloading the latest dblp files from the [dblp website](https://dblp.uni-trier.de/xml). If the url location where files are hosted is changed/incorrect, a separate url can be used instead.
- This downloads the dblp `.dtd` and `.xml.gz` files, and decompress the `.gz` file into `.xml`.
- dtd_url[str]: url location of the `.dtd` file to be downloaded from.  
- xml_zip_url [str]: url of the `.xml.tz` file to be downloaded from.  
- xml_zip_filename [str]: specify filename of the downloaded `.xml.gz` file. 
- xml_filename [str]: specify filename of the `.xml` file that is decompressed.
  
*class* DBLP_Parser.**execute_parser**  

- This executes the underlying SAX parser, calling the xml.sax.handler.ContentHandler
- filename [str]:  path and name of XML file to be parsed. If **download_latest_dump() was used, the file to be parsed will be `"dblp.xml"`.


### License

This code is published under the MIT licence. 

### References

There are two main references that helped contributed to writing this package. Instantiating the outer dblp class to download dblp materials directly came from from [angelosalatino](https://github.com/angelosalatino/dblp-parser). Some component of the SAX parsing logic itself was borrowed from [hibernator11](https://github.com/hibernator11/notebook-emerging-topics-corpora/blob/master/dblp/dblp-xml2csv-process.py).

