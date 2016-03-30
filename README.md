## To run the program, please follow the procedures below:
* Clone https://github.com/apewiki/fullstack-nanodegree-vm.git
```git clone https://github.com/apewiki/fullstack-nanodegree-vm.git mydirectory
* Install Vagrant
* cd vagrant directory and bring up VirtualBox
```
vagrant up
```
```
vagrant ssh
```
* cd /vagrant
* cd catalog_proj

##Start the app
* Database setup
```
python database.py
```
* Populate databse with some records
```
python populateItems.py
```
* Start the app
```
python catalog.py
```

## Description:
There are a four categories in the catalog. Each category is populated with a few items. 
You will not be able to edit these items because they were not created by you.
To  add/Edit/Delete items, please follow the procedures described below.

To add item:
- Login though orange button on top right corner
	- You may login through either Google+ account or Facebook
	- To add a picture for a new item, please load a picture file from your computer. 
	  The file should be located at /static/images/ directory.

To edit/delete item:
- Login in as specified in "Add item"
- You may only edit/delete items added by you