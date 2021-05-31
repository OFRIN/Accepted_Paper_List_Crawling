
import urllib.request

conference_dict = {
    "AAAI2019":{
        "type" : "pdf",
        "url" : "https://aaai.org/Conferences/AAAI-19/wp-content/uploads/2018/11/AAAI-19_Accepted_Papers.pdf"
    },
    "AAAI2020":{
        "type" : "pdf",
        "url" : "https://aaai.org/Conferences/AAAI-20/wp-content/uploads/2020/01/AAAI-20-Accepted-Paper-List.pdf"
    },
    "AAAI2021":{
        "type" : "pdf",
        "url" : "https://aaai.org/Conferences/AAAI-21/wp-content/uploads/2020/12/AAAI-21_Accepted-Paper-List.Main_.Technical.Track_.pdf"
    }
}

def download_file_using_url(url, file_path):
    urllib.request.urlretrieve(url, file_path)

for key in conference_dict.keys():
    download_file_using_url(conference_dict[key]['url'], f'./data/{key}.pdf')