import urllib.request, urllib.parse
from jsinterp import JSInterpreter

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

def decodeSig(sig,url,player_url):
    code_webpage = urllib.request.urlopen(urllib.request.Request(player_url))
    code = ""
    for i in code_webpage:
        code = code + i.decode()
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
        if '<span id="eow-title" class="watch-title" dir="ltr" title="' in i:
            video_title = i.split('<span id="eow-title" class="watch-title" dir="ltr" title="')[1].split('"')[0]
            return video_title

def cleaning_filename(filename):
    filename = video_title+".m4a"
    filename = filename.replace('?',"").replace('<','').replace('>','').replace(':','').replace('/','').replace('\\','').replace('*','').replace('|','').replace('"','')
    return filename

def download(url, filename):
    cleaning_filename(filename)
    response = urllib.request.Request(url)
    len_bytes = str(urllib.request.urlopen(response).info().get('Content-Length'))
    response.add_header('Range','bytes=0-'+len_bytes)
    myFile = open(filename,"wb")
    myFile.write(urllib.request.urlopen(response).read())
    myFile.close()

video_url = input("Link : ")

video_id = get_Video_ID(video_url)
video_webpage = urllib.request.urlopen(urllib.request.Request(video_url))

video_webpage_code = ""
for i in video_webpage:
        video_webpage_code += i.decode()

player_url = "http://youtube.com"+get_js_player(video_webpage_code).replace("\\/","/")
video_title = get_video_title(video_webpage_code)

try:
    all_Itag = get_all_itag(video_webpage_code)
except:
    get_info_video_webpage = urllib.request.urlopen(urllib.request.Request("http://youtube.com/get_video_info?video_id="+video_id))
    get_info_video_webpage_code = ""
    for i in get_info_video_webpage:
        get_info_video_webpage_code += i.decode()
    all_Itag = get_all_itag(get_info_video_webpage_code)

itag140 = get_Itag(all_Itag,140)

if 'cipher' in itag140:
    sig, url = sigYouMightBeSleeping(itag140)
    url = decodeSig(sig,url,player_url)
else:
    url = sigWaleuleu(itag140)

download(url, video_title)
