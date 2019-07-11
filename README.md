# Item Catalog
Item Catalog project for Full Stack Web Developer Nanodegree from Udacity

## Getting Started
Install [Vagrant](https://www.google.com/url?q=http://vagrantup.com/&sa=D&ust=1562760712425000) and [VirtualBox](https://www.google.com/url?q=https://www.virtualbox.org/&sa=D&ust=1562760712425000).

Follow these [instructions provided by Udacity](https://www.google.com/url?q=https://www.udacity.com/wiki/ud088/vagrant&sa=D&ust=1562760712425000).

Using the terminal, change directory to /vagrant (cd /vagrant), then type ```vagrant up``` to launch your virtual machine.

Once it is up and running, clone this repository to your vagrant directory.
```
$ git clone https://github.com/jpchungyew/item-catalog-project.git
```

Type ```vagrant ssh``` to log into the virtual machine. This will log your terminal in to the virtual machine, and you'll get a Linux shell prompt.

Navigate to the shared vagrant directory by typing ```cd /vagrant```.

Navigate into catalog directory, where the repository was downloaded to.

In the prompt, type in the following to get the application up and accessible on localhost:8000:
```
$ export FLASK_APP=application.py
$ python -m flask run --host=0.0.0.0 --port=8000
```

To seed the database with dummy data, run the following:
```
$ python dummy_data.py
```

To log out, type ```exit``` at the shell prompt. To turn the virtual machine off (without deleting anything), type ```vagrant halt```. If you do this, you'll need to run vagrant up again before you can log into it.

