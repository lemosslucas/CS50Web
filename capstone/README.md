# Polybook  
A website to read books in multiple languages and become fluency  
![image](https://github.com/user-attachments/assets/b0d06af6-c9ae-4c44-b195-d9f86f357a50)
*Polybook Interface*

## Distinctiveness and Complexity  
Polybook is a website offering a multicultural library of PDF books, combining advanced features such as internet book search, real-time word translation, and reading with a unique PDF viewer. With the goal of promoting learning and fluency in languages efficiently and in a fun way.

The website offers several features, including:  
- **Search**: Find PDF books available on the internet.
  - Example of Search Function:
  ![image](https://github.com/user-attachments/assets/0a4b9be5-c1d5-4e3e-909b-46f4ab964fbb)
  *Search Results*

  - You need to choose one of these links
  ![image](https://github.com/user-attachments/assets/298e4c1e-a6cd-4874-becf-80fac9d7ce89)
  *Example of Download options*

- **Upload book**: Enrich the library uploading books.
  - You need to click in upload a book and fill the requeriments, after click in save changes
  ![image](https://github.com/user-attachments/assets/734b61a9-cf2a-4e1e-98fb-bf24b9767d9a)
  *Upload Form*

- **Read a book**: Open a page with all books available in the database, showing the title, cover, language, and gender. When you click on the chosen book, you can read it in a unique PDF viewer developed for Polybook.
  - Click the read book button on the top the page you are redirect to this page
    ![image](https://github.com/user-attachments/assets/1cad4ae8-ffcb-4f10-bc09-69442e36de43)
    *Books availabes*
    
    ![image](https://github.com/user-attachments/assets/f2437861-99e2-4f92-8469-8cd0fadbee83)
    *PDF viewer*
- **Word translation and saving**: While reading, if you encounter a word you don't know, you can select it to get an instant translation. This translated word can then be saved to a database, where you can review it later.
  - Select the text and click in 'translate text' and your text are transalated
    ![image](https://github.com/user-attachments/assets/37ec27df-ee28-463d-8573-dc1322faeec9)
    *Select Text and Translate*
    
    ![image](https://github.com/user-attachments/assets/94a5eb8e-1516-478d-965b-8ab4f6bf53a8)
    *Words database*

This project is complex compared to many others because it integrates various technologies, including:  
1. **Web scraping** to find and download books in the web.  
2. **PDF-to-text conversion** in Python to enable text-based features.  
3. **JavaScript functionality** for creating an interactive PDF viewer and enabling word selection and translation on the website.  

## File Structure  
- `db.sqlite3`: The SQL database file.  
- `manage.py`: The Django management script to run the server.  
- `capstone/`:  
  - `urls.py`: Defines the URL paths for the Polybook pages.  
- `polybook/`:  
  - `admin.py`: Manages the website's data through the admin interface.  
  - `models.py`: Contains the classes used to define the database objects.  
  - `urls.py`: Defines the URL paths specific to the Polybook application.  
  - `views.py`: Contains the functions that handle the application logic and interact with the database.  
  - `/templates/polybook/`: HTML templates used for the website's front-end.  
  - `/static/polybook/`:  
    - `read.js`: JavaScript file for front-end functionalities.  
    - `styles.css`: CSS file for custom styling.
  - `/media`:
    - `/covers`: Stores the cover's book
    - `/media/pdfs`: Stores the books in PDF format
      
## Libraries
For running the Polybook you need to install the librarys in 'requirements.txt'  
```bash
pip install -r requirements.txt
```
## How to Run the Project 
To apply changes to the database, run the following commands:
```bash
python manage.py makemigrations
python manage.py migrate
```
To start the server, run the following command:  
```bash
python manage.py runserver
```
To create an admin user, run the following command:
```bash
python manage.py createsuperuser
```

## Technologies Used  
### Languages  
- **[Python](https://python.org)**  
- **[JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)**  
- **[HTML](https://developer.mozilla.org/en-US/docs/Web/HTML)**  
- **[CSS](https://developer.mozilla.org/en-US/docs/Web/CSS)**  

### Database  
- **[SQLite](https://www.sqlite.org/index.html)**  

### Frameworks and Libraries  
- **[Django](https://www.djangoproject.com/)**: For backend development and database management.  
- **[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)**: For web scraping.  
- **[PyPDF2](https://pypi.org/project/PyPDF2/)**: For extracting text from PDF files.  
- **[pdf.js](https://mozilla.github.io/pdf.js/)** A library to display and extract content from PDF files in the browser.

### APIs
- **[MyMemory Translated](https://mymemory.translated.net/doc/spec.php)** API for real-time text translation.

# Credit
### Developer
- **[Lucas Lemos Ricaldoni](https://github.com/lemosslucas)**
