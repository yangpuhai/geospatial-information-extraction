# geospatial-information-extraction


1.Folder1 : extract geospatial information from web (Paper Code and data)
  
  File in the folder1
    
  1.1 Codes of address extraction module:

    (1) download_street_name.py : From the OpenStreetmap extract the street names, city name, state name and country name of the experimental areas.

    (2) open_web.py : The function access Google search engine.
    
    (3) address_extract.py : Based on the entered street dictionary, the address is extracted from the specified document.
    
    (4) acquire_addresses.py : A series of functions that extract addresses within a region.
    
    (5) address_main.py : The main function of extracting addresses in several areas.
    
  1.2 Codes of webpage classifier
  
    (1) acquire_training_data.py : Get training data of the webpage classifier.
    
    (2) url_feature_extract.py : Extracting features of URL.
    
    (3) web_page_prediction_model.py : Training classifier.
    
  1.3 Codes of place name extraction module:
  
    (1) open_webpage2.py : The functions access Google search engine and normal webpage.
    
    (2) tittles_to_tittle.py : Extract a corret place name from multiple potential place names.
    
    (3) address_find_tittle.py : The functions extract potential place names for one address in 50 and 10 titles based on different rules.
    
    (4) acquire_place_name.py : A series of functions that extract place names by addresses within a region.
    
    (5) place_name_main.py : The main function of extracting place names in several areas.
    
  1.4 Data files used in the experiment:
    
    (1) proxy_ip_address : The proxy ip that access the webpages, our experiment did not use it.
    
    (2) user_agents : The user agents that access the webpages.
    
    (3) google_domain : Google domain name used to access Google search engine.
    
    (4) types : The business types extracted from Google Maps.
    
    (5) street_type : Street types and their abbreviations,used to build street dictionaries..
    
    (6) filter_words : Filter the illegal names in the correct place names.
    
2.Folder2 : extract openstreetmap and wikimapia data (Download data for comparison.)
  
  File in the folder1
  
    (1) extract_openstreetmap_place_inf.py : Download data for comparison from OpenStreetMap.
    
    (2) extract_wikimapia_place_inf.py : Download data for comparison from Wikimapia.
    
3.Running steps:

  (1) download_street_name.py
  
  (2) address_main.py
  
  (3) acquire_training_data.py
  
  (4) web_page_prediction_model.py
  
  (5) place_name_main.py

  (6) extract_openstreetmap_place_inf.py
  
  (7) extract_wikimapia_place_inf.py
