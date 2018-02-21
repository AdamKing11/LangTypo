import os, sys, re, csv
from bs4 import BeautifulSoup
import requests, time
from tqdm import tqdm
url = 'http://web.phonetik.uni-frankfurt.de/S/S00002.html'

def get_phoneme_and_description(url):
	req  = requests.get(url)
	soup = BeautifulSoup(req.text, 'html.parser')

	tds = soup.find_all('td')
	# if we don't find anything
	if len(tds) == 0:
		return None

	td_regex = re.compile(r'</?td>')
	phoneme = td_regex.sub('', str(tds[1]))
	phoneme = re.sub(r'&lt;', '<', phoneme)
	description = td_regex.sub('', str(tds[3]))

	return phoneme, description

def main():
	ps_and_ds = []
	base_url = 'http://web.phonetik.uni-frankfurt.de/S/S{0}.html'
	with open('upsid_descs.txt', 'w') as wf:
		writer = csv.writer(wf, delimiter = '\t', quotechar = None)
		writer.writerow(['phoneme', 'description'])
		
		for i in tqdm(range(919)):
			i_str = str(i)
			while len(i_str) < 4:
				i_str = '0' + i_str
			url = base_url.format(i_str)
		
			p_and_d = get_phoneme_and_description(url)
			if p_and_d:
				#print(i, len(ps_and_ds))
				ps_and_ds.append(p_and_d)
				writer.writerow(p_and_d)

				time.sleep(.25)
	return ps_and_ds
		
	
if __name__ == '__main__':
	main()
