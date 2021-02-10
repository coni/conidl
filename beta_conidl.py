# coding: utf-8
import re
import json
import urllib, http.cookiejar
from jsinterp import JSInterpreter
import requests
import os

def extract_json_objects(text, decoder=json.JSONDecoder()):
        pos = 0
        while True:
            match = text.find('{', pos)
            if match == -1:
                break
            try:
                result, index = decoder.raw_decode(text[match:])
                yield result
                pos = match + index
            except ValueError:
                pos = match + 1

def _parse_sig_js(jscode):
        for i in jscode.splitlines():
            if '=function(a){a=a.split("")' in i:
                if len(i.split("=")[0]) == 2:
                    funcname = i.split("=")[0]
        jsi = JSInterpreter(jscode)
        initial_function = jsi.extract_function(funcname)
        return lambda s: initial_function([s])

class conidl:

    def get_video_link(self, url):
        html_file = self.make_get(url)

        s = None

        for dictionnaire in extract_json_objects(html_file):
            if "INNERTUBE_CONTEXT" in dictionnaire:
                for i in dictionnaire["INNERTUBE_CONTEXT"]:
                    print(i)
            print("next dict")
            input()

            if "streamingData" in dictionnaire:
                for video_information in dictionnaire["streamingData"]["adaptiveFormats"]:
                    if video_information["itag"] == 140:
                        if "signatureCipher" in video_information:

                            for k in video_information["signatureCipher"].split("&"):
                                if "url=" in k:
                                    url = urllib.parse.unquote(k.split("url=")[1])
                                elif "s=" in k:
                                    s = urllib.parse.unquote(k.split("s=")[1])
                                elif "sp=" in k:
                                    sp = k.split("sp=")[1]
                        else:
                            url = urllib.parse.unquote(video_information["url"])
            
            if "CLIENT_CANARY_STATE" in dictionnaire:
                for j in dictionnaire["WEB_PLAYER_CONTEXT_CONFIGS"]["WEB_PLAYER_CONTEXT_CONFIG_ID_KEVLAR_WATCH"]:
                    js_url = dictionnaire["WEB_PLAYER_CONTEXT_CONFIGS"]["WEB_PLAYER_CONTEXT_CONFIG_ID_KEVLAR_WATCH"]["jsUrl"]
            
            if "videoDetails" in dictionnaire:
                for j in dictionnaire["videoDetails"]:
                    title = dictionnaire["videoDetails"]["title"]

        if s != None:
            player_url = "https://www.youtube.com/%s" % js_url
            code = self.make_get(player_url)
            
            res = _parse_sig_js(code)
            finalsig = res(s)

            url = url + "&%s=%s&ratebypass=yes" % (sp, finalsig)
        
        return url

    def crawling_dictionnary(self, dictionnaire, words, layer=0):
        # essaye de convertir un autre type qu'une liste en String et de le mettre dans une liste
        if type(words) != list:
            try:
                word = words
                words = [str(word)]
            except:
                print("ERREUR: Impossible to convert to String")
                exit()

        final_dict = {}
        child_dictionnary = None

        for word in words:
            final_dict[word] = []

        if type(dictionnaire) == dict:
            for element in dictionnaire:
                if element in words:
                    if dictionnaire[element] not in final_dict[element]:
                        final_dict[element].append(dictionnaire[element])

                if type(dictionnaire[element]) == dict or type(dictionnaire[element]) == list:
                    child_dictionnary = self.crawling_dictionnary(dictionnaire[element], words, layer + 1)
                    for word in words:
                        if child_dictionnary[word]:
                            final_dict[word] += child_dictionnary[word]

        elif type(dictionnaire) == list:
            for element in dictionnaire:
                if type(element) == dict or type(element) == list:
                    child_dictionnary = self.crawling_dictionnary(element, words, layer + 1)
                    for word in words:
                        if child_dictionnary[word]:
                            final_dict[word] += child_dictionnary[word]

        if layer == 0:
            for element in final_dict:
                if len(final_dict[element]) == 1:
                    final_dict[element] = final_dict[element][0] 

        return final_dict

    def delete_doublon(self,liste):
        new_liste = []
        for element in liste:
            if element not in new_liste:
                new_liste.append(element)
        return new_liste

    def get_playlist_videos(self, url):
        code = self.make_get(url)

        for dictionnaire in extract_json_objects(code):

            if "contents" in dictionnaire:
                for i in dictionnaire["contents"]["twoColumnBrowseResultsRenderer"]["tabs"]:
                    playlist_json = i

            if "INNERTUBE_API_KEY" in dictionnaire:
                browser_key = dictionnaire["INNERTUBE_API_KEY"]
                context_dict = dictionnaire["INNERTUBE_CONTEXT"]
                context_dict.pop("adSignalsInfo")
                context_dict.pop("user")
                context_dict.pop("request")
                playlist_data = {"context":dictionnaire["INNERTUBE_CONTEXT"]}
                url_next_playlist = "https://www.youtube.com/youtubei/v1/browse?key=%s" % browser_key

        video_list = []
        
        while True:
            video_information = self.crawling_dictionnary(playlist_json, ["token","contents","onResponseReceivedActions"])
            
            if video_information["onResponseReceivedActions"]:
                video = video_information["onResponseReceivedActions"][0]["appendContinuationItemsAction"]["continuationItems"]
                
            else:
                video = video_information["contents"][2]

                
            for index in range(len(video)-1):
                video_id = video[index]["playlistVideoRenderer"]["videoId"]
                video_title = video[index]["playlistVideoRenderer"]["title"]["runs"][0]["text"]
                video_list.append({"videoId":video_id,"title":video_title})
                

            if video_information["token"]:
                data_next_playlist = playlist_data
                data_next_playlist.update({"continuation":video_information["token"]})
                data_next_playlist = str(data_next_playlist).replace("'",'"').replace(" {","{").replace(' "','"').replace(" True","true") # Ca marche mieux avec Requests cette requete
                playlist_json = json.loads(self.make_post(url_next_playlist,data_next_playlist).text)
            else:
                return video_list

    def download(self, url, filename):
        response = urllib.request.Request(url)
        
        try:
            len_bytes = str(urllib.request.urlopen(response).info().get('Content-Length'))
        except:
            print(url)
        
        response.add_header('Range','bytes=0-'+len_bytes)
        myFile = open(filename+".m4a","wb")
        myFile.write(urllib.request.urlopen(response).read())
        myFile.close()

    def cleaning_filename(self, filename):
        filename = filename.replace('?',"").replace('<','').replace('>','').replace(':','').replace('/','').replace('\\','').replace('*','').replace('|','').replace('"','')
        return filename


    def make_get(self, url, headers=None):
    #  URLLIB
        # request = self.browser_session.request.Request(url)
        # request.add_header("User-Agent","Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
        # request.add_header("Connection","keep-alive")
        # return self.browser_session.request.urlopen(request).read().decode()

    #  Requests
        request = self.browser_session.get(url, headers=headers)
        return request.text

    def make_post(self, url, data):
        
    #  urllib
        # # data = urllib.parse.urlencode(data)
        # # json_data = json.dumps(data)
        # # post_data = json_data.encode('utf-8')
        # data = data.encode("utf-8")
        # request = self.browser_session.request.Request(url, data=data)
        # # request.add_header("User-Agent","Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
        # # request.add_header("Connection","keep-alive")
        # return self.browser_session.request.urlopen(request)

    #  requests
        return self.browser_session.post(url, data=data)


    def __init__(self, url, folder=None):
        
    #   """ setup le browser """
    #  URLLIB
        # self.browser_session = urllib
        # self.cookie = http.cookiejar.MozillaCookieJar()
        # cookie_handler = self.browser_session.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookie))
        # cookie_handler.addheaders = [('User-agent', 'Mozilla/5.0')]
        # self.browser_session.request.install_opener(cookie_handler)

    #  Requests    
        self.browser_session = requests.session()
        default_folder = "/storage/emulated/0/Music"
        if folder != "":
            if folder[0] != "/":
                folder = "%s/%s" % (default_folder, folder)
        else:
            folder = "%s/%s" % (default_folder, folder)

        temp = ""
        for path in folder.split("/"):
            temp += "%s/" % path
            if os.path.isdir(temp) is False:
                os.mkdir(temp)
        if "playlist" in url:
            for i in self.get_playlist_videos(url):
                download_link = self.get_video_link("https://www.youtube.com/watch?v=%s" % i["videoId"])
                filename = self.cleaning_filename(i["title"])
                print(filename)
                self.download(download_link, "%s/%s" % (folder, filename))
        else:
            print("Not a playlist")

conidl(input("link : "), input("folder : "))
