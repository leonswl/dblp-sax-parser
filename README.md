# DBLP SAX Parser

<p align="center">
    <a href="https://www.python.org/downloads/release/python-3113/" alt="Contributors">
      <img src="https://img.shields.io/badge/python-3.10.7-blue**"/></a>
    <a href="https://layonsan-hdb-resale.streamlit.app/" alt="Streamlit App">
      <img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg"/></a>
</p>

- [DBLP SAX Parser](#dblp-sax-parser)
    - [What is it?](#what-is-it)
    - [Context and Purpose](#context-and-purpose)
    - [Usage](#usage)
    - [License](#license)
    - [References](#references)

### What is it?
A parsing package using the [Simple API for XML (SAX)](https://docs.python.org/3/library/xml.sax.html).

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

### License

This code is published under the MIT licence. 

### References

There are two main references that helped contributed to writing this package. Instantiating the outer dblp class to download dblp materials directly came from from [angelosalatino](https://github.com/angelosalatino/dblp-parser). Some component of the SAX parsing logic itself was borrowed from [hibernator11](https://github.com/hibernator11/notebook-emerging-topics-corpora/blob/master/dblp/dblp-xml2csv-process.py).

