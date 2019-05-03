from bs4 import BeautifulSoup
from manhuagui.constant import MANHUAGUI_URL
import requests
import execjs
import re
import json


NEWEST_INDEX = '31409'
MANHUAGUI_CONFIG = 'manhuagui_config.json'


class Crawler:
    def __init__(self):
        self.__session = requests.Session()

    def chapter(self, url):
        """
        {
            'referer': string,
            'pictures': list
            [
                url: string,
                ...
            ],
            'params': dict
            {
                'cid': string,
                'md5': string
            },
            'cname': string, chapter title,
            'bname': string, book name
        }
        """

        result = {
            'referer': url,
            'pictures': list()
        }

        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

        LZjs = r'''var LZString=(function(){var f=String.fromCharCode;var keyStrBase64="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";var baseReverseDic={};function getBaseValue(alphabet,character){if(!baseReverseDic[alphabet]){baseReverseDic[alphabet]={};for(var i=0;i<alphabet.length;i++){baseReverseDic[alphabet][alphabet.charAt(i)]=i}}return baseReverseDic[alphabet][character]}var LZString={decompressFromBase64:function(input){if(input==null)return"";if(input=="")return null;return LZString._0(input.length,32,function(index){return getBaseValue(keyStrBase64,input.charAt(index))})},_0:function(length,resetValue,getNextValue){var dictionary=[],next,enlargeIn=4,dictSize=4,numBits=3,entry="",result=[],i,w,bits,resb,maxpower,power,c,data={val:getNextValue(0),position:resetValue,index:1};for(i=0;i<3;i+=1){dictionary[i]=i}bits=0;maxpower=Math.pow(2,2);power=1;while(power!=maxpower){resb=data.val&data.position;data.position>>=1;if(data.position==0){data.position=resetValue;data.val=getNextValue(data.index++)}bits|=(resb>0?1:0)*power;power<<=1}switch(next=bits){case 0:bits=0;maxpower=Math.pow(2,8);power=1;while(power!=maxpower){resb=data.val&data.position;data.position>>=1;if(data.position==0){data.position=resetValue;data.val=getNextValue(data.index++)}bits|=(resb>0?1:0)*power;power<<=1}c=f(bits);break;case 1:bits=0;maxpower=Math.pow(2,16);power=1;while(power!=maxpower){resb=data.val&data.position;data.position>>=1;if(data.position==0){data.position=resetValue;data.val=getNextValue(data.index++)}bits|=(resb>0?1:0)*power;power<<=1}c=f(bits);break;case 2:return""}dictionary[3]=c;w=c;result.push(c);while(true){if(data.index>length){return""}bits=0;maxpower=Math.pow(2,numBits);power=1;while(power!=maxpower){resb=data.val&data.position;data.position>>=1;if(data.position==0){data.position=resetValue;data.val=getNextValue(data.index++)}bits|=(resb>0?1:0)*power;power<<=1}switch(c=bits){case 0:bits=0;maxpower=Math.pow(2,8);power=1;while(power!=maxpower){resb=data.val&data.position;data.position>>=1;if(data.position==0){data.position=resetValue;data.val=getNextValue(data.index++)}bits|=(resb>0?1:0)*power;power<<=1}dictionary[dictSize++]=f(bits);c=dictSize-1;enlargeIn--;break;case 1:bits=0;maxpower=Math.pow(2,16);power=1;while(power!=maxpower){resb=data.val&data.position;data.position>>=1;if(data.position==0){data.position=resetValue;data.val=getNextValue(data.index++)}bits|=(resb>0?1:0)*power;power<<=1}dictionary[dictSize++]=f(bits);c=dictSize-1;enlargeIn--;break;case 2:return result.join('')}if(enlargeIn==0){enlargeIn=Math.pow(2,numBits);numBits++}if(dictionary[c]){entry=dictionary[c]}else{if(c===dictSize){entry=w+w.charAt(0)}else{return null}}result.push(entry);dictionary[dictSize++]=w+entry.charAt(0);enlargeIn--;w=entry;if(enlargeIn==0){enlargeIn=Math.pow(2,numBits);numBits++}}}};return LZString})();String.prototype.splic=function(f){return LZString.decompressFromBase64(this).split(f)};'''

        response = self.__session.get(url, headers=headers)
        if response.status_code != requests.codes.ok:
            print('[Error] status code: ' + str(response.status_code))
            return

        soup = BeautifulSoup(response.text, 'lxml')
        scripts = soup.find_all('script', type='text/javascript')
        script = ''
        for s in scripts:
            if len(s.text) > 0:
                r = re.search("window\[\"[\w\W]+\"\]\(([\w\W]+)\)", s.text)
                if r:
                    script = r.group(1)
                    break

        info = execjs.compile(LZjs).eval(script)

        r = re.search("SMH\.imgData\(([\w\W]+)\)\.preInit\(\);", str(info))
        if not r:
            print('[Error] cannot execute javascript')
            return None

        info = json.loads(r.group(1))

        headers['Referer'] = result['referer']

        result['params'] = {
            'cid': str(info['cid']),
            'md5': str(info['sl']['md5'])
        }
        result['cname'] = info['cname']
        result['bname'] = info['bname']

        server = 'i.hamreus.com'

        for f in info['files']:
            result['pictures'].append('https://' + server + info['path'] + f)

        return result

    def album(self, url):
        """
        {
            'url': string,
            'index': int,
            'book-title': string,
            'comics': list
            {
                id: string:
                {
                    [chapter title: string, url: string]
                },
                ...
            }
        }
        """

        data = dict()

        data['url'] = url
        data['index'] = int(re.search("https://www\.manhuagui\.com/comic/([\d]+)/*", url).group(1))
        response = self.__session.get(url)
        if response.status_code != requests.codes.ok:
            print('[Error] status code: ' + str(response.status_code))
            return None

        soup = BeautifulSoup(response.text, 'lxml')

        book_title = soup.find('div', class_='book-title')
        data['book-title'] = book_title.text

        data['comics'] = dict()

        tags_li = soup.find_all('li')
        for li in tags_li:
            a = li.find('a', href=True, class_='status0')
            if not a:
                continue

            r = re.search("/comic/\d+/(\d+)\.html", a['href'])
            if not r:
                continue

            data['comics'][r.group(1)] = [a['title'], MANHUAGUI_URL + a['href']]

        return data
