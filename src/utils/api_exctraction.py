def get_info():
    # Import Libraries
    import requests, json, os, sys, time
    import pandas as pd
    from datetime import datetime

    '''
    Preparing folder variables.
    '''
    os.chdir(os.path.dirname(sys.path[0])) # This command makes the notebook the main path and can work in cascade.
    main_folder = sys.path[0]
    data_folder = (main_folder + "\data")

    '''
    Creating time variables.
    '''
    current_time = time.strftime("%H_%M_%S",time.localtime())
    date = datetime.now()
    actual_date = date.strftime("%Y_%m_%d")


    #Remove the limit to see the df
    pd.set_option('display.max_columns', None)

    #Creating the necessary lists
    anime_list = []
    missing_requests_list = []
    resource_does_not_exist = []

    '''
    To check if there is an empty value. If the category is empty, it returns None.
    '''
    def try_it(i):
        try:
            return i["name"]
        except:
            return None

    '''
    Def with a try check to get the finishing time of an anime, in case the anime is a movie, then it returns the release time.
    If the anime is not a movie, it checks for the finishing time. If there is no finishing time, it returns None 
    '''

    url = "https://api.jikan.moe/v4/anime" # url of the api

    r = requests.get(url)# request to a web page (url)    
    
    data = r.json() # creating a variable for all the info we get

    n_pages = data['pagination']['last_visible_page']
    #for page in range (1,n_pages +1):
    for page in range (1,2):
        r_page = requests.get(url + '?page=' + str(page)) # request to a web page (url)
        content = r_page.json()
        print (page)
        data = content["data"]
        time.sleep(1)
        for char in data: #Already 1 to 13000 of 25850 #Loop to go thru a range of chosen numbers
            #time.sleep(1)
            try: # First try yo check if the page exist or not
                # Creation of the necessary dictionary o store the values in each loop # We specify which information to get in each Item
                anime_dict = {"Cover" : char["images"]["jpg"]["large_image_url"] if char["images"]["jpg"]["large_image_url"]  else None,
                            "English_Title" : char["title"] if char["title"]  else None,
                            "Japanses_Title" : char["title_japanese"] if char["title_japanese"]  else None,
                            "Type" : char["type"] if char["type"]  else None,
                            "Source" : char["source"] if char["status"] else None,
                            "Audience" : [try_it(i) for i in char["demographics"]], # List comprehension calling the Def try_it
                            "N_Episodes" : (int(char["episodes"])) if char["episodes"] else 0,
                            "Duration" : char["duration"] if char["duration"]  else None,
                            "Rating" : char["rating"] if char["rating"] else None,
                            "Score" : char["score"] if char["score"]  else None,
                            "Scored_by" : char["scored_by"] if char["scored_by"]  else None,
                            "Rank" : (int(char["rank"])) if char["rank"] else None,
                            "Season" : char["season"] if char["season"] else None,
                            "Genre" : [try_it(i) for i in char["genres"]],# List comprehension calling the Def try_it
                            "Theme" : [try_it(i) for i in char["themes"]],# List comprehension calling the Def try_it
                            "Released" : (int(char["aired"]["prop"]["from"]["year"])) if char["aired"]["prop"]["from"]["year"] else None, # If else in one line
                            "Studios" : [try_it(i) for i in char["studios"]],# List comprehension calling the Def try_it
                            "Producers" : [try_it(i) for i in char["producers"]]# List comprehension calling the Def try_it
                            }
                            
                anime_list.append(anime_dict) # Append the loop info to anime_list
                #time.sleep(1) # we use here a time sleep cuz if we are to fast asking for information, the server might block us
            # Ending of the first try specifying the error
            except:
                if r_page.status_code == 429: #If there is a 429 error we show it on screen and tell us the respuesta.reason
                    missing_requests_list.append(id)
                    print (f"El código de estado de la petición es: {r_page.status_code}. Estatus {r_page.reason}. No se puede recoger información de la página {id}\n")
                else:
                    resource_does_not_exist.append(id) #If there is a any other error we show it on screen and tell us the respuesta.reason
                    print (f"El código de estado de la petición es: {r_page.status_code}. Estatus {r_page.reason}. No se puede recoger información de la página {id}\n")
                continue

    # We create df from anime_list and save it in a csv file adding actual date and time variables to the name
    anime_df = pd.DataFrame(anime_list)
    anime_csv = os.path.join(data_folder,"anime_" + actual_date+ "_" +current_time + ".csv")# Saving the image to the images folder
    anime_df.to_csv(anime_csv, sep = ';', index = False)
    print(f'anime_{actual_date}{current_time}.csv created\n\n')