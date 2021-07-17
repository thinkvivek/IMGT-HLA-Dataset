from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os

full_path = os.path.realpath(__file__)
path, filename = os.path.split(full_path)

driver = webdriver.Chrome(executable_path= path + r"\chromedriver.exe")
driver.implicitly_wait(3)
driver.get('https://www.ebi.ac.uk/ipd/imgt/hla/align.html')

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
feat = soup.find_all(class_="text")

locus = 'B'
segment = 'exon2'
mismatches = 'Show All Bases'

driver.find_element_by_name('gene').send_keys(locus)
driver.find_element_by_xpath('//option[@value="'+segment+'"]').click()
driver.find_element_by_xpath('//option[@value="'+mismatches+'"]').click()
driver.find_element_by_xpath("""//*[@id="jd_submitButtonPanel"]/input""").send_keys(Keys.ENTER)

htmlSeq = driver.page_source
soupSeq = BeautifulSoup(htmlSeq, 'html.parser')

table = str(soupSeq.find("pre")).split('<br/>')

alleles = []
data = []

for st in table:
    st = st.replace('<pre class="normal">', '').replace('</pre>', '').replace(' ', '')
    if(len(st.split()) > 0):
        alleleName = st.split()[0]
        if (alleleName not in alleles) and alleleName != 'AACodon':
            alleles.append(alleleName)
        data.append(st)


final_list = ["AlleleName, Segment, Sequence"]

for allele in alleles:
    seq = ''
    for st in data:
        tempStr = st.split()
        if(allele == tempStr[0]):
            if seq != tempStr[1]:
                seq = seq + tempStr[1]
    final_list.append(allele + ',' + segment + ',' + seq)

file2 = open(path + r"\Output.txt","a")

for rec in final_list:
    file2.writelines(rec + "\n")

file2.close()