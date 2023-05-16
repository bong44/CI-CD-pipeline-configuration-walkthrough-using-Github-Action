import requests
from bs4 import BeautifulSoup
import json

url = 'https://bus.koreacharts.com/intercity-bus-terminal.html'

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

num = 10000

# 크롤링 결과를 저장할 딕셔너리
bus_info_dict = {}

# 첫 번째 <ul> 안의 <a> 태그 크롤링
first_ul = soup.find('ul', class_='list-unstyled')
first_links = first_ul.find_all('a')
iteratorNum = len(first_links)
iteratorNumChk = 0;
for link in first_links:
    key = link.text.strip() # ex. 간성
    value_dict = {} # ex. 간성 : {}

    # 두 번째 <ul> 안의 <a> 태그 크롤링
    second_url = "https://bus.koreacharts.com" +link.get('href')
    second_response = requests.get(second_url)
    second_soup = BeautifulSoup(second_response.content, 'html.parser')

    second_ul = second_soup.find('ul', class_='list-unstyled')
    second_links = second_ul.find_all('a')
    second_value_dict = {} # ex. 동서울 : {}
    for second_link in second_links:
        second_key = second_link.text.strip() # ex. 간성 - 동서울

        # <table> 안의 정보 크롤링
        third_url = "https://bus.koreacharts.com" + second_link.get('href')
        third_response = requests.get(third_url)
        third_soup = BeautifulSoup(third_response.content, 'html.parser')

        table = third_soup.find('table', class_='table table-striped table-bordered dt-responsive nowrap')
        tbody = table.find('tbody')
        rows = tbody.find_all('tr')

        third_value_dict = []

        for row in rows:
            cols = row.find_all('td')
            bus_id = num
            departure_time = cols[0].text.strip()
            arrival_time = cols[1].text.strip()
            bus_grade = cols[2].text.strip()
            cost = cols[3].text.strip()
            num += 1
            iteratorNumChk += 1

            # 정보를 딕셔너리에 저장
            
            third_value_dict.append({       'bus_id' : bus_id,
                                            'departure_time': departure_time,
                                           'arrival_time': arrival_time,
                                           'bus_grade': bus_grade,
                                           'cost': cost})

        # 두 번째 딕셔너리에 저장
        second_value_dict[second_key] = third_value_dict

    bus_info_dict[key] = second_value_dict
    # bus_info_dict.append(value_dict)
    # print("now crowlled data length .."+str(len(bus_info_dict))+" _ : "+str(num))
    # print(bus_info_dict)
    print("%.2f%%" % (iteratorNumChk / iteratorNum * 100.0))

    # # 첫 번째 딕셔너리에 저장
    # bus_info_dict[key] = value_dict

# 결과 출력
print(bus_info_dict)

filename = "test.json"

with open(filename, 'w', encoding='utf-8') as f:
    json.dump(bus_info_dict, f, ensure_ascii=False)