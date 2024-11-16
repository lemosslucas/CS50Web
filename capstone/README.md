# Polybook  
A website to read books in multiple languages and become fluency  
![image](https://github.com/user-attachments/assets/9d05cd36-29ef-4fac-ac13-ed4e2df6cda3)
*Polybook Interface*

## Distinctiveness and Complexity  
Polybook is a website where users can search, upload, download, and read books in PDF format, creating a rich library of multicultural content.  

The website offers several features, including:  
- **Search**: Find PDF books available on the internet.

Example of Search Function:
  ![image](https://github.com/user-attachments/assets/068daf55-1890-457a-9a33-64f22d021aca)
You need to choose a one of those links to download you book
-![image](https://github.com/user-attachments/assets/9fed8b96-a7b8-4923-b693-bfe82006e968)

- **Upload book**: Enrich the library uploading books.
- You need to click in upload a book and fill the requeriments, after click in save changes
![image](https://github.com/user-attachments/assets/8b994103-212a-43d3-8e85-7050147f7c23) 
- **Read a book**: Open a page with all books available in the database, showing the title, cover, language, and gender. When you click on the chosen book, you can read it in a unique PDF viewer developed for Polybook.
![image](https://github.com/user-attachments/assets/adcacf5c-53cd-4c2a-ae93-7efd3b40b920)
*Books availabes*
![image](https://github.com/user-attachments/assets/357f2071-3090-4ced-98f7-659339556638)
*PDF viewer*
- **Word translation and saving**: While reading, if you encounter a word you don't know, you can select it to get an instant translation. This translated word can then be saved to a database, where you can review it later.  
![image](https://github.com/user-attachments/assets/4f356eef-dad5-4b96-b323-12bce7b7c665)
![image](https://github.com/user-attachments/assets/a7ccb21c-8f33-444b-acd7-de80ba439a37)

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
pip install -r requiriments.txt
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
