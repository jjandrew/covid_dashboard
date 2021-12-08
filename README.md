#Documentation for covid_dashboard

## Description
This application provides up to date Covid data and news articles to a user with the ability to 
schedule updates for the future.
The Covid data and news articles returned can be edited within the config.json file.


## Code Modules:

###user_interface.py
####Description
- This is the main module which will deal with flask and the flow of the program.

####Functions
**check_updated_config**()
- This function will be scheduled to check if config file has been updated.

  Will schedule itself every 5 minutes.

**event_update**(title: str, content: str, to_update: str, repeat: bool, test=False)
- This procedure will add an event to the scheduled_events array.

  This will be added to the left-hand side of the webpage.
    
  :param test: Checks whether test case is to be used (default false).
    
  :param repeat: Whether the event is to be repeated.
    
  :param to_update: What is to be updated.
    
  :param title: Title of the event.
    
  :param content: Content displayed under the title.
    
  :return: Only used in testing.
    
**remove_event**(title: str)
- Will remove event with the title provided from scheduled_events.

  :param title: the title of the event to be removed.

**event_exists**(title: str, test=False) -> bool
- Will cycle through events with the title provided from scheduled_events.
    
  :param test: Checks whether test case is to be user (Default false).
    
  :param title: the title of the event to be removed.
    
  :return True if event present otherwise False.

**remove_news_from_home**()  
- Changes articles when news has been removed so that the display can be updated.

**add_update**(repeat, data_to_update, news_to_update,
               label_name: str, scheduler_time: str) -> bool
- Will update both schedulers if both news and covid data are to be updated.

  Will also deal if only one is to updated or neither.
    
  :param repeat: Whether the event is to be repeated every 24 hours: Bool
    
  :param data_to_update: Whether the covid data is to be updated: Bool
    
  :param news_to_update: Whether the news is to be updated: Bool
    
  :param label_name: The name of the event to be added.
    
  :param scheduler_time: The time the event is to be added.
    
  :return: Return value to be used in testing.

**index**()
- The function that is called when directing to the /index part of the webpage.
    
  This is the main homescreen of the webpage and will be refreshed every minute.

  This procedure checks if an action has been carried out on the webpage.
    
  This procedure also sets the values for events, news, covid data and images.

  :return: The template for the webpage.
    


####Global Variables
**articles**: list
- articles to be displayed in the user interface.

**scheduled_events**: list
- List of scheduled events.

**app**
- The flask project to be run.

**location**
- City location in the config file.

**nation_location**
- Nation described in the config file.

**image_name**
- Name of the image in the config file.

###covid_data_handler.py
#### Description
- This Module processes the data received in the 'nation_2021-10-28.csv' file.
Module also receives information from the public health England API.

#### Functions:
**parse_csv_data**(csv_filename: str) -> list
- This function will read from the 'nation_2021-10-28' file and return a list of strings
    corresponding to each line of the csv file.

    :param csv_filename: Name of file to be parsed.

    :return: List[str] of each line of the csv file.

**process_covid_csv_data**(covid_csv_data: list) -> tuple
- Takes in csv data file as input and calculates:
        Cases for last week excluding most recent value as it is incomplete, 
Hospital cases, Cumulative Deaths as up to date as file allows.

  :param covid_csv_data: Data passed in from parsing function.

  :return: weekly cases, hospital cases, cumulative deaths as integers or Error if error reading.

**covid_API_request**(location="Exeter", location_type="ltla") -> dict
- Retrieves COVID data from the public health England API.

  Will be able to search based on the location and location_type passed in as parameters.
    
  :param location: location to be searched for in API.
    
  :param location_type: type of entry location is.
    
  :return: Data returned from PHE API in json format.

**process_covid_API**(covid_json: dict) -> tuple
- Retrieves weekly cases, hospital cases and total deaths from the json.

  :param covid_json: Data retrieved from the API call.
    
  :return: weekly cases, hospital cases, total deaths.

**schedule_covid_updates**(update_interval: int, update_name: str) -> str
- Will carry out the event denoted by update_name after the interval shown by update_interval.

  :param update_interval: Time of the update.
    
  :param update_name: Name of the update.

  :return: test if test case is passed in.

**update_covid_data**(update_name: str, repeat=False) -> str
- The function called by the scheduler to print the covid data from the API.

  :param update_name: Name of the update to be carried out.
    
  :param repeat: Whether the update is to be repeated.
      
  :return: Test statement for use in testing.

**get_starting_data**(test="")
- Function to retrieve the starting values for the user interface.
    
  :return: Test statement for use if test case is passed in.


### covid_news_handling.py

#### Description
- This module receives articles from the newsapi.
It has two functions one for calling API and one for processing the responses.

#### Functions
**news_API_request**(covid_terms="Covid COVID-19 coronavirus") -> list
- Takes in terms to be searched in the API as a string separated by spaces and
    returns an array of the responses received from the various API calls.

  :param covid_terms: Takes in a string separated by spaces of terms to be searched for in the API.
    
  :return: Array of the responses received from the various API calls.

**update_news**(test=None) -> list
- Retrieves api responses and loops through the articles in each of the
    responses appending each article to an array.
    
    :return: articles returned from the various API calls or empty array if no key provided.

**update_removed_news**(title: str) -> str
- This function will add a removed event to an array, so it isn't searched for again.

  :param title: The title of the event that is to not be searched for again.
    
  :return: Title for use in testing to make sure procedure ran.

**schedule_news_updates**(update_interval: int, update_name: str) -> str
- Will carry out the event denoted by update_name after the interval shown by update_interval.

  :param update_interval: Time of the update.

  :param update_name: Name of the update.
    
  :return: test if test case has been passed in.

**news_update**(update_name: str, repeat=False, test=False) -> list
- The function called by the scheduler to print the response from news API.

  :param test: Checks if test case is to be passed in (default False).
    
  :param update_name: Name of the update to be carried out.
    
  :param repeat: Whether the event is to be repeated.
    
  :return: Used when test case is passed in to make sure program exists.


#### Global Variables
**removed**
- A list of articles that have been removed from search.


### decode_config.py
####Description
- This module will be used to check that the config file is valid and then return values.

####Functions
**decode_config**(file_name='config.json') -> tuple:
- This function reads from the config.json file and will return suitable values.

  :return: Relevant values retrieved from the json file.


### time_conversions.py
####Description
- Time conversions for use with the scheduler.

####Functions
**time_difference**(scheduled_time: str):
- Will calculate difference between current time and scheduled time in seconds.

  :param scheduled_time: Time passed in url query.

  :return: Difference between times in seconds or None if invalid entry.

###shared_data.py
####Description
- This module will store the general data and functions that need to be accessed by all modules.

####Functions
**get_scheduler**()
- Will return the scheduler to the user_interface.

  :return: scheduler
    
**update_scheduler**(updated_s)
- Will update the scheduler stored in the module.

  :param updated_s: Scheduler to be passed in.

**get_covid_values**() -> tuple
- Will return the covid_values to the user interface.

  :return: local weekly figures, national weekly figures,
  national hospital figures, national total deaths as a tuple.

**set_covid_values**(local_figs, national_week_figs, national_hospital_figs, national_deaths)
- Will set the values for data that needs to be accessed by the user interface.

  :param local_figs: local weekly figures may be int or string.
    
  :param national_week_figs: national weekly figures may be int or string.
    
  :param national_hospital_figs: national hospital cases may be int or string.
    
  :param national_deaths: total number of national deaths may be int or string.

**get_news_articles**() -> list
- Function for providing user interface with the stored articles.

  :return: Articles

**set_news_articles**(news_articles: list)
- Will set the news articles to be accessed by the user interface.

  :param news_articles: articles to be set.

**get_scheduled_events**() -> list
- This function will return scheduled events for use in all modules.

  :return: Scheduled events.

**set_scheduled_events**(events: list)
- Will set scheduled events for use in all modules.

  :param events: Scheduled events.
    
####Global Variables
**scheduler**
- The scheduler to be used within multiple aspects of the program.

**local_week_figs**
- Weekly Covid figures in the local area.

**national_week_figs**
- Weekly Covid figures nationally.

**nation_hospital_figs**
- Total number of hospital cases nationally.

**nation_deaths**
- Total number of deaths due to Covid nationally.

**articles**: list
- News articles to be displayed in the user interface.

**scheduled_events**: list
- Events that are scheduled to occur.


###runtime_tests.py
####Description
- Module containing the tests to be carried out during runtime.

####Functions
**test_covid_API_request**()
- Tests covid_API_request function can make a request and return a dictionary.

**test_schedule_covid_updates**()
- Tests updates on covid data can be scheduled.

**test_update_covid_data**()
- Tests no scheduled events are present when test is passed in.

**test_decode_config**()
- Tests config file can be decoded and tests it can be decoded if file is edited.

**test_news_API_request**()
- Tests API request can be made.

  Tests default values are used.
    
  Tests different terms can be used.

**test_update_news**()
- Tests update_news returns a value.

**test_schedule_news_updates**()
- Tests updates for the news can be scheduled.

**test_get_scheduler**()
- Tests that a scheduler is returned.

**test_update_scheduler**()
- Tests that the scheduler can be updated and then retrieved.

**test_get_news_articles**()
- Tests news articles are returned as a list.

**test_get_scheduled_events**()
- Tests get_scheduled_events returns a list.

**test_set_scheduled_events**()
- Tests scheduled events can be set and then retrieved.

**run_tests**()
- This procedure will execute all the runtime tests.

  It will then schedule itself again for an 15 minutes time.

**schedule_tests**()
- Schedules runtime tests to be carried out.
    


##Test Modules

###Description
The modules to be used with pytest as unit tests for the program.

###test_covid_data_handler.py
####Description
Tests for covid_data_handler to run using pytest.

####Functions
**test_parse_csv_data**()
- Tests the parse_csv_data function returns the correct values.

**test_process_covid_csv_data**()
- Tests the process_covid_csv_data function can handle information correctly and deal with errors.

**test_covid_API_request**()
- Tests covid_API_request function can make a request and return a dictionary.

**test_process_covid_API**()
- Tests the process_covid_API function can deal with empty arguments.

  Also checks it can deal with an argument of incorrect form.

**test_schedule_covid_updates**()
- Tests updates on covid data can be scheduled.

**test_update_covid_data**()
- Tests no scheduled events are present when test is passed in.
 
**test_get_starting_data**()
- Tests the correct starting data is returned even when API calls are not possible.

###test_decode_config.py
####Description
- Tests for decode_config module to run using Pytest.

####Functions
**test_decode_config**()
- Tests config file can be decoded and tests it can be decoded if file is edited.

###test_news_data_handling.py
####Description
- Tests for the news_data_handling module to run using Pytest.

####Functions
**test_news_API_request**()
- Tests API request can be made.

  Tests default values are used.

  Tests different terms can be used.

**test_update_news**()
- Tests update_news returns a value.

**test_update_removed_news**()
- Tests an article can be removed from future news searches.

**test_schedule_news_updates**()
- Tests updates for the news can be scheduled.

**test_news_update**()
- Tests news_update returns an array.


###test_shared_data.py
####Description
- Tests for the shared_data module to be run using Pytest.

####Functions
**test_get_scheduler**()
- Tests that a scheduler is returned.

**test_update_scheduler**()
- Tests that the scheduler can be updated and then retrieved.

**test_get_covid_values**()
- Tests that 4 covid values are returned when get_covid_values is called.

**test_set_covid_values**()
- Tests covid_values can be set and then retrieved.

**test_get_news_articles**()
- Tests news articles are returned as a list.

**test_set_news_articles**()
- Tests news articles can be set and then retrieved.

**test_get_scheduled_events**()
- Tests get_scheduled_events returns a list.

**test_set_scheduled_events**()
- Tests scheduled events can be set and then retrieved.


###test_time_conversions.py
####Description
- Tests for the time_conversions module to be run using Pytest.

####Functions
**test_time_difference**()
- Tests invalid entries to time_difference function return None.


###test_user_interface.py
####Description
- Unit Tests for the user_interface part of the application to be run using Pytest.

####Functions
**test_event_update**()
- Tests events can be updated and are returned in the correct format.

**test_event_exists**()
- Tests it is possible to check whether an event is present in scheduled events.

**test_add_update**()
- Tests that it is not possible to add updates with invalid entries.



##Other Files:

###logging_file.log
####Description
- This file will store any errors or warnings that are thrown up during the running.
of the program.

###test.json
####Description
- A json file with invalid inputs for use during runtime testing.

###empty.json
####Description
- An empty json file that is used during testing.

###templates/index.html
####Description
- The html file used by flask for the creation of the application.

###static/images
####Description
- Directory used by flask when searching for images. covid_image.jpeg is placed in here as default
  image for the webpage.

    