# Simple Heureka + tests
This repository contains a simple web app written in Python which mimics e-shop products'
advisor/comparator Heureka - https://www.heureka.cz

Repository also contains tests for the application.

## Table of contents
  * [Prerequisites](#prerequisites)
    + [Application](#application)
    + [Tests](#tests)
    + [Instalation on Linux Mint / Ubuntu](#instalation-on-linux-mint--ubuntu)
    + [Installing the virtual environment](#installing-the-virtual-environment)
    + [Installing Selenium for end-to-end tests](#installing-selenium-for-end-to-end-tests)
        * [Local installation and running](#local-installation-and-running)
        * [Browserstack](#browserstack)
  * [Running the app](#running-the-app)
    + [Configuration](#configuration)
    + [Running the app Locally](#running-the-app-locally)
    + [Running the app on Heroku](#running-the-app-on-heroku)
      - [How to deploy the app to Heroku](#how-to-deploy-the-app-to-heroku)
  * [Running tests](#running-tests)
    + [Unit tests](#unit-tests)
    + [Integration tests](#integration-tests)
    + [End-to-end tests](#end-to-end-tests)
      - [Configuration](#configuration-1)
      - [Running end-to-end tests](#running-end-to-end-tests)
  * [Documentation](#documentation)
    + [The Application](#the-application)
      - [Description](#description)
      - [Resources](#resources)
    + [Data for the application](#data-for-the-application)
      - [Data caching](#data-caching)
    + [Models](#models)
    + [Libraries](#libraries)
    + [HTML Templates](#html-templates)
    + [Application routing](#application-routing)
    + [Static content](#static-content)
    + [Tests](#tests-1)
      - [Unit tests](#unit-tests-1)
      - [Integration tests](#integration-tests-1)
      - [End-to-end tests](#end-to-end-tests-1)
        * [Libraries](#libraries-1)
        * [Fixtures](#fixtures)
        * [Components](#components)
        * [Page objects](#page-objects)
        * [Actual tests](#actual-tests)
        * [Screenshots](#screenshots)
    + [Source code documentation](#source-code-documentation)

## Prerequisites
All the shell scripts in the repo expect a Linux distribution, so Linux OS is
recommended, tested on Linux Mint 18 Sarah (based on Ubuntu 16.04 LTS).

### Application
The web app needs following:
* Python 3.5+ + `venv` module for maintaining Python virtual enviroments
    * i.e. `python3.5` package
    * i.e. `python3.5-venv` package
* Redis in-memory data store - `redis-server` package

### Tests
Additionally end-to-end tests need:
* `wget` - `wget` package - needed for Selenium installation
* `unzip` - `unzip` package - needed for Selenium installation
* `java` - i.e `openjdk-8-jre` package - needed for running Selenium server
* Chromium browser *version 66+* (or Chrome browser), i.e `chromium-browser`
  package - needed for browser automation

### Instalation on Linux Mint / Ubuntu
First resynchronize package index:
```
# sudo apt-get update
```
And then install missing packages by running:
```
# sudo apt-get install <package-name>`
```

### Installing the virtual environment
The next step is to install virtual environment for the app and for tests, run:
```
# ./init_venv.sh
```
You should see successful installation of all needed Python packages from PyPI into your newly created virtual
environment located in `venv` directory.

### Installing Selenium for end-to-end tests
For browser automation you can:
* either install Selenium server locally
* or use Browserstack testing platform - you need to have an account there - they provide Selenium on
various operating systems and also various browsers and their versions.


##### Local installation and running
For local installation, simply run:
```
# ./install-selenium.sh
```
The script installs Selenium Standalone Server JAR file and Chromedriver
to the `selenium` directory.

Then you can run Selenium by
```
# ./run-selenium.sh
```

##### Browserstack
You can also run end-to-end tests using Browserstack instead of using local or remote Selenium server.

It is possible to create a free trial account on Browserstack if you don't have any there yet.
Then you will need your _Username_ and _Access Key_ - you can find
those in _Account | Settings_ when logged in.


## Running the app

### Configuration
App configuration is stored in YAML configuration file `app/config.yaml`

It is also possible to override this file's configuration by
adding `app/config.local.yaml` file - this one takes precedence before the former one.

The file must contain following two configuration keys:
* `api_url` - where the API which provides data for the app is running
* `redis_url` - where redis is running - this value is preset for Heroku deployment
```
api_url: http://python-servers-vtnovk529892.codeanyapp.com:5000
redis_url: $REDIS_URL
```
If syntax `$VAR_NAME` is used for the value,
it means the value is expected to be in enviromental variable `VAR_NAME`.

In case you want to run the application locally and don't want to export the REDIS_URL variable,
change the `redis_url` key value like this:
```
redis_url: http://localhost:6379
```

### Running the app Locally
For running the app locally, namely for development purposes, simply run:
```
# ./run-app.sh
```
Then you can open the app in your browser at `http://localhost:5000`

### Running the app on Heroku
It is also possible to deploy the app on Heroku Cloud Application Platform - https://www.heroku.com

#### How to deploy the app to Heroku
Assumption is that you have this repository already cloned and checked out.

First Create an account on Heroku if you don't have one already

Then Install Heroku CLI, see - https://devcenter.heroku.com/articles/heroku-cli#download-and-install

Then Login to heroku from the command line:
```
# heroku login
```

After you are successfully logged-in, create a new project on Heroku:
```
heroku create my-heureka-app
```
where `my-heureka-app` is name of the project (you can of course choose your own name).

Then go to http://www.heroku.com, log in, open your new project and go to *Resources* of the project.

Under *Resources*, search for an Add-on *Heroku Redis* and then add it to the project.

Then go to your command line and push the code to Heroku:
```
git push heroku <your-local-branch-to-be-deployed>:master
```

You should see logs how the project is being deployed and eventually the deployment is successfully finished.

Your app should be running now at https://my-heureka-app.heroku.com.

## Running tests
Repository contains following tests for the application:
* unit tests which test the app code on the lowest level
* integration tests which test integration of particular app parts with real API and real Redis
* end-to-end tests which test the whole running app using browser automation

As mentioned above for browser automation Selenium browser automation tool is used - https://www.seleniumhq.org/

### Unit tests
For unit tests run:
```
# ./run-unit-tests.sh
```

### Integration tests
For integration tests it is expected that Redis is up and running and that the real API is up and accessible, then you can run:
```
# ./run-integration-tests.sh
```

### End-to-end tests
Selenium server has to be already running or Browserstack access is needed in
order for end-to-end tests to work, see next section.

#### Configuration
End-to-end tests need to be configured namely to know:
* where the app runs
* which Selenium server to use

End-to-end tests have their own configuration in `test_e2e/config.yaml` file,
or again you can override it with `test_e2e/config.local.yaml` file - this one takes precedence before the former one.

The file must contain following three configuration keys:
* `app_url` - where the app is running
    * i.e. `http://localhost:5000` when running locally
    * i.e. `https://my-heureka-app.heroku.com` when running on Heroku
* `remote_driver_url`: where to connect to Selenium server
    * `http://localhost:4444/wd/hub` for locally running Selenium server
    * `http://<user>:<access_key>@hub.browserstack.com:80/wd/hub` for Browserstack
* `log_level` - level of logging, i.e. `info`

#### Running end-to-end tests
When everything is set up, you can run all end-to-end tests by:
```
# ./run-e2e-tests.sh
```

## Documentation

###  The Application

#### Description
The application mimics in a simple way real e-shop products' advisor/comparator Heureka - https://www.heureka.cz.

* On its homepage it offers categories of the products
* On the category page it shows products belonging to the category
* On the product page it shows details of the product and price comparison among mock shops that offer the product

#### Resources
The aplication is written in Python 3 and is using following 3rd party libraries:
* Flask microframework for handling HTTP requests - http://flask.pocoo.org
* Jinja2 templating language for generating HTML pages - http://jinja.pocoo.org
* Bootstrap library for styling the web application - https://getbootstrap.com
* Requests library for communication with external API - http://docs.python-requests.org
* redis-py library for communicating with Redis in-memory data store - https://github.com/andymccurdy/redis-py
* PyYAML library for reading configuration files - http://pyyaml.org/wiki/PyYAML
* Gunicorn WSGI HTTP Server for running a real HTTP server - used in deployment on Heroku - http://gunicorn.org

### Data for the application
The app relies on an existing API which provides data for the app - the API is not part of this repository, see https://catalogue9.docs.apiary.io

#### Data caching
The app makes calls to the API to get necessary data needed to form a HTML page which is then being served to the browser.

To prevent API overload and to provide better UX - shorter page loading time on the client's side -
responses from API calls are being cached using Redis in-memory data store (see https://redis.io) with a predefined expiration timeout.

When a particular API call response expires in the cache, it is fetched from the API next time when
requesting the data and then cached again.

### Models
In `app/models.py` there are models for the app:
* `AllCategories` - class that represents a collection of all categories
* `Category` - class that represents a category of product
* `Product` - class that represents a product
* `Offer` - class that represents an offer of a product on a particular shop
* `Pagination` - generic class that provides data for pagination component
    * calculates total pages for the products in a category, etc.

### Libraries
Own specific libraries for the application are located in `app/libs` directory
* `api.py` - `CachedApi` class that implements communication to the API together with caching the responses
* `redis_cache.py` - `RedisCache` class which implements communication with Redis in-memory data store

Own shared libraries - libraries for the app and tests - are in `app/shared`
* `configuration.py` - library with `Configuration` class which implements reading the configuration from a YAML file

### HTML Templates
Templates are stored in `app/templates` directory
* `base.html` - base template for all pages which is then extended by a particular page
* `categories.html` - template for home page of the aplication, list of categories
* `category.html` - template for page where products of a particular category are shown
* `product.html` - tempate for product page where information about product are shown
* `oops.html` - error page template for showing `404 Not Found` and `500 Internal Server Error` HTTP errors

These templates include templates in `app/templates/include` directory, which provide some commonly used parts in an application page:
* `categories_menu` - template for categories sidebar
* `pagination.html` - template for pagination component of the page
* `product_comparison.html` - template for product comparison part of the product page
* `product_specification.html` - template for product specification part of the product page
* `title_bar.html` - title bar of the application

HTML is styled with Bootstrap library which is linked directly from BootstrapCDN - see https://getbootstrap.com/docs/4.1/getting-started/download/#bootstrapcdn

Where needed the app is styled directly in HTML or using custom styles, for those see [Static content](#static-content)

### Application routing
Application routing and how HTML templates are populated is defined in `app/views.py` file, the app serves following paths:
* `/` - homepage - list of categories
* `/categories/<category_id>` - category page
* `/products/<product_id>` - product page

Both category and product page also support pagination using query string parameter `page`, i.e. `/categories/1?page=2`

### Static content
Static content for the application is in `app/static` directory
* `images` - directory with images for the aplication
* `styles` - directory for custom CSS styles

### Tests
Unit tests, integration and end-to-end tests are also provided in the repo.
They are written using following 3rd party libraries:
 * `pytest` - test runner, see https://pytest.org
 * `selenium` - library for communication with selenium server, see https://pypi.org/project/selenium/
 * `daiquiri` - library for logging, slightly more user friendly than standard `logging` library

#### Unit tests
These are located in `app` directory, always next to the file that they test:
* `app/test_models.py` - tests for models
* `app/libs/test_api.py` - tests for `CachedApi` class
* `app/libs/test_redis_cache` - tests for `RedisCache` class

These tests use mocks where appropriate to test only the functionality of the class in the isolation.

#### Integration tests
These are located in the `test_integration` directory - their aim is to test parts of the code that
interact with external entities:
* `test_integration/test_api.py` - checks whether real API data are parsed correctly
* `test_integration/test_redis_cache.py` - tests check that:
    * communication with real Redis in-memory cache works as expected
    * cache invalidation works as expected

These tests also use mocks where appropriate to test only the exact functionality we want to test in this scope.

#### End-to-end tests
These are located in the `test_e2e` directory - their aim is to test the application in the whole
and exactly the same way as the user will use it with his browser.

For that Selenium Standalone Server is used as a browser automation tool - see https://www.seleniumhq.org

It enables to control the browser the same way as user controls it - by clicking, typing into the web page which is running in the browser.

##### Libraries
Own libraries in the `test_e2e/libs` directory provide support for tests
* `browser.py` - provides:
    * browser startup and teardown
        * support for locally/remotely running Selenium
        * support for Browserstack platform
    * means to save a screenshot when test fails

##### Fixtures
Own Pytest fixtures for test setup and teardown are in `test_e2e/fixtures` directory
* `browser.py` - calls functions from `browser.py` library for browser setup/teardown
* `logging.py` - setups logging and logs basic info about test execution

##### Components
In directory `test_e2e/components` there are modules with classes that implement
HTML page components abstraction - HTML code which is used across multiple HTML pages.
They also encapsulate all the Selenium code for that:
* `web_component.py` - base class `WebComponent`, following classes extend this class
* `categories_menu.py` - class `CategoriesMenu` - category side bar abstraction
* `image_gallerry.py` - class `ImageGallery` - image gallery abstraction
* `pagination.py` - class `Pagination` - pagination part of the HTML page abstraction
* `title_bar.py` - class `TitleBar` - title bar part of the HTML page abstraction

##### Page objects
In directory `test_e2e/pages` there are modules with classes that implement
HTML pages abstraction - the whole HTML page (apart from common HTML components).
They also encapsulate all the Selenium code for that:
* `category_page.py` - class `CategoryPage` - abstraction of the category page
* `home_page.py` - class `HopePage` - abstraction of the home (categories) page
* `oops_page.py` - class `OopsPage` - abstraction of the error page
* `product_page.py` - class `ProductPage` - abstraction of the product page

##### Actual tests
In directory `test_e2e/tests` there are actual tests
* `test_category.py` - tests for checking content of the category page of the app
* `test_homepage.py` - tests for checking content of the home page of the app
* `test_navigation.py` - tests for checking navigation through the app in various ways
* `test_oops_page.py` - tests for checking the error page, namely 404 page
* `test_pagination.py` - tests that verify that pagination on the category page works
* `test_product.py` - tests for content and behaviour of the product page including image gallery

##### Screenshots
Screenshots from failed tests are stored in `screenshots` directory

### Source code documentation
Classes and their methods in the app and in tests are documented using reSt
Sphinx syntax - http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
