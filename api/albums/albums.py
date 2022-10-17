import asyncio

class Albums():
    async def search_albums(self, search_query: str, limit: int) -> list:
        aiohttp = self.aiohttp
        endpoints = self.api_endpoints
        errors = self.errors
        response = await aiohttp.post(endpoints.search_albums_url + search_query)
        result = await response.json()
        album_ids = []
        for i in range(0,int(limit)):
            try:
                album_ids.append(result['gr'][0]['gd'][int(i)]['seo'])
            except (IndexError, TypeError, KeyError):
                pass
        if len(album_ids) == 0:
          return await errors.no_results()
        album_info = await self.get_album_info(album_ids, False)
        return album_info

    async def get_album_info(self, album_id: list, info: bool) -> list:
        aiohttp = self.aiohttp
        endpoints = self.api_endpoints
        album_info = []
        if info == True:
            self.info = True
        for i in album_id:
          response = await aiohttp.post(endpoints.album_details_url + i)
          result = await response.json()
          album_info.extend(await asyncio.gather(*[self.format_json_albums(result) for i in range(0,1)]))
        return album_info

    async def get_album_tracks(self, album_id: list) -> list:
        aiohttp = self.aiohttp
        endpoints = self.api_endpoints
        response = await aiohttp.post(endpoints.album_details_url + album_id)
        result = await response.json()
        track_seokeys = []
        for i in result['tracks']:
            track_seokeys.append(i['seokey'])
        result = await self.get_track_info(track_seokeys)
        return result

    async def format_json_albums(self, results: dict) -> dict:
        functions = self.functions
        errors = self.errors
        data = {}
        try:
            data['seokey'] = results['album']['seokey']
        except (IndexError, TypeError, KeyError):
            return await errors.no_results()
        data['album_id'] = results['album']['album_id']
        data['title'] = results['album']['title']
        try:
            data['artists'] = await functions.findArtistNames(results['album']['artist'])
            data['artist_seokeys'] = await functions.findArtistSeoKeys(results['tracks'][0]['artist'])
            data['artist_ids'] = await functions.findArtistIds(results['tracks'][0]['artist'])
        except (KeyError, IndexError):
            data['artists'] = ""
            data['artist_seokeys'] = ""
            data['artist_ids'] = ""
        data['duration'] = results['album']['duration']
        data['is_explicit'] = results['album']['parental_warning']
        data['language'] = results['album']['language']
        data['label'] = results['album']['recordlevel']
        data['track_count'] = results['album']['trackcount']
        try:
            data['release_date'] = results['album']['release_date']
        except:
            data['release_date'] = ""
        data['play_count'] = results['album']['al_play_ct']
        data['favorite_count'] = results['album']['favorite_count']
        data['album_url'] = f"https://gaana.com/album/{results['album']['seokey']}"
        data['images'] = {'urls': {}}
        data['images']['urls']['large_artwork'] = (results['album']['artwork']).replace("size_s.jpg", "size_l.jpg")
        data['images']['urls']['medium_artwork'] = (results['album']['artwork']).replace("size_s.jpg", "size_m.jpg")
        data['images']['urls']['small_artwork'] = (results['album']['artwork'])
        if self.info == True:
            data['tracks'] =  await self.get_album_tracks(data['seokey'])
        self.info = False
        return data