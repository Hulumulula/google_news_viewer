# Google News Viewer
GNV - a module that allows you to get a list of news from news.google.com,  
and then view them in the chrome browser and write new session cookies to the database.

## INSTALLATION
Download the project to your directory.  
```bash
git clone https://github.com/Hulumulula/google_news_viewer.git
```

Create a virtual environment,  
install the packages from requirements.txt there and select your environment.   
```bash
pip install -r requirements.txt
```  

Create a .env file to edit the variables. (optional)   
See [SETTINGS](#settings) for descriptions and what they do. 

As standard, you can put [WebDriver](https://chromedriver.chromium.org/downloads)   
in the `driver/webdriver.exe` folder next to `core`.   
(If this is not done the `Manager` will download it to its own memory).

## RUN
To run the project, navigate to the location of main.py and run  
```bash
python main.py
```  

After the first run, you will have two directories `logs` and `db`.  
Logs will store the `debug_{datetime}.logs`  
DB stores the database (SQLite3)

## SETTINGS
The example settings are stored in the .env-example  

* WEBDRIVER_PATH - Accepts the type `str(path)`. Path to the webdriver.  
    By default it looks in `driver/webdriver.exe`.  
    If it does not find it there is an error.  
    If empty - Manager downloads driver into memory.  
    ⚠️***Caution: driver and browser versions mismatch can cause unexpected errors.***  
  
* DB_LOCATION - Accepts the type `str(path)`. The path to the database.  
    By default it is set to `db/profile.sqlite3`. 
  
* DEBUG - Accepts the type `bool`. If `True` - All received errors will be logged with trace.  
    By standard - `False`  
    
* HOME_URL - Accepts the type `str`. The full url address from which to parse links.  
    By standard - `https://news.google.com`  
  
* SUBHOME_URL - Accepts the type `str`. Complemented by the `HOME_URL` query:  
    `{HOME_URL}{SUBHOME_URL}`. It first requires `/`. By default - `/home`.
   
* NAMED_URL - Accepts the type `str`.  
    Specifies where the links you're looking for start:  
    For example, with `NAMED_URL='/articles'` and `HOME_URL='https://news.google.com'`,  
    links like `'./articles/...'` or `'https://news.google.com/articles/...'` will be searched.  
    It first requires `/`.  
    By default - `/articles`.
  
* PROCESSES - Accepts the type `int`. Indicates how many processes can be created simultaneously in `Pool`.  
    The standard is ` 5`.
  
* IS_LOGGING - Accepts the type `bool`. If `False` - logging will be turned off. Default is `True`.

