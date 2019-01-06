import requests

def content(key):
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    }
    res = requests.get('https://www.baidu.com/s?ie=UTF-8&wd={}'.format(key),headers=headers).text
    return res
if __name__ == '__main__':
    content('python')

