import xml.sax
import pandas as pd

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
                            self.article[feature] = value
                        elif feat_type == "list":
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
        print("Creating dataframe from records")
        self.df = pd.DataFrame.from_records(self.articles)
        print("Successfully created dataframe")

    def to_csv(self, filename:str='dblp_output'):
       print("Writing dataframe to csv")
       self.df.to_csv(f'{filename}.csv')
       print(f"Successfully wrote to csv - {filename}.csv")
           
    def save(self, filename:str='dblp_output'):
        print("Persisting dataframe as pickle")
        self.df.to_pickle(f'{filename}.pkl')
        print(f"Dataframe has beem persisted as a pickle file - {filename}.pkl")

if __name__ == "__main__":
    # creates a parser object
    parser = xml.sax.make_parser()
    # override default ContextHandler
    handler = DBLP_Handler()
    parser.setContentHandler(handler)
    # creates a SAX parser to parse the given xml file
    parser.parse('dblp_sample.xml')
    handler.to_df()
    # handler.save()
    # handler.to_csv()

        