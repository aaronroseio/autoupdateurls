# autoupdateurls

## High Level Functions:
* Runs on Check Point's GAIA (using the built in python modules)
* Downloads a list of URLs from GitHub
* Parses the URLs from the list and adds them to a custom application/site object 
* Pushes policy (by default it only publishes policy, but you can uncomment the lines to install as well)
* This object can be used for dynamic allow/block lists

## Requirements
* Python 2.7 or greater
* Check lines 12 & 13 - be sureto download the CA bundle as instructed

## Setup
* Clone the Python script to your host
* Download the CA bundle (see above) 
* Modify the variables:
  * Line 15 - Add the URL of the suspicious domain list on GitHub (or similar repository) that you would like to use
  * Line 17 - Change the name of the Application/Site URL object that will be created if you wish 
  * Line 20 - Change the domain if you're using this in a Multi-Domain environment
  * Line 21 - Name of your policy package if not "Standard" 
  * Line 22 - Installation Targets (gateway name) 
* For unattended (cron, etc.) use:
  * Line 19 - Add your API Key
  * Uncomment line 115 and comment out lines 109 - 112
