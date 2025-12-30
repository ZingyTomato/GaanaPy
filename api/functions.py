import asyncio
from Crypto.Cipher import AES
import base64

class Functions:
    
    async def decryptLink(self, encrypted_data: str) -> str:
        ## NEW IV and KEY. These can possibly keep changing.
        IV = b'xC4dmVJAq14BfntX'
        KEY = b'gy1t#b@jl(b$wtme' 
        offset = int(encrypted_data[0]) ## Calculate offset from the first character.
        cipher = AES.new(KEY, AES.MODE_CBC, IV)
        
        ## Extract Ciphertext (skipping offset + 16-char IV string).
        ciphertext_b64 = encrypted_data[offset + 16:]
        ciphertext = base64.b64decode(ciphertext_b64 + "==")
        
        ## Decrypt using the IV and key from above.
        decrypted = cipher.decrypt(ciphertext)
        raw_text = decrypted.decode('utf-8', errors='ignore').strip()
        
        if "/hls/" in raw_text:
            path_start = raw_text.find("hls/")
            clean_path = raw_text[path_start:]
            # Remove any non-printable padding characters at the end.
            clean_path = "".join(filter(lambda x: x.isprintable(), clean_path))
            return f"https://vodhlsgaana-ebw.akamaized.net/{clean_path}"

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
