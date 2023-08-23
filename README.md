TECH STACK
Python
Django
PostgreSQL
Celery
RabbitMQ
Docker
Ubuntu
I. DESCRIPTION

This app represents a basic web aggregator that collects, processes and
renders the data on the web page, allowing searching particuar items.



II. TECHNICAL INFO

The web application consists of three parts:
1) Web scraping engine;
2) Data engine;
3) Data rendering app;

DATA MINING
The work begins with starting a connection to the target source
and extraction of the links from each page, till the end, so the
links are saved to a flat file for further use.
The saved liks are retrieved from the flat file and formed to an
iterable, and another part of the engine uses each of the links
to throw a request to the source. After the target server has given
back the responses, all of them are arranged in the asynchronous flow
so there are as many responses given as the links.
All the responses are taken by the DataFetcher and the dict objects are
formed from each response and packed into the list.

SAVING OF THE DATA
The structured objects are validated whether the're of the right type or not
and saved to the database.

DATA RENDERING
The web application queries the data from the database, forms it to the python
objects and puts each of them on the HTML template.



III. UML SCHEMES

WEB SCRAPING ENGINE
<img src="schemes/webscraper.puml">

DATA MANAGER
<img src="schemes/data_engine.puml">

DATA RENDER
<img src="schemes/data_render.puml">



IV. DATABASE SCHEME
<img scr="schemes/database.puml"