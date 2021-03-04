from bs4 import BeautifulSoup
import requests 

class Scrapper:

    # constructor
    def __init__(self, auto, test):

        self.auto = auto
        self.test = test

        self.findFilters = {
            "url": "https://niw.es/es/coches-segunda-mano",
            "findElement": "section",
            "findValue": {"class": "mdx-result-list mdx-result-list--grid"}
        }

        self.findCars = {
            "url": "https://niw.es/es/coches-segunda-mano/marca/modelo/page1?search=passenger&PRICE_RETAIL_CUR_FROM=7000&PRICE_RETAIL_CUR_TO=43000&MILEAGE_MIL_FROM=15000&MILEAGE_MIL_TO=88000&INITIAL_REGISTRATION_DTE_FROM=2020&INITIAL_REGISTRATION_DTE_TO=2021&FEATURES_MST%5B%5D=HYBRID_ELECTRIC_BOL#result-tools",
            "findElement": "div",
            "findValue": {"class": "tiles-container-10"}
        }

        self.findCar = {
            "findElement": "div",
            "findValue": {"class": "tiles-container-10 s-space-5"}
        }

        self.findMarca = {
            "findElement": "section",
            "findValue": {"id": "breadcrumb"}
        }

        self.index = 0

        self.elements = [
            'Combustible', 
            'Transmisión', 
            'Kilometraje', 
            'Fecha de registro', 
            'Potencia', 
            'Puertas', 
            'Plazas', 
            'Ciudad']


        self.filters = {
            "Ciudad":{
                "type": "A",
                "query": "&POOL_REGION_STR",
                "list" : []
            },
            "Marca":{
                "type": "A",
                "query": "&MANUFACTURER_LST",
                "list" : []
            },
            "Price":{
                "type": "B",
                "query": "&PRICE_RETAIL_CUR_",
                "list" : [1,50000]
            },
            "KM":{
                "type": "B",
                "query": "&MILEAGE_MIL_",
                "list" : [1,100000]
            },
            "Year":{
                "type": "B",
                "query": "&INITIAL_REGISTRATION_DTE_",
                "list" : [0,6]
            },
            "Color":{
                "type": "C",
                "query": "&BODY_BASE_COLOR_LST%5B%5D",
                "list" : ["YELLOW","BLUE","BEIGE","WHITE","GREY","BROWN","ORANGE","BLACK","GOLD","SILVER","RED","PINK","GREEN","PURPLE"]
            },
            "Combustible": {
                "type": "A",
                "query": "&FUEL_TYPE_LST",
                "list": ["DIESEL", "ELECTRIC", "LIQUEFIED_PETROLEUM_GAS", "COMPRESSED_NATURAL_GAS", "PETROL"]
            },
            "nseats":{
                "type": "C",
                "query": "&NUMBER_OF_SEATS_INT%5B%5D",
                "list" : [1,2,3,4,5,6,7,8,9]
            },
            "ndoors":{
                "type": "C",
                "query": "&NUMBER_OF_DOORS_INT%5B%5D",
                "list" : [1,2,3,4,5,6,7]
            },
            "Potencia":{
                "type": "B",
                "query": "&ENGINE_PWR_",
                "list" : [1,200]
            },
            "Transmisión":{
                "type": "C",
                "query": "&TRANSMISSION_LST%5B%5D",
                "list" : ["AUTOMATIC", "MANUAL", "SEMIAUTOMATIC"]
            }
        }

        self.elementType = {
            "A": ["Write a single element from the list (Enter to skip filter)"],
            "B": ["Write the lowest value to filter (Enter to skip lowest)", "Write the highest value to filter (0 to skip highest)"],
            "C": ["Write multiple elements from the list (Enter to skip filter)"]
        }



    # BS FUNCTION
    def findElement(self, options):
        """
        INPUT: DICTIONARY WITH KEY ELEMENTS TO FIND MATCHES WITH BEAUTIFUL SOUP
        OUTPUT: LIST OF MATCHES
        """
        r = requests.get(options["url"]) 
        soup = BeautifulSoup(r.text, "html.parser") 
        items = soup.find_all(options["findElement"], options["findValue"])
        return items

    # GET FILTERS
    def getFilters(self):
        """
        OUTPUT: LIST OF CITIES AND BRANDS TO POPULATE MAIN FILTER DICTIONARY
        """
        filters = self.findElement(self.findFilters)[0]
        selectableFilters = {
            "Marca": "mdx-manufacturer_lst-passenger",
            "Ciudad": "mdx-pool_region_str-passenger"
        }
        
        for f in selectableFilters:
            items = filters.find_all("select", {"id": selectableFilters[f]})[0].contents
            finalItems = [x["value"] for x in items]
            self.filters[f]["list"] = finalItems[1:]

        
    # CREATE SEARCH
    def createSearch(self):
        """
        OUTPUT: URL WITH QUERY FILTERS APLIED
        """
        # ASK USER
        print('Welcome to NIW.es')
        print("I am going to show you all the cars we have available, please use the following filters to make an accurate search:")
        print("It is important to respect uppercase and lowercase letters")
        input("Press Enter to continue...\n")

        filters = self.filters
        elementType = self.elementType

        # USER INPUT FOR EACH FILTER
        k=0
        for f in filters:
            x = filters[f]
            print("\n"+f)                       # print element name
            print(filters[f]["list"])           # print list options
            question = elementType[x["type"]]
            value = []
            for q in question:
                ## AUTO VS MANUAL
                if self.auto == True:
                    a = self.test[k]
                else:
                    print(q)
                    a = input()
                
                value.append( str(a) )
                k+=1
            filters[f]["value"] = value

        # CORRECT YEAR
        self.correctYear()

        # CREATE URL
        finalUrl = "https://niw.es/es/coches-segunda-mano/{marca}/modelo/page1?search=passenger"
        q = ""
        for f in filters:
            value = filters[f]["value"]
            ftype = filters[f]["type"]

            # MARCA
            if f == "Marca":
                finalUrl = finalUrl.format(marca = "marca")
                
            # SINGLE CHOICE
            if ftype == "A":
                if value[0] != "": 
                    q += filters[f]["query"] + "=" + value[0]

            # FROM TO
            if ftype == "B":
                if value[0] != "": 
                    q += filters[f]["query"] + "FROM=" + value[0]
                if value[1] != "": 
                    q += filters[f]["query"] + "TO=" + value[1]

            # MULTIPLE CHOICE
            if ftype == "C":
                if value[0] != "": 
                    vals = value[0].split(" ")
                    for v in vals:
                        q += filters[f]["query"] + "=" + v

        finalUrl += q
        finalUrl += "#result-tools"
        self.findCars["url"] = finalUrl

        print('\nUrl to check them in the web')
        print(finalUrl)
        print('\nSearching cars that match your criteria...')

    # YEAR OF USE TO AGE OF CAR
    def correctYear(self):
        a = self.filters['Year']['value'][0]
        b = self.filters['Year']['value'][1]
        self.filters['Year']['value'][0] = b
        self.filters['Year']['value'][1] = a

        for i in range(2):
            x = self.filters['Year']['value'][i]
            if x != "":
                self.filters['Year']['value'][i] = str( 2021-int(x) )

    # GET DATA
    def getCars(self):
        """
        INPUT: URL WITH QUERY FILTERS
        OUTPUT: LIST OF CARS THAT MATCH WITH A URL 
        """

        # EXTRACT CARS FROM A SPECIFIC PAGE
        cars = self.findElement(self.findCars)[1].contents
        finalCars = list(map(self.getCar, cars))
        finalCars = list(filter(None, finalCars)) # delete adds

        # PRINT PAGE OF CARS
        if len(finalCars) > 0:

            print('\nCars found:\n')
            k = self.index
            for f in finalCars:
                k+=1
                print('Car number '+str(k)+":")
                print(f)
                print("")           

            # NEXT PAGE 
            self.index = k
            url = self.findCars["url"]
            pageStart = url.find('page')+4
            pageEnd = url.find('?',pageStart)
            pageNumber = int(url[pageStart:pageEnd])
            self.findCars["url"] = url[:pageStart] + str(pageNumber+1) + url[pageEnd:]
            input("Press Enter to see next page...\n")
            print("Searching more cars...")
            self.getCars()
        
        else:
            print('I hope you have found a car that suits you!')


        
    def getCar(self, item):
        """
        INPUT: URL OF a SPECIFIC CAR
        OUTPUT: DICTIONARY OF A CAR WITH ALL THE RELEVANT DATA
        """
        try:
            href = "https://niw.es" + item.find_all('div', {"class": "column block"})[2].contents[0].attrs["href"]
            self.findCar["url"] = href
            self.findMarca["url"] = href
            carData = self.findElement(self.findCar)[4].contents
            car = self.getData(carData)
            car["href"] = href
            return car

        except:
            return None

    def getData(self, x):
        """
        INPUT: DIV ELEMENT CONTAINING RELEVANT INFO ABOUT A CONCRETE CAR
        OUTPUT: DICTIONARY WITH THAT DATA + 
        """

        def getElement(e):
            el = x[0].find_all("li", {"title": e})[0].contents[1].contents[0]
            data[e] = el

        data = {}
        
        # Combustible Transmisión Kilometraje Fecha de registro Potencia Puertas Plazas Ciudad
        elements = self.elements
        for e in elements:
            getElement(e)

        try:
            color = x[0].find_all("div", {"class": "bodyBaseColor"})[0].attrs['data-color']
        except:
            color = 'not found'

        # COLOR
        data["Color"] = color

        # PRICE
        price = x[1].find_all("span", {"id": "summary_price"})[0].attrs['data-summary']
        data["Price"] = price

        # BRAND
        data["Marca"] = self.findElement(self.findMarca)[0].contents[0].contents[0].contents[2].contents[0].contents[0]

        return data

    # MAIN
    def run(self):
        self.getFilters()
        self.createSearch()  
        self.getCars() 
     

if __name__ == '__main__':
    
    auto = 1    # 0: ENTER FILTERS HERE. 1: ENTER FILTER WITH INPUTS
    test = [
        'Madrid',       # CITY: CAPITALIZED
        'BMW',          # BRAND: UPPERCASE
        '20000',        # MIN PRICE [0]
        '200000',       # MAX PRICE [500.000]
        '',             # MIN KM [0]
        '40000',        # MAX KM [1.000.000]   
        '0',            # MIN AGE [0]
        '4',            # MAX AGE [6]
        'YELLOW BLUE RED BLACK GREY',       # COLOR: UPPERCASE 
        'PETROL',       # COMBUSTIBLE: UPPERCASE
        '2 3 4',        # N SEATS [1-9]
        '',             # N DORS [1-7]
        '50',           # MIN POWER [0]
        '',             # MAX POWER [300]
        'AUTOMATIC MANUAL']     # TRANSMISSION: UPPERCASE

    test = [
        '',       # CITY: CAPITALIZED
        '',          # BRAND: UPPERCASE
        '',        # MIN PRICE [0]
        '',       # MAX PRICE [500.000]
        '',             # MIN KM [0]
        '',        # MAX KM [1.000.000]   
        '0',            # MIN AGE [0]
        '4',            # MAX AGE [6]
        'YELLOW BLUE RED BLACK GREY',       # COLOR: UPPERCASE 
        '',       # COMBUSTIBLE: UPPERCASE
        '',        # N SEATS [1-9]
        '',             # N DORS [1-7]
        '',           # MIN POWER [0]
        '',             # MAX POWER [300]
        'AUTOMATIC']     # TRANSMISSION: UPPERCASE

    S = Scrapper(auto, test)
    S.run()

