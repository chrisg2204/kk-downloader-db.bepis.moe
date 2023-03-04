import shutil
import argparse

from fn.utils import remove_comma
from urllib.request import Request, urlopen
from pathlib import Path
from bs4 import BeautifulSoup

ap = argparse.ArgumentParser()
ap.add_argument('--index', type=int, default=0)
# 0, 100, 500, 1000
ap.add_argument('--downloads', type=int, default=0)
args = ap.parse_args()

domain = 'https://db.bepis.moe' 
site = '{}/koikatsu?page={}'.format(domain, args.index)
storage = './storage'
img_urls = []
card_names = []
counter = 0

print('Site: {}'.format(site))
req = Request(
    url=site, 
    headers={'User-Agent': 'Mozilla/5.0'}
)
page = urlopen(req).read()
soup = BeautifulSoup(page, 'html.parser')
downloadTag = 'Download count:'

for div in soup.findAll('div', {'class': ['logo', 'logo--hover-state']}):
	content = div.get('title').split('\n')
	for title in content:
		if downloadTag in title:
			tag = title.split(':')
			n_download = remove_comma(tag[1])
			if n_download >= args.downloads:
				card_names.append(content[-1])

for link in soup.findAll('a', {'class': ['btn', 'btn-primary', 'btn-sm']}):
	img_urls.append(link.get('href'))

for img_url in img_urls:
	if Path(img_url).name[:2] == 'KK':
		img_name = Path(img_url).name.split('.')
		if img_name[0] in card_names:
			print('Downloading file: {}'.format(domain+img_url))
			img_dest = storage + '/' + Path(img_url).name
			req_img = Request(
				url=domain+img_url, 
				headers={'User-Agent': 'Mozilla/5.0'}
			)

			with urlopen(req_img) as response, open(img_dest, 'wb') as out_file:
				shutil.copyfileobj(response, out_file)
				counter += 1

if counter >= 1:
	print("{} Files Downloaded!".format(counter))
