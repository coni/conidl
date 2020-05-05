# coding: utf-8
import urllib.request, urllib.parse
from jsinterp import JSInterpreter
import os

def get_json_name(player_url,sig):
    player_url = player_url.split('.')[-1] + "_" + player_url.split('.')[-2].split("/")[0]+"_"+str(len(sig))+".json"
    return player_url

def get_webpage_code(webpage):
    code = ""
    for i in webpage:
        code += i.decode()
    return code

def _parse_sig_js(jscode):
        for i in jscode.splitlines():
            if '=function(a){a=a.split("")' in i:
                if len(i.split("=")[0]) == 2:
                    funcname = i.split("=")[0]
        jsi = JSInterpreter(jscode)
        initial_function = jsi.extract_function(funcname)
        return lambda s: initial_function([s])

def get_Video_ID(video_url):
    try:
        video_id = video_url.split("=")[1].split('&')[0]
    except IndexError:
        video_id = video_url.split("/")[-1]
    return video_id

def get_js_player(video_webpage):
    for i in video_webpage.splitlines():
        if "assets" in i:
            player_url = i.split('"js":')[1].split('"')[1]
            return player_url

def get_Itag(allItag,itag_id):
    if '\\"itag\\"' in allItag:
        itag_string = '\\"itag\\":'
    else:
        itag_string = '"itag":'

    unItag = ""
    count0 = 0
    count1 = 0

    for i in allItag:
        unItag = unItag+i
        if i == "{":
            count0 = count0+1
        if i == "}":
            count1 = count1+1
        
        if i != ",":
            if count0 == count1:
                if itag_string+str(itag_id) in unItag:
                    itag = unItag
                    if itag[0] == ",":
                        itag = itag[1:-1]
                    if itag[-1] != "}":
                        itag = itag+"}"
                    return itag
                unItag = ""

def sigYouMightBeSleeping(itag):
    cipher = '"cipher'+itag.split('cipher')[1][0:-1]
    cipher = urllib.parse.unquote(cipher)
    error = True
    temp = -1
    sig = cipher.split('s=')[temp]
    while error:
        if len(sig) < 100 or 'cipher' in sig or '&' in sig:
            temp = temp + 1
            sig = cipher.split('s=')[temp].split("\\")[0]
        else:
            error = False
    sig = sig.replace('"',"").split("\\")[0]
    url = urllib.parse.unquote(itag.split('url=')[1][0:-2]).split('%3')[0].split('\\')[0]
    return sig, url

def sigWaleuleu(itag):
    if '\\"url\\"' in itag:
        url = itag.split('\\"url\\":\\"')[1].split('"')[0].replace('\\u0026','&').replace("\\/","/").replace("\\","")
    else:
        url = itag.split('url":"')[1].split('"')[0].replace('\\u0026','&')
    return url

def decodeSig(sig,url,player_url, json_filename):
    code_webpage = urllib.request.urlopen(urllib.request.Request(player_url))
    code = get_webpage_code(code_webpage)
    res = _parse_sig_js(code)
    cache_res = res(test_string)
    cache_spec = [ord(c) for c in cache_res]
    finalsig = ""
    for i in cache_spec:
        finalsig += sig[i]
    url = url+"&sig="+finalsig
    return url

def get_all_itag(webpage):
    if '"adaptiveFormats\\":[' in webpage:
        for i in webpage.splitlines():
            if 'adaptiveFormats' in i:
                allItag = i.split('"adaptiveFormats\\":[')[1].split(']')[0]
                break
    else:
        webpage = urllib.parse.unquote(webpage)
        allItag = webpage.split('"adaptiveFormats":[')[1].split(']')[0]
    return allItag

def get_video_title(webpage):
    for i in webpage.splitlines():
        if '",\\"title\\":\\"' in i:
            video_title = i.split('",\\"title\\":\\"')[1].split('\\",')[0].replace('\\/',"/").replace('\\\\\\"','"')
            return video_title

def cleaning_filename(filename):
    filename = filename.replace('?',"").replace('<','').replace('>','').replace(':','').replace('/','').replace('\\','').replace('*','').replace('|','').replace('"','')
    return filename

def download(url, filename):
    filename = cleaning_filename(filename)
    response = urllib.request.Request(url)
    len_bytes = str(urllib.request.urlopen(response).info().get('Content-Length'))
    response.add_header('Range','bytes=0-'+len_bytes)
    myFile = open(filename+".m4a","wb")
    myFile.write(urllib.request.urlopen(response).read())
    myFile.close()

def url_Verification(url):
    if "." in url:
        if "youtu.be" in url or "youtube.com" in url:
            if "=" in url:
                if len(url.split("=")[1].split("&")[0]) == 11:
                    return "Video"
                elif "playlist" in url:
                    return "Playlist"
            else:
                if len(url.split("/")[-11]) == 11:
                    return "Video"
    return False

def downloadVideo(video_url, last_from_playlist=False):
    try:
        try:
            index = video_url.split('index=')[1]
        except:
            index = None
        video_url = video_url.split('&')[0]
        video_id = get_Video_ID(video_url)
        video_webpage = urllib.request.urlopen(urllib.request.Request(video_url))
        video_webpage_code = get_webpage_code(video_webpage)

        player_url = "http://youtube.com"+get_js_player(video_webpage_code).replace("\\/","/")
        video_title = get_video_title(video_webpage_code)
        try:
            all_Itag = get_all_itag(video_webpage_code)
        except:
            get_info_video_webpage = urllib.request.urlopen(urllib.request.Request("http://youtube.com/get_video_info?video_id="+video_id))
            get_info_video_webpage_code = get_webpage_code(get_info_video_webpage)
            all_Itag = get_all_itag(get_info_video_webpage_code)

        itag140 = get_Itag(all_Itag,140)

        if 'cipher' in itag140:
            sig, url = sigYouMightBeSleeping(itag140)
            cache_cipher_name = get_json_name(player_url,sig)
            url = decodeSig(sig,url,player_url, cache_cipher_name)
        else:
            url = sigWaleuleu(itag140)
        if index:
            print(str(index)+"/"+str(last_from_playlist),video_title)
        else:
            print(video_title)
        download(url, video_title)
        return True
    except:
        return False

def get_video_in_playlist(url):
    playlist_webpage_code = get_webpage_code(urllib.request.urlopen(urllib.request.Request(url)))
    playlist_videos = []

    videos = ""
    first_video = ""

    for i in playlist_webpage_code.splitlines():
        if ";index=1" in i:
            if i.split('href="')[1].split('"')[0].split('&')[0] != first_video:
                first_video = i.split('href="')[1].split('"')[0]
                break
    
    first_video_code = get_webpage_code(urllib.request.urlopen(urllib.request.Request("http://youtube.com"+first_video)))
    validation = False
    for i in first_video_code.splitlines():
        if 'amp;index=1"' in i and 'http' not in i.split('href="')[1].split('"')[0]:
            videos = i.split('href="')[1].split('"')[0]
            playlist_videos.append("https://youtube.com"+videos)
            validation = True
        if "amp;index=" in i and validation is True:
            if i.split('href="')[1].split('"')[0] != videos and 'http' not in i.split('href="')[1].split('"')[0]:
                videos = i.split('href="')[1].split('"')[0]
                playlist_videos.append("https://youtube.com"+videos)


    return playlist_videos


url = input("Link : ")

url_type = url_Verification(url)
if url_type == False:
    print("Wrong link")
    exit()
elif url_type == "Video":
    downloadVideo(url)
elif url_type == "Playlist":
    count = 0
    error = []
    playlist_videos = get_video_in_playlist(url)
    last_from_playlist = playlist_videos[-1].split('index=')[-1].split('&')[0]
    for i in get_video_in_playlist(url):
        count += 1
        verification = downloadVideo(i, last_from_playlist=last_from_playlist)
        if verification is False:
            error.append(count)
print(error)