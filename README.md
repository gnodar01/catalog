# README
Catalogizer:
An Application that provides allows the creation of Catalogs, categories, and customized records for each category.

## Running the App
* All files in this repo were developed and tested on Ubuntu 14.04.3 LTS, running on [VirtualBox](https://www.virtualbox.org/wiki/VirtualBox) (v5.0.10) VM, created and configured through [Vagrant](https://www.vagrantup.com/)
  * Install Vagrant on either VirtualBox (free) or your VM of choice
  * The Vagrantfile and pg_config.sh will provides the necessary configuration for Vagrant to run this App
* Clone the Repository
* CD into the repository using command line
* You will need to register your app on [Google](https://console.developers.google.com) and [Facebook](https://developers.facebook.com/docs/apps/register)
  * Generate a `client_secrets.json' for Google
    * Redirect URIs should be set to `localhost:5000/gconnect`, `localhost:5000/login`
    * Javascript Origins should be set to `localhost:5000`
  * Generate a `fb_client_secrets.json` for Facebook
* Run `vagrant up`
* SSH into Vagrant `vagrant ssh`
* CD into the shared vagrant directory `cd \vagrant`
* To pre-populate the database, run python database_populator.py
* To launch the application, run `python catalogizer.py`
* Open your browser and navigate to `http://localhost:5000/`

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