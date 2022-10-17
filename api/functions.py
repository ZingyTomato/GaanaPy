import asyncio
from Crypto.Cipher import AES
import base64

class Functions():
    
    ### From https://github.com/cyberboysumanjay/GaanaAPI/blob/0488e812a9ac7d740d785c6e09f1e83e527eebcc/gaana.py#L57
    async def decryptLink(self, link: str) -> str:
        IV = 'asd!@#!@#@!12312'.encode('utf-8')
        KEY = 'g@1n!(f1#r.0$)&%'.encode('utf-8')
        aes = AES.new(KEY, AES.MODE_CBC, IV)
        stream_url = await self.unpad((aes.decrypt(base64.b64decode(link))).decode('utf-8'))
        if "https://vodhlsgaana.akamaized.net" in stream_url:
            stream_url = stream_url.replace("96.mp4.master", "320.mp4.master")
        return stream_url

    async def unpad(self, s: str) -> str: 
        return s[0:-ord(s[-1])]

    async def findArtistNames(self, results: list) -> str:
        artists = []
        for i in results:
            artists.append(i['name'])
        return ', '.join(artists)

    async def findArtistSeoKeys(self, results: list) -> str:
        seokeys = []
        for i in results:
            seokeys.append(i['seokey'])
        return ', '.join(seokeys)

    async def findArtistIds(self, results: list) -> str:
        ids = []
        for i in results:
            ids.append(i['artist_id'])
        return ', '.join(ids)

    async def findGenres(self, results: list) -> str:  
        genres = []
        for i in results:
            try:
                genres.append(i['name'])
            except ValueError:
                return ""
        return ', '.join(genres)