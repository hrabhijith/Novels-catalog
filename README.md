# Project: Item Catalog (Novel Library)

Novel library is a novel catalog website which provides information about novels from various authors.

# Please read the following instructions!

## Highlights

* Users can login using Google or Facebook account and start adding novels under different authors provided.
* Users can only edit or delete novel entries which are added by them after logging in.
* Users can only view novel's information added by other users.
* Home page lists all the authors currently present in database and recently added novels by users.
* Selecting an author takes users to the novels list page of the author.
* Novel's name and year published will be displayed in the novels' list page.
* Users cannot 'Edit' or 'Delete' untill they login.
* After logging in, users can 'Edit' and 'Delete' only those novels which are added by them.
* Users can also add new novel to the list after logging in.
* Selecting a novel will take the user to the novel's description page.
* Novel's description can be edited with 'Edit' button only if the user is logged in and has the authority to edit.
* Users can logout using 'Logout' button after logging in.

## Installation

Follow each section below to install all the required softwares and tools to run this project.

* To run commands on the terminal on your computer (if you don't have one) install:

In **Windows OS**, you can use the Git Bash terminal program from [Git](https://git-scm.com/download/win).
On **Windows 10 OS**, you can use the bash shell in [Windows Subsystem for Linux](https://msdn.microsoft.com/en-us/commandline/wsl/install_guide).
On **Mac OS**, you can use the built-in **Terminal** program, or another such as **iTerm**.
On **Linux**, you can use any common terminal program such as **gnome-terminal** or **xterm**.

* Install Python 3 locally in your computer.

**Windows and Mac:** Install it from python.org according to you computer's OS: [link](https://www.python.org/downloads/)
**Mac (with Homebrew):** In the terminal, run `brew install python3`
**Debian/Ubuntu/Mint:** In the terminal, run `sudo apt-get install python3`

Use this command from the command line to check the installtion status of python `python3 --version`

* Install **Virtual Box**
VirtualBox is the software that actually runs the virtual machine. You can download it from virtualbox.org, [here](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1). Install the platform package for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it; Vagrant will do that.

**Ubuntu users:** If you are running Ubuntu 14.04, install VirtualBox using the Ubuntu Software Center instead. Due to a reported bug, installing VirtualBox from the site may uninstall other software you need.

* Install **Vagrant**
Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. Download it from vagrantup.com, [here](https://www.vagrantup.com/downloads.html). Install the version for your operating system.

**Windows users:** The Installer may ask you to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.
If Vagrant is successfully installed, you will be able to run `vagrant --version` in your terminal to see the version number.

* Once you have VirtualBox and Vagrant installed, open a terminal and run the following commands:

`mkdir project`
`cd project`
`vagrant init ubuntu/trusty64`
`vagrant up`

This will create a new directory for this project and begin downloading a Linux image into this directory. It may take a long time to download, depending on your Internet connection.

When it is complete, you can log into the Linux instance with `vagrant ssh`. You are now ready to continue with the project.

If you log out of the Linux instance or close the terminal, the next time you want to use it you only need to run `cd project` and `vagrant ssh`

## Database

* This project uses SQLlite and SQLAlchemy ORM as database tool and language for queries.
* Before running the python source code, database has to be setup by running following commands.

using either
`python database_setup.py`

or using 
`python3 database_setup.py`

* After this step, Initial DB data has to be inserted by running the following commands. This has to done by the admins if in production.

using either
`python insertauthors.py`

or using 
`python3 insertauthors.py`

## Source Code

The source code is written in the "finalproject.py" file and should be run from linux machine.

According to the python version installed, the code can be run 

using either
`python finalproject.py`

or using 
`python3 finalproject.py`


## Output

By default, the application will start at 'localhost:5000'. Users should enter this url in any browser to start using the application.

