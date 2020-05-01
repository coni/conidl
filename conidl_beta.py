import requests
import urllib.parse
from jsinterp import JSInterpreter

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


# Cette video a un probleme de localisation je crois https://www.youtube.com/watch?v=2N4Qi5oYgDk
video_url = "https://www.youtube.com/watch?v=DHFemeiBK3g"

video_id = getVideoID(video_url)
video_webpage = getWebpage(video_url)
player_url = getJsPlayer(video_webpage)
get_info_video_webpage = requests.get("http://youtube.com/get_video_info?video_id="+video_id)
get_info_video_webpage = urllib.parse.unquote(get_info_video_webpage.text)


allItag = get_info_video_webpage.split('"adaptiveFormats":[')[1].split(']')[0]


#nic ca mere on fera un truc propre plus tard

unItag = ""
import os
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
            if '"itag":140' in unItag:
                itag140 = unItag
            unItag = ""

cipher = '"cipher'+itag140.split('cipher')[1][0:-1]
cipher = urllib.parse.unquote(cipher)
error = True
temp = -1
print()
sig = cipher.split('s=')[temp]
while error:
    if len(sig) < 100 or 'cipher' in sig or '&' in sig:
        temp = temp + 1
        sig = cipher.split('s=')[temp].split("\\")[0]
    else:
        error = False

sig = sig.replace('"',"").split("\\")[0]

url = urllib.parse.unquote(itag140.split('url=')[1][0:-2]).split('%3')[0].split('\\')[0]
# print("len :",len(sig))
# print("sig : "+sig)
# print("url : "+url)

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
        jsi = JSInterpreter(jscode)
        initial_function = jsi.extract_function(funcname)
        return lambda s: initial_function([s])

player_url = "http://youtube.com"+player_url.replace("\\/","/")
# print(player_url)
code = requests.get(player_url).text

res = _parse_sig_js(code)
compat_chr = chr
test_string = ''.join(map(compat_chr, range(len(sig))))
cache_res = res(test_string)
cache_spec = [ord(c) for c in cache_res]
finalsig = ""
for i in cache_spec:
    finalsig = finalsig+sig[i]
#+"%3D%3D&sig=

print("sig : "+sig+"\n\nurl : "+url+"\n\nfinalsig : "+finalsig)

print("essayes ca : "+url+"&sig="+finalsig)














#kozypop twilligt
"sp=sig\u0026s=RJpPlLswaQqgfSa3RaMo-YC_SSeVge1agMAnrF5I7aTIM3Ga8dZDgLUCIQDHIE8-Pu5DLevhcVb6Uih-OFCZOXt9gYGon2XZUvGm1Q==\u0026"
"\u0026sp=sig\u0026s=RJpPlLsw6QPgJO1YPbESeQvs1omK0ByOegAGdYWAo8_ICCESAe21BDwCIQCbzNmy8Z8GGvxEED-SX4vdvilBg9zpXF4xLIvGGv1zBQ=="

#Jakob Ogawa - You Might Be Sleeping [with Clairo]
"\u0026sp=sig\u0026s=RJpPlLswlAlgersV906PvX3ivpsyqPmNEaAz-ZjgKrAI02A53ak8Y_cCIFGPMC4SlPCYpPHonDgsWoBWzOelJBp8zgpowa1zw7TH"
"s=RJpPlLsweQ0geVYHCL93xNpkyaNXiC-q2LAOfm6_-QeITMtjAIKFj8QCIQCQXEmCqye-ReE2mrZ_t-kMb9HiAeAVMZFV4Xr9TKGiDg==\u0026"