import os
import requests

# Inputs- ------------------------------------------------------------------- #

last_hours = '48h'  # 24h ou 48h
type_file = 'json'  # csv ou json
region = 'brasil'  # brasil ou ams
local = os.getenv('FILES')

# Functions ------------------------------------------------------------------- #

def download_url(url, save_path, chunk_size=128):
    """Function to download files from a specific URL"""
    print("Downloading file to: " + save_path)
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        print("File was found, and downloading the file")
        with open(save_path, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=chunk_size):
                fd.write(chunk)
    else:
        print("File not found")


def validate_existing_file(save_path, file_name):
    for _, _, file in os.walk(save_path):
        if file_name in file:
            return False

    return True

# Main Function ------------------------------------------------------------------- #

def main(region, last_hours, type_file, path):
    url_region = 'https://queimadas.dgi.inpe.br/home/download?id=focos_'+region+'&time='+last_hours+'&outputFormat='+type_file+'&utm_source=landing-page&utm_medium=landing-page&utm_campaign=dados-abertos&utm_content=focos_'+region+'_'+last_hours+''
    file_name = 'focos_' + last_hours + '_' + region.lower() + '.' + type_file
    save_path = path + '/' + file_name

    is_file_available = False

    if validate_existing_file(save_path, file_name):
        download_url(url_region, save_path)
        print(f'Successfully saved file')
        is_file_available = True
    else:
        print(f"File {file_name} already exists")

    print('Removing temporary files')
    try:
        for file in os.listdir(local):
            if file.endswith(".zip") or file.endswith(".csv"):
                os.remove(local + "/" + file)
    except:
        pass


if __name__ == '__main__':
    main(region, last_hours, type_file, local)