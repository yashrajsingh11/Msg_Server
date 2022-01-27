from operator import contains, imod
from flask import Flask, request, jsonify
import pickle
import numpy as np
import time
import re
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

app = Flask(__name__)

def get_hyperlinks(url):
  try:
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome("./chromedriver.exe", options = options)
    driver.get(url)
    time.sleep(5)
    total = driver.find_elements_by_tag_name("a") 
    driver.quit()
    return len(total)
  except Exception as ex:
    return 0

def get_pagerank(url):
  try:
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome("./chromedriver.exe", options = options)
    driver.get("https://checkpagerank.net/")
    tf = driver.find_element_by_name("name")
    tf.clear()
    tf.send_keys(url)
    driver.find_element_by_class_name("btn-primary").click()
    delay = 5 
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME , 'results')))
    resultTable = driver.find_element_by_class_name("results")
    resultTableContent = resultTable.get_attribute('innerHTML')
    driver.quit()
    return resultTableContent.split("/10")[0]
  except Exception as ex:
    return "qwerty"

def getDomainName(s):
  temp = s.split("/")[2]
  return temp

URL_REGEX = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]?\([^\s()]+\)[^\s()]?\)|\([^\s]+?\))+(?:\([^\s()]?\([^\s()]+\)[^\s()]?\)|\([^\s]+?\)|[^\s`!()\[\]{};:\'\".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""

def getFeatures(url) :
  featureList = []
  domainName = getDomainName(url)
  all_digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
  # 1) Length of URL
  featureList.append(len(url))
  # 2) Length of Domain Name
  featureList.append(len(domainName))
  # 3) ip
  pattern1 = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
  if pattern1.search(url) != None:
    featureList.append(1)
  else:
    featureList.append(0)
  # 4) nb_dots
  featureList.append(len(domainName.split(".")) - 1)
  # 5) nb_hyphens
  featureList.append(len(domainName.split("-")) - 1)
  # 6) nb_at
  featureList.append(len(url.split("@")) - 1)
  # 7) nb_slash
  featureList.append(len(url.split("/")) - 1)
  # 8) nb_www
  featureList.append(len(url.split("www")) - 1)
  # 9) nb_dslash
  count = len(url.split("//")) - 2
  if count > 0:
    featureList.append(1)
  else:
    featureList.append(0)
  # 10) http_in_path
  featureList.append(len(url.split("http")) - 2)
  # 11) https_token
  scheme = url.split("/")[0]
  if scheme == "http:":
    featureList.append(1)
  else:
    featureList.append(0)
  # 12) ratio_digits_url
  total_digits_url = 0
  for s in url:
    if s in all_digits:
        total_digits_url += 1
  featureList.append(round(total_digits_url / len(url), 9))
  # 13) ratio_digits_host
  total_digits_domain = 0
  for s in domainName:
    if s in all_digits:
        total_digits_domain += 1
  featureList.append(round(total_digits_domain / len(domainName), 9))
  # 14) nb_hyperlinks
  featureList.append(get_hyperlinks(url))
  #15) page_rank
  tempResult = get_pagerank(url)
  if tempResult[-1] not in all_digits:
    featureList.append(0)
  else:
    featureList.append(tempResult[-1])
  return featureList


filename = 'finalized_model.sav'
TFLITE_FILE_PATH = "model.tflite"
fieldnames = ['url','target']
@app.route('/add', methods=["POST"])
def add_tobase():
    input_json = request.get_json(force=True) 
    data = input_json['data']
    with open(r'kb.csv', 'a', newline='') as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
      writer.writerow(data)
      print("csvfile")
    return jsonify("Done")


@app.route('/api', methods=["POST"])
def hello_world():
    input_json = request.get_json(force=True) 
    data = input_json['data']
    urls_list = []
    for i in data:
      try:
        urls_list.append(re.findall(URL_REGEX,i)[0])
      except:
        pass
    tmp_url = []
    for url in urls_list:
        if 'http' in url or 'https' in url:
            tmp_url.append(url)
        else:
            tmp_url.append('http://'+url)
    loaded_model = pickle.load(open(filename, 'rb'))
    answer = []
    try:
        for i,url in enumerate(tmp_url):
            k = {}
            tmp = np.array(getFeatures(url))
            ans = loaded_model.predict(tmp.reshape(1,-1))
            k["url"] =  data[i]
            k["result"] = ans.tolist()[0] + 0.0
            print(k)
            answer.append(k)
        return jsonify({"prediction":answer})
    except Exception as e:
      print(e)
      return jsonify({"prediction":[]})
      



if __name__ == '__main__':
    app.run(port=4000,debug=True,host="0.0.0.0")