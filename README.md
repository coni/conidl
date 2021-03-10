# conidl
coni trying to understand how YouTube downloader works

## Patch notes
Who cares about patch notes?

## Comment ca marche ?
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

CAS No.2:

    Il est possible aussi de ne pas trouver de cipher, et dans ce cas l'url emmene directement vers le lien téléchargeable

CAS No.3:

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
