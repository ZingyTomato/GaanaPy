import asyncio
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

class Functions:
    
    def __init__(self):
        self.BLOCK_SIZE = 16
    
    async def decryptLink(self, encrypted_data: str) -> str:
        encrypted_data = encrypted_data.strip()
        ## This master key can possibly keep changing.
        KEY = b'gy1t#b@jl(b$wtme' 
        offset = int(encrypted_data[0]) ## Calculate offset from the first character.
        
        ## Extract the raw IV using the offset.
        ivRaw = encrypted_data[offset:offset + self.BLOCK_SIZE]
        iv = ivRaw.encode("utf-8")
        
        ## Calculate ciphertext.
        cipher_text_b64 = encrypted_data[offset + self.BLOCK_SIZE:]
        cipher_bytes = base64.b64decode(cipher_text_b64)
        
        ## Decrypt ciphertext to get final URL.
        cipher = AES.new(KEY, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(cipher_bytes), self.BLOCK_SIZE)
        
        return decrypted.decode("utf-8") 

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
