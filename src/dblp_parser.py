import xml.sax
import re
import requests
import sys
import shutil
import gzip
from hurry.filesize import size
import pandas as pd

class DBLP_Parser:
    def __init__(self):
        self.handler = self.DBLP_Handler()

    def __download_dtd(self, url:str=None, filename:str=None)->None:
        """
        Borrowed from: https://github.com/angelosalatino/dblp-parser
        Function that downloads the DTD from the DBLP website.

        Args:
            url [str] : The URL of where to download it from. If None then default is
            filename [str]: location of where to save the dtd file
        Returns:
            None
        """

        if url is None:
            url = "https://dblp.uni-trier.de/xml/dblp.dtd"

        if filename is None:
            filename = "dblp.dtd"

        self.__download_file(url, filename)
        
        print(f"DTD downloaded from {url}.")

    def __download_file(self, url:str, filename:str) -> bool:
        """
        Borrowed from: https://github.com/angelosalatino/dblp-parser
        Function that downloads files (general).
        
        Args:
            url [string]: Url of where the model is located.
            filename [string]: location of where to save the model
        Returns:
            is_downloaded [boolean]: whether it is successful or not.
        """

        is_downloaded = False
        with open(filename, 'wb') as file:
            response = requests.get(url, stream=True)
            total = response.headers.get('content-length')

            if total is None:
                #f.write(response.content)
                print('There was an error while downloading the DTD.')
            else:
                downloaded = 0
                total = int(total)
                for data in response.iter_content(chunk_size=max(total // 1000, 1024*1024)):
                    downloaded += len(data)
                    file.write(data)
                    done = int(50*downloaded/total)
                    sys.stdout.write(
                        f"\r[{'█' * done}{'.' * (50 - done)}] {size(downloaded)}/{size(total)}"
                    )
                    sys.stdout.flush()
                sys.stdout.write('\n')
                is_downloaded = True

        return is_downloaded
    
    def __download_and_prepare_dataset(self, url:str=None, filename_zip:str=None, filename_unzip:str=None)->None:
        """
        Borrowed from: https://github.com/angelosalatino/dblp-parser
        Function that downloads the whole dataset (latest dump) from the DBLP website.
        Then it decompresses it

        Args:
            url [string]: URL of dblp database. If none provided will use default one.
            filename_zip [string]: name and path of zip archive containing all papers.
            filename_unzip [string]: name and path of folder into which we want unzip everything.

        Returns:
            None
        """

        if url is None:
            url = "https://dblp.uni-trier.de/xml/dblp.xml.gz"

        if filename_zip is None:
            filename_zip = "dblp.xml.gz"
        
        self.__download_file(url, filename_zip)
        
        print(f"Latest dump of DBLP downloaded from {url}.")
        
        if filename_unzip is None:
            filename_unzip = "dblp.xml"
        
        with gzip.open(filename_zip, 'rb') as f_in:
            with open(filename_unzip, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
                
        print("File unzipped and ready to be parsed.")
    
    def download_latest_dump(self, dtd_url:str=None, xml_zip_url:str=None, xml_zip_filename:str=None, xml_filename:str=None)->None:
        """
        Borrowed from: https://github.com/angelosalatino/dblp-parser
        Downloads the latest dump of the DBLP dataset

        Args:
            dtd_url [str]: url string of dblp dtd file to download from
            xml_zip_url [str]: url string of xml gzip file to download from
            xml_zip_filename [str]: name for zip file after downloading
            xml_filename [str]: name for unzip file after downloading

        Returns:
            None

        """
        self.__download_dtd(url=dtd_url)
        self.__download_and_prepare_dataset(
                url=xml_zip_url,
                filename_zip=xml_zip_filename,
                filename_unzip=xml_filename)
        
        print("Dataset prepared. You can now parse it.")

    def execute_parser(self, filename:str):
        """
        Function to execute the SAX parser

        Args:
            filename : str - path of XML file to be parsed

        Returns:
            parser: SAX XMLReader object
            handler: SAX API Content Handler
        """
        parser = xml.sax.make_parser()
        # override default ContextHandler
        parser.setContentHandler(self.handler)
        # creates a SAX parser to parse the given xml file
        parser.parse(filename)

        return parser, self.handler
    
    class DBLP_Handler(xml.sax.ContentHandler):
        def __init__(self):
            """
            Args:
                None

            Returns:
                None
            """
            # initialise path, text and article to store element contents, paths (containing tags parsed) and article (to store contents passed for the element)
            self.path = [] # store path of tags parsed for each element
            self.content = {}
            self.text = [] # store feature contents for the element 
            self.article = {} # store element and the contents for each article
            self.articles = [] # initialise empty list to hold processing articles
            # initialise for attribute keys
            self.mdate = {}
            self.publtype = {}
            self.key = {}
            
            # set counter to count elements parsed
            self.counter = 0 

            # Element types in DBLP
            self.all_elements = {"article",
                                "inproceedings",
                                "proceedings",
                                "book",
                                "incollection",
                                "phdthesis",
                                "mastersthesis",
                                "www",
                                "person",
                                "data"}
            
            # Feature types in DBLP
            self.all_features = {"address"  :"str",
                                "author"   :"list",
                                "booktitle":"str",
                                "cdrom"    :"str",
                                "chapter"  :"str",
                                "cite"     :"list",
                                "crossref" :"str",
                                "editor"   :"list",
                                "ee"       :"list",
                                "isbn"     :"str",
                                "journal"  :"str",
                                "month"    :"str",
                                "note"     :"str",
                                "number"   :"str",
                                "pages"    :"str",
                                "publisher":"str",
                                "publnr"   :"str",
                                "school"   :"str",
                                "series"   :"str",
                                "title"    :"str",
                                "url"      :"str",
                                "volume"   :"str",
                                "year"     :"str"}
        def __count_pages(self, pages:str)->str:
            """
            Borrowed from: https://github.com/billjh/dblp-iter-parser/blob/master/iter_parser.py
            Parse pages string and count number of pages. There might be multiple pages separated by commas.
            VALID FORMATS:
                51         -> Single number
                23-43      -> Range by two numbers
            NON-DIGITS ARE ALLOWED BUT IGNORED:
                AG83-AG120
                90210H     -> Containing alphabets
                8e:1-8e:4
                11:12-21   -> Containing colons
                P1.35      -> Containing dots
                S2/109     -> Containing slashes
                2-3&4      -> Containing ampersands and more...
            INVALID FORMATS:
                I-XXI      -> Roman numerals are not recognized
                0-         -> Incomplete range
                91A-91A-3  -> More than one dash
                f          -> No digits
            ALGORITHM:
                1) Split the string by comma evaluated each part with (2).
                2) Split the part to subparts by dash. If more than two subparts, evaluate to zero. If have two subparts,
                evaluate by (3). If have one subpart, evaluate by (4).
                3) For both subparts, convert to number by (4). If not successful in either subpart, return zero. Subtract first
                to second, if negative, return zero; else return (second - first + 1) as page count.
                4) Search for number consist of digits. Only take the last one (P17.23 -> 23). Return page count as 1 for (2)
                if find; 0 for (2) if not find. Return the number for (3) if find; -1 for (3) if not find.

            Parameters
            ----------
            pages : str
                The string describing the page numbers.

            Returns
            -------
            str
                The page count

            """
            cnt = 0
            try:
                for part in re.compile(r",").split(pages):
                    subparts = re.compile(r"-").split(part)
                    if len(subparts) > 2:
                        continue
                    else:
                        try:
                            re_digits = re.compile(r"[\d]+")
                            subparts = [int(re_digits.findall(sub)[-1]) for sub in subparts]
                        except IndexError:
                            continue
                        cnt += 1 if len(subparts) == 1 else subparts[1] - subparts[0] + 1
                return "" if cnt == 0 else str(cnt)
            except TypeError:
                return ""   
            
        def startElement(self, tag, attributes):
            """
            SAX handler method called when the parser encounters a start element.
            """
            if tag != 'dblp':
                self.path.append(tag)
                self.counter += 1
            
            # Check if the tag is present in the target elements
            if tag in self.all_elements:
                # Store the attributes in the article dictionary
                self.article['mdate'] = attributes.get('mdate')
                self.article['publtype'] = attributes.get('publtype')
                self.article['key'] = attributes.get('key')

            # Print progress for every 100,000 elements
            if self.counter % 1e5 == 0:
                print(f'Processed {self.counter} elements')
                
        def characters(self, content):
            """
            SAX handler method called when the parser encounters character data inside an element.
            """
            if content != '\n':
                self.text.append(content)

        def endElement(self, tag):
            """
            SAX handler method called when the parser encounters an end element.
            """
            try:
                if (tag in self.all_elements) & (tag == self.path[0]):
                    self.article['type'] = tag
                    self.path.pop(0) # remove first element from path

                    # Create a list of tuples containing the path and text content
                    record_lst = (list(zip(self.path,self.text)))

                    for feature, value in record_lst:
                    # Process the element and its contents if the tag is present in the feature list
                        if feature in self.all_features.keys():
                            # Retrieve feature type for the tag
                            feat_type = self.all_features.get(feature)
                            # Add element and its contents to the article dictionary
                            if feat_type == "str":
                                # apply __count_pages() method to count number of pages
                                if feature == "pages":
                                    value = self.__count_pages(value)

                                self.article[feature] = value
                            elif feat_type == "list":
                                
                                # update feature, value in article 
                                if feature in self.article:
                                    self.article[feature].append(value)
                                else:
                                    self.article[feature] = [value]
                    
                    # Append article contents to articles list
                    self.articles.append(self.article)
                    # Reset article dictionary
                    self.path = []
                    self.text = []
                    self.article = {}

            # Exception for ending element of </dblp>
            except Exception:
                print("Parsed closing element </dblp>. Completed parsing of elements in xml file. ")   

        def to_df(self):
            """
            Function to transform records of articles (dictionaries) to a dataframe
            """
            print("Creating dataframe from records")
            self.df = pd.DataFrame.from_records(self.articles)
            print("Successfully created dataframe")

        def to_csv(self, filename:str='dblp_output'):
            """
            Function to export dataframe as csv

            Args:
                filename [str]: Location and name of csv file to be exported

            Args:
                None
            """
            print("Writing dataframe to csv")
            self.df.to_csv(f'{filename}.csv')
            print(f"Successfully wrote to csv - {filename}.csv")
            
        def save(self, filename:str='dblp_output'):
            """
            Function to persist dataframe in pickle format

            Args:
                filename [str]: Location and name of pickle file to be persisted

            Returns:
                None
            """

            print("Persisting dataframe as pickle")
            self.df.to_pickle(f'{filename}.pkl')
            print(f"Dataframe has beem persisted as a pickle file - {filename}.pkl")


if __name__ == "__main__":
    DBLP_Parser()
    

        