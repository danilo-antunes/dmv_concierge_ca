from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import sys
zipcode = sys.argv[1]
qtd_of_people = sys.argv[2]
date_of_birth = sys.argv[3] #mmddyy format
license_number = sys.argv[4]
phone_number = sys.argv[5]
op = webdriver.ChromeOptions()
op.add_argument('headless')
driver = webdriver.Chrome(executable_path=r'C:\\Users\\Danilo_Antunes\\AppData\\Local\\Programs\\Python\\Python311\\chromedriver.exe', options=op)
#driver = webdriver.Chrome(executable_path=r'C:\\Users\\Danilo_Antunes\\AppData\\Local\\Programs\\Python\\Python311\\chromedriver.exe')
driver.get('https://www.dmv.ca.gov/portal/wp-json/dmv/v1/field-offices?q='+zipcode)
dado_cidade = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/pre'))).text
cidade = json.loads(dado_cidade)
office = cidade[0]['meta']['dmv_field_office_public_id']
driver.get('https://www.dmv.ca.gov/portal/wp-json/dmv/v1/appointment/branches/'+office+'/dates?services[]=DT!1857a62125c4425a24d85aceac6726cb8df3687d47b03b692e27bd8d17814&numberOfCustomers='+qtd_of_people)
dados_data=WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/pre'))).text
data_array = json.loads(dados_data)
date = data_array[0]
driver.get('https://www.dmv.ca.gov/portal/wp-json/dmv/v1/appointment/branches/'+office+'/times?date='+date+'&services[]=DT!1857a62125c4425a24d85aceac6726cb8df3687d47b03b692e27bd8d17814&numberOfCustomers='+qtd_of_people)
dado_horario = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/pre'))).text
horario_array = json.loads(dado_horario)
hour = horario_array[0]
import requests

url = "https://www.dmv.ca.gov/portal/wp-json/dmv/v1/appointment/hold-appointment"

data = {
  "numberItems": qtd_of_people,
  "officeId": office.split('!')[0],
  "requestDate": date,
  "requestTime": hour,
  "requestTask": "DT",
  "firstName": "hold",
  "lastName": "hold",
  "telNumber": phone_number,
  "token": "",
  "hasPrevPermit": "false",
  "dob": date_of_birth,
  "dlNumber": license_number
}
 
response = requests.post(url, json=data)
 
print("Status Code", response.status_code)
print("JSON Response ", response.json())

