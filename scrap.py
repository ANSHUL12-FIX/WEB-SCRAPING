import requests
from bs4 import BeautifulSoup
import pandas

tripadvisor_url = "https://www.tripadvisor.in/Hotels-g297687-Dehradun_Dehradun_District_Uttarakhand-Hotels.html/?pages="
page_num_MAX = 3
scriped_info_list = []

for page_num in range(1, page_num_MAX):
    req = requests.get(tripadvisor_url + str(page_num))
    content = req.content

    soup = BeautifulSoup(content, "html.parser")

    all_hotels = soup.find_all("div", {"class": "listItem"})
    

    for hotel in all_hotels:
        hotel_dict = {}
        hotel_dict["name"] = hotel.find("div", {"class": "listing_title"}).text
        hotel_dict["location"] = hotel.find("div", {"class": "react-container"}).text
        try:
            hotel_dict["price"] = hotel.find("div", {"class": "price-wrap"}).text
        except AttributeError:
            pass  
            
        hotel_dict["reviews"] = hotel.find("div", {"class": "prw_rup prw_common_rating_and_review_count_with_popup linespace is-shown-at-mobile"}).text
        
        hotel_dict["wifi_parking"] = hotel.find("span", {"class": "text_container"}).text
        
        scriped_info_list.append(hotel_dict)
    
        # print(hotel_name, hotel_location, hotel_price, hotel_reviews, hotel_wifi_parking)
dataFrame = pandas.DataFrame(scriped_info_list)
dataFrame.to_csv("trip.csv")
