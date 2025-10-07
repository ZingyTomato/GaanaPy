import asyncio
from Crypto.Cipher import AES
import base64
import binascii

class Functions:
    
    ### From https://github.com/cyberboysumanjay/GaanaAPI/blob/0488e812a9ac7d740d785c6e09f1e83e527eebcc/gaana.py#L57
    async def decryptLink(self, link: str) -> str:
        IV = 'asd!@#!@#@!12312'.encode('utf-8')
        KEY = 'g@1n!(f1#r.0$)&%'.encode('utf-8')
        aes = AES.new(KEY, AES.MODE_CBC, IV)
        try:
            if not link:
                return ""
            if isinstance(link, bytes):
                raw_link = link.decode('utf-8', errors='ignore')
            else:
                raw_link = str(link)
            normalized = raw_link.strip().replace("\n", "").replace("\r", "").replace(" ", "")
            padding = '=' * (-len(normalized) % 4)
            try:
                decoded = base64.b64decode(normalized + padding)
            except (binascii.Error, ValueError):
                decoded = base64.urlsafe_b64decode(normalized + padding)
            decrypted = aes.decrypt(decoded).decode('utf-8')
            stream_url = await self.unpad(decrypted)
        except (binascii.Error, UnicodeDecodeError, ValueError, TypeError, IndexError):
            return ""
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

    async def isExplicit(self, explicit: int) -> bool: 
        if explicit == 1:
            return True
        else:
            return False 
