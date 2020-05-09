# Marche avec la plus part des vidéos, pas toutes, il faut revoir ça€€

"""  Pour vous expliquer comment le programme marche avant que j'oublie comment ca marche #: 

On va prendre "https://www.youtube.com/watch?v=B9NokdAGVvw" pour exemple.
Pour commencer il faut juste récuperer l'id de cette vidéo "B9NokdAGVvw", puis avec cette id on va aller sur une direction
spéciale de youtube : "http://youtube.com/get_video_info?video_id=B9NokdAGVvw". Dessus on aura un fichier "get_video_info"
semi encode en "url" (j'ai pas le nom exact de l'encodage mais juste en tapant ca sur internet on est censé trouver)

Dans ce fichier "get_video_info" on a TOUTES les informations de la vidéos dont (normalement) plusieurs liens téléchargeables
les liens peuvent etre différencier par des code appeler "itag", on va prendre le 140 par exemple car c'est le plus
interessant dans un lecteur musique rapide.

Si c'est decoder on est censé avoir un truc similaire à ca : 
{"itag":140,
"mimeType":"audio/mp4;+codecs=\"mp4a.40.2\""
,"bitrate":130305,
"initRange":{"start":"0","end":"631"},
"indexRange":{"start":"632","end":"1059"},
"lastModified":"1575156026981946",
"contentLength":"5278284",
"quality":"tiny",
"projectionType":"RECTANGULAR",
"averageBitrate":129488,
"highReplication":true,
"audioQuality":"AUDIO_QUALITY_MEDIUM",
"approxDurationMs":"326101",
"audioSampleRate":"44100",
"audioChannels":2,
"cipher":"s=RJpPlLswRQ2hANupiGE7o3C1I0_gqQld1dAoTpt4pBXIXnxUBcR7dmAlAiBxlj41LLdUGIBWzogE2zm53qxDYr-CcuMEMXCMTQfPXA%3D%3D\u0026sp=sig\u0026
url=https%3A%2F%2Fr6---sn-n4g-jqbed.googlevideo.com%2Fvideoplayback%3Fexpire%3D1588278905%26ei%3DGOKqXpXTO9SIVKu1loAM%26ip%3Dx.x.x.x%26id%3Do-AEqjORnSDYozYsCsMGZlEmKR8zFKJc0akCgLcC4bHVr7%26itag%3D140%26source%3Dyoutube%26requiressl%3Dyes%26mh%3D56%26mm%3D31%252C26%26mn%3Dsn-n4g-jqbed%252Csn-4g5ednld%26ms%3Dau%252Conr%26mv%3Dm%26mvi%3D5%26pcm2cms%3Dyes%26pl%3D17%26initcwndbps%3D548750%26vprv%3D1%26mime%3Daudio%252Fmp4%26gir%3Dyes%26clen%3D5278284%26dur%3D326.101%26lmt%3D1575156026981946%26ns%3Db_kTJc2zDGbF79XUm7JmpTkC%26mt%3D1588257274%26fvip%3D4%26keepalive%3Dyes%26c%3DWEB%26txp%3D5531432%26n%3DsTs_U1E1rLpTysH%26sparams%3Dexpire%252Cei%252Cip%252Cid%252Citag%252Csource%252Crequiressl%252Cvprv%252Cmime%252Cgir%252Cclen%252Cdur%252Clmt%252Cns%26lsparams%3Dmh%252Cmm%252Cmn%252Cms%252Cmv%252Cmvi%252Cpcm2cms%252Cpl%252Cinitcwndbps%26lsig%3DALrAebAwRAIgC5eLeCdRCyN4AMDh-qUPFG89M1pnrOogcvRzInqqXZ0CIDNHUBk1ng7MeYmRbwTRE7gdi3m2fi1cuPBYZxojXXRe"}

CAS No.1:

    Vous allez trouver ça mais sur une meme et seule ligne, j'ai juste rajouter des espaces pour que ca soit lisible.
    Ce qui est le plus interessant ici c'est le "cipher" qui contient le "sig" : "RJpPlLswRQ2hANupiGE7o3C1I0_gqQld1dAoTpt4pBXIXnxUBcR7dmAlAiBxlj41LLdUGIBWzogE2zm53qxDYr-CcuMEMXCMTQfPXA"
    et l'url "https%3A%2F%2Fr6---sn-n4g-jqbed.googlevideo.com%2Fvideoplayback%3Fexpire%3D1588278905%26ei%3DGOKqXpXTO9SIVKu1loAM%26ip%3Dx.x.x.x%26id%3Do-AEqjORnSDYozYsCsMGZlEmKR8zFKJc0akCgLcC4bHVr7%26itag%3D140%26source%3Dyoutube%26requiressl%3Dyes%26mh%3D56%26mm%3D31%252C26%26mn%3Dsn-n4g-jqbed%252Csn-4g5ednld%26ms%3Dau%252Conr%26mv%3Dm%26mvi%3D5%26pcm2cms%3Dyes%26pl%3D17%26initcwndbps%3D548750%26vprv%3D1%26mime%3Daudio%252Fmp4%26gir%3Dyes%26clen%3D5278284%26dur%3D326.101%26lmt%3D1575156026981946%26ns%3Db_kTJc2zDGbF79XUm7JmpTkC%26mt%3D1588257274%26fvip%3D4%26keepalive%3Dyes%26c%3DWEB%26txp%3D5531432%26n%3DsTs_U1E1rLpTysH%26sparams%3Dexpire%252Cei%252Cip%252Cid%252Citag%252Csource%252Crequiressl%252Cvprv%252Cmime%252Cgir%252Cclen%252Cdur%252Clmt%252Cns%26lsparams%3Dmh%252Cmm%252Cmn%252Cms%252Cmv%252Cmvi%252Cpcm2cms%252Cpl%252Cinitcwndbps%26lsig%3DALrAebAwRAIgC5eLeCdRCyN4AMDh-qUPFG89M1pnrOogcvRzInqqXZ0CIDNHUBk1ng7MeYmRbwTRE7gdi3m2fi1cuPBYZxojXXRe"
    qui faut pas oublier de décoder. Si on rentre ce lien meme decoder, cela ne nous mènera a rien, car l'url n'est pas complet
    il manque le sig a la fin de l'url pour ça il faut rajouter
        "&sig=RJpPlLswRQ2hANupiGE7o3C1I0_gqQld1dAoTpt4pBXIXnxUBcR7dmAlAiBxlj41LLdUGIBWzogE2zm53qxDYr-CcuMEMXCMTQfPXA"
    Cela marchera toujours pas, pour que ca marche il faut aller décoder en cherchant le code de la permutation. Pour ce faire
    il faut aller chercher le script javascript qui permet de décoder ca, il trouvable sur la page web de la vidéo : "https://www.youtube.com/watch?v=B9NokdAGVvw"
    ca ressemble a un truc du genre '"assets":{"css":"\/s\/player\/64dddad9\/www-player-webp.css","js":"\/s\/player\/64dddad9\/player_ias.vflset\/fr_FR\/base.js"}}'
    il a juste cette partie "\/s\/player\/64dddad9\/player_ias.vflset\/fr_FR\/base.js" qui nous interesse. Maintenant que nous avons le lecteur, dedans ce trouve la fonction
    qui permet de décoder le sig, faut aller la chercher.

CAS No.2
    Il est possible aussi de ne pas trouver de cipher, et dans ce cas l'url emmene directement vers le lien téléchargeable

CAS No.3
    Si les malgrès les deux cas rien ne fonctionne, les url téléchargeables en plus des cipher sont trouvables sur la page de la vidéo ^^
    C'est la solution contre le problèmes de localisations en EN, faut que j'l'intègre


Dans le JSinterpreter :
    Funcname : C'est juste une recherche de string ('?=function(a){a=a.split("")}' il recherche le '?' en particulier)

Et c'est la dernière partie que j'ai pas entièrement encore compris.
"""

""" All Itag
249          webm       audio only tiny   55k , opus @ 50k (48000Hz), 1.67MiB
250          webm       audio only tiny   73k , opus @ 70k (48000Hz), 2.21MiB
140          m4a        audio only tiny  130k , m4a_dash container, mp4a.40.2@128k (44100Hz), 4.20MiB
251          webm       audio only tiny  140k , opus @160k (48000Hz), 4.30MiB
160          mp4        256x144    144p  121k , avc1.4d400c, 24fps, video only, 2.74MiB
278          webm       256x144    144p  132k , webm container, vp9, 24fps, video only, 2.77MiB
133          mp4        426x240    240p  267k , avc1.4d4015, 24fps, video only, 6.19MiB
242          webm       426x240    240p  313k , vp9, 24fps, video only, 5.33MiB
243          webm       640x360    360p  588k , vp9, 24fps, video only, 9.09MiB
134          mp4        640x360    360p  609k , avc1.4d401e, 24fps, video only, 12.58MiB
244          webm       854x480    480p 1137k , vp9, 24fps, video only, 15.74MiB
135          mp4        854x480    480p 1154k , avc1.4d401e, 24fps, video only, 25.11MiB
136          mp4        1280x720   720p 2251k , avc1.4d401f, 24fps, video only, 47.72MiB
247          webm       1280x720   720p 2300k , vp9, 24fps, video only, 28.30MiB
248          webm       1920x1080  1080p 3203k , vp9, 24fps, video only, 44.41MiB
137          mp4        1920x1080  1080p 4567k , avc1.640028, 24fps, video only, 90.77MiB
18           mp4        640x360    360p  530k , avc1.42001E, mp4a.40.2@ 96k (44100Hz), 17.19MiB
22           mp4        1280x720   720p 1601k , avc1.64001F, mp4a.40.2@192k (44100Hz) (best)

"""

# coding: utf-8
import urllib.request, urllib.parse
from jsinterp import JSInterpreter
import os, os.path
import time

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
    if 'signatureCipher' in itag:
        cipher = '"signatureCipher'+itag.split('signatureCipher')[1][0:-1]
        sig = cipher.split("=sig")[0].split("=")[-1].split("\\\\")[0].replace("%3D","=")
        url = urllib.parse.unquote(cipher.split("url=")[1].split('"')[0].replace("\\/","/").replace("%3F","?").replace("%3D","=").replace("%26","&")).replace("%3D","").replace("\\","")
    else:
        cipher = '"cipher'+itag.split('cipher')[1][0:-1]

    # try:
    #     cipher = '"cipher'+itag.split('cipher')[1][0:-1]
    # except:
    #     print(itag)
    #     exit()
        
        cipher = urllib.parse.unquote(cipher)
        temp = -1
        sig = cipher.split('s=')[temp]
        while True:
            if len(sig) < 100 or 'cipher' in sig or '&' in sig:
                temp = temp + 1
                sig = cipher.split('s=')[temp].split("\\")[0]
            else:
                break
        sig = sig.replace('"',"").split("\\")[0]
        url = urllib.parse.unquote(itag.split('url=')[1][0:-2]).split('"')[0].split('\\')[0]
    if len(url) < 420:
        print(itag)
        exit()

    return sig, url

def sigWaleuleu(itag):
    if '\\"url\\"' in itag:
        url = itag.split('\\"url\\":\\"')[1].split('"')[0].replace('\\u0026','&').replace("\\/","/").replace("\\","")
    else:
        try:
            url = itag.split('url":"')[1]
        except:
            print(itag)
            exit()
        url = url.split('"')[0].replace('\\u0026','&')
    return url

def decodeSig(sig,url,player_url, json_filename):
    if os.path.isfile("./cache/"+json_filename) is not True:
        code_webpage = urllib.request.urlopen(urllib.request.Request(player_url))
        code = get_webpage_code(code_webpage)

        # slt = open("base.js","r")
        # code = slt.read()
        res = _parse_sig_js(code)
        # slt.close()
        #res c'est la fonction Javascript pour trouver la 'clé' du chiffrement

        # Ca sort l'alphabet Ascii et le met dans test_string, la longueur dépend de la longueur du sig
        test_string = ''.join(map(chr, range(len(sig))))
        cache_res = res(test_string)
        #cache_res va prendre l'alphabet d'en haut et le mélanger selon la fonction
        cache_spec = [ord(c) for c in cache_res]
        # Et enfaite l'alphabet modifier c'est juste pour obtenir les nombres a permuter (c'est pour ca qu'on utilise ord() pour avoir les codes des 
        # caracteres )
        
        json_file = open("./cache/"+json_filename,"w")
        json_file.write("[")
        for i in range(len(cache_spec)):
            if i != len(cache_spec)-1:
                json_file.write(str(cache_spec[i])+", ")
            else:
                json_file.write(str(cache_spec[i]))
        json_file.write("]")
        json_file.close()
    else:
        jsuisunouf = open("./cache/"+json_filename)
        slt = jsuisunouf.read().splitlines()[0]
        cache_spec = []
        for i in range(len(slt.split(", "))):
            cache_spec.append(int(slt.split(", ")[i].replace("[","").replace("]","")))
        jsuisunouf.close()

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
            video_title = i.split('",\\"title\\":\\"')[1].split('\\",')[0].replace('\\/',"/").replace('\\\\\\"','"').replace("\\\\u0026","&")
            return video_title

def cleaning_filename(filename):
    filename = filename.replace('?',"").replace('<','').replace('>','').replace(':','').replace('/','').replace('\\','').replace('*','').replace('|','').replace('"','')
    return filename

def download(url, filename):
    filename = cleaning_filename(filename)
    response = urllib.request.Request(url)
    try:
        len_bytes = str(urllib.request.urlopen(response).info().get('Content-Length'))
    except:
        print(url)
        exit()
    response.add_header('Range','bytes=0-'+len_bytes)
    myFile = open("./music/"+filename+".m4a","wb")
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
                if len(url.split("/")[-1]) == 11:
                    return "Video"
    return False

def downloadVideo(video_url, last_from_playlist=False):
    try:
        index = video_url.split('index=')[1].split("&")[0]
    except:
        index = None
    video_url = video_url.split('&')[0]
    video_id = get_Video_ID(video_url)
    video_webpage = urllib.request.urlopen(urllib.request.Request(video_url))
    video_webpage_code = get_webpage_code(video_webpage)
    try:
        player_url = "https://youtube.com"+get_js_player(video_webpage_code).replace("\\/","/")
    except:
        print("Impossible de récupérer le lecteur")
        return False
    video_title = get_video_title(video_webpage_code)

    try:
        all_Itag = get_all_itag(video_webpage_code)
    except:
        get_info_video_webpage = urllib.request.urlopen(urllib.request.Request("https://youtube.com/get_video_info?video_id="+video_id))
        get_info_video_webpage_code = get_webpage_code(get_info_video_webpage)
        all_Itag = get_all_itag(get_info_video_webpage_code)

    itag140 = get_Itag(all_Itag,140)

    if 'cipher' in itag140 or 'Cipher' in itag140:
        sig, url = sigYouMightBeSleeping(itag140)

        cache_cipher_name = get_json_name(player_url,sig)
        url = decodeSig(sig,url,player_url, cache_cipher_name)
    else:
        url = sigWaleuleu(itag140)
    if last_from_playlist:
        print(str(index)+"/"+str(last_from_playlist),video_title)
    else:
        print(video_title)
    download(url, video_title)
    return True

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
    
    first_video_code = get_webpage_code(urllib.request.urlopen(urllib.request.Request("https://youtube.com"+first_video)))
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

start_time = time.time()

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
