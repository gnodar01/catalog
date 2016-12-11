# README
Udacity Full-Stack Nanodegree: Project 3 - Catalog

An Application that provides allows the creation of Catalogs, categories, and customized records for each category.

## Server Info
* IP Address: `35.163.169.28`
* SSH Port: `2200`
* App address: `http://ec2-35-163-169-28.us-west-2.compute.amazonaws.com/`
 
### Ubuntu Packages
* finger
* apache2
* libapache2-mod-wsgi
* postgresql
* python-psycopg2
* git
* python-flask
* python-sqlalchemy
* python-pip

### Python Packages
* oauth2client
* requests
* httplib2 

### Configurations
* sudo privilage to user grader
* permissions in `/etc/sudoers.d/grader`: `grader ALL=(ALL:ALL) ALL`
* Set local timezone to UTC
* Changed SSH port from 22 to 2200
* Configured Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123)

## Navigating and using the App
* To create a new Catalog you will need to "Log In"
	* On the top right click log in, or click "Create New Catalog" and you will be redirected to the login screen
	* You may use your Google or Facebook account to log in
* Once you have logged in click "Create New Catalog", and give it a name
* You will then need to create one or more Categories for your Catalog, by clicking "Create New Category"
* Each Category is populated with Records. To create a Record, you will first need to create a Record Template. To do this, click "Add Record" followed by "Create New Record Template"
	* The Record Template defines the layout the Category's Records; you may define one or more fields
	* Give the field a label, and choose the field kind
		* Field kinds include Short Text input fields, Long Text Input Fields, Check Box Lists, Radio Lists, and Drop Down Menus
		* If you choose Check Box, Radio, or Drop Down, you will need to define one or more options for this field
	* If a Field Kind that requires options is chosen, you will be shown a new input to define the Option.
		* To add additional Options, click the Plus Icon
		* To remove an Option, click the Subtract Icon to the right of the input
	* To add an additional Field, click the "Add Field" button
	* To remove a Field, click the Subtract Icon to the right of the Field Label input
* Once you have defined a Record Template, you will be redirected to the Add Record screen, and you will see your new Template under "Your Templates"
* You may now add one or more Records for this Category, using your Record Template
* After you have made a record. You can edit it by clicking the Pencil Icon
* You may edit the names of Record Templates, Categories, or Catalogs by clicking the Pencil Icon next to their names
* You may delete Catalogs, Categories, Record Templates, or Records by clicking the Trash Can Icon next to thier names
	* If you delete a Parent, all of it's children will be deleted along with it
		* For example if you delete a Catalog, all Categories, Record Templates, and Records contained inside of it will also be deleted
* Each user is only able to Edit and Delete Catalogs, or their contents, if they were the original creator
* You may log out at any time by clicking "Log Out" on the top right of your screen
