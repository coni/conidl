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

import urllib.request
import requests
import urllib.parse
from jsinterp import JSInterpreter
import os, sys

def _parse_sig_js(jscode):
        # funcname = _search_regex(
        #     (r'\b[cs]\s*&&\s*[adf]\.set\([^,]+\s*,\s*encodeURIComponent\s*\(\s*(?P<sig>[a-zA-Z0-9$]+)\(',
        #      r'\b[a-zA-Z0-9]+\s*&&\s*[a-zA-Z0-9]+\.set\([^,]+\s*,\s*encodeURIComponent\s*\(\s*(?P<sig>[a-zA-Z0-9$]+)\(',
        #      r'\b(?P<sig>[a-zA-Z0-9$]{2})\s*=\s*function\(\s*a\s*\)\s*{\s*a\s*=\s*a\.split\(\s*""\s*\)',
        #      r'(?P<sig>[a-zA-Z0-9$]+)\s*=\s*function\(\s*a\s*\)\s*{\s*a\s*=\s*a\.split\(\s*""\s*\)',
        #      # Obsolete patterns
        #      r'(["\'])signature\1\s*,\s*(?P<sig>[a-zA-Z0-9$]+)\(',
        #      r'\.sig\|\|(?P<sig>[a-zA-Z0-9$]+)\(',
        #      r'yt\.akamaized\.net/\)\s*\|\|\s*.*?\s*[cs]\s*&&\s*[adf]\.set\([^,]+\s*,\s*(?:encodeURIComponent\s*\()?\s*(?P<sig>[a-zA-Z0-9$]+)\(',
        #      r'\b[cs]\s*&&\s*[adf]\.set\([^,]+\s*,\s*(?P<sig>[a-zA-Z0-9$]+)\(',
        #      r'\b[a-zA-Z0-9]+\s*&&\s*[a-zA-Z0-9]+\.set\([^,]+\s*,\s*(?P<sig>[a-zA-Z0-9$]+)\(',
        #      r'\bc\s*&&\s*a\.set\([^,]+\s*,\s*\([^)]*\)\s*\(\s*(?P<sig>[a-zA-Z0-9$]+)\(',
        #      r'\bc\s*&&\s*[a-zA-Z0-9]+\.set\([^,]+\s*,\s*\([^)]*\)\s*\(\s*(?P<sig>[a-zA-Z0-9$]+)\(',
        #      r'\bc\s*&&\s*[a-zA-Z0-9]+\.set\([^,]+\s*,\s*\([^)]*\)\s*\(\s*(?P<sig>[a-zA-Z0-9$]+)\('),
        #     jscode, 'Initial JS player signature function name', group='sig')
        funcname = "Ev"
        """
        En général c'est "Ev" qu'on retrouve, faut que j'écrive un algo pour chercher lequel c'est exactement
        
        """
        jsi = JSInterpreter(jscode)
        initial_function = jsi.extract_function(funcname)
        return lambda s: initial_function([s])

def getVideoID(video_url):
    try:
        video_id = video_url.split("=")[1]
    except IndexError:
        video_id = video_url.split("/")[-1]
    return video_id

def getWebpage(video_url):
    video_webpage = requests.get(video_url)
    return video_webpage

def getJsPlayer(video_webpage):
    for i in video_webpage.iter_lines():
        if "assets" in i.decode():
            player_url = i.decode().split('"js":')[1].split('"')[1]
    return player_url

#nic ca mere on fera un truc propre plus tard

def getItag(allItag,itag_id):
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
                if '"itag":'+str(itag_id) in unItag:
                    itag = unItag
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
    url = itag.split('url":"')[1].split('"')[0].replace('\\u0026','&')
    return url

def decodeSig(sig,url,player_url):
    code = requests.get(player_url).text
    res = _parse_sig_js(code)
    compat_chr = chr
    test_string = ''.join(map(compat_chr, range(len(sig))))
    cache_res = res(test_string)
    cache_spec = [ord(c) for c in cache_res]
    finalsig = ""
    for i in cache_spec:
        finalsig = finalsig+sig[i]
    url = url+"&sig="+finalsig
    return url


# Cette video a un probleme de localisation je crois https://www.youtube.com/watch?v=2N4Qi5oYgDk
# video_url = "https://www.youtube.com/watch?v=B9NokdAGVvw"
# video_url = "https://www.youtube.com/watch?v=WybG8FesMc8"
# Ne télécharge pas les vidéos ayant des problèmes de localisations en "EN"

video_url = input("Lien : ")

video_id = getVideoID(video_url)
video_webpage = getWebpage(video_url)
player_url = "http://youtube.com"+getJsPlayer(video_webpage).replace("\\/","/")
get_info_video_webpage = urllib.parse.unquote(requests.get("http://youtube.com/get_video_info?video_id="+video_id).text)


try:
    allItag = get_info_video_webpage.text.split('"adaptiveFormats":[')[1].split(']')[0]
except:
    sys.exit("La vidéo à un problème de localisation")
    #C'est une déduction, j'ai rien fais pour aller fouiller à l'intérieur


itag140 = getItag(allItag,140)

if 'cipher' in itag140:
    sig, url = sigYouMightBeSleeping(itag140)
    url = decodeSig(sig,url,player_url)
else:
    url = sigWaleuleu(itag140)

print(url)

#Télécharger le fichier : m4a_webpage = urllib.request.urlretrieve(m4a, "videoplayback.m4a")