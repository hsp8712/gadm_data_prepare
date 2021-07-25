import requests
import os
import shutil
from lxml import etree


def get_all_countries():
    url = "https://gadm.org/download_country_v3.html"
    r = requests.get(url)
    r.raise_for_status()
    dom = etree.HTML(r.text)
    options = dom.xpath("//*[@id=\"countrySelect\"]/option/@value")

    countries = []
    for c in options:
        if len(c) == 0:
            continue
        parts = c.split('_')
        code = parts[0]
        name = parts[1]
        num_of_level = int(parts[2])
        country = (code, name, num_of_level)
        countries.append(country)
    return countries


def download(url, local_dir):
    filename = url.split('/')[-1]

    target_dir = local_dir
    if not target_dir.endswith(os.sep):
        target_dir = target_dir + os.sep

    local_filename = target_dir + filename
    print("download start, url: {0}, local_filename: {1}".format(url, local_filename))
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    return local_filename


shp_url_template = "https://biogeo.ucdavis.edu/data/gadm3.6/shp/gadm36_{0}_shp.zip"


def download_all_shps(local_dir):
    all_countries = get_all_countries()
    print("Total countries: {0}".format(len(all_countries)))
    print(all_countries)
    for c in all_countries:
        country_code = c[0]
        shp_url = shp_url_template.format(country_code)
        download(shp_url, local_dir)
        print("{0} done".format(c))


if __name__ == "__main__":
    # execute only if run as a script
    local_dir = "C:\\Users\\hsp87\\Desktop\\test"
    download_all_shps(local_dir)
