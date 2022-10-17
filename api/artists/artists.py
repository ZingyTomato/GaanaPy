import asyncio

class Artists():
    async def search_artists(self, search_query: str, limit: int) -> list:
        aiohttp = self.aiohttp
        endpoints = self.api_endpoints
        errors = self.errors
        response = await aiohttp.post(endpoints.search_artists_url + search_query)
        result = await response.json()
        artist_ids = []
        for i in range(0,int(limit)):
            try:
                artist_ids.append(result['gr'][0]['gd'][int(i)]['seo'])
            except (IndexError, TypeError, KeyError):
                pass
        if len(artist_ids) == 0:
          return await errors.no_results()
        artist_info = await self.get_artist_info(artist_ids, False)
        return artist_info

    async def get_artist_info(self, artist_id: list, info: bool) -> list:
        aiohttp = self.aiohttp
        endpoints = self.api_endpoints
        artist_info = []
        if info == True:
            self.info = True
        for i in artist_id:
            response = await aiohttp.post(endpoints.artist_details_url + i)
            result = await response.json()
            artist_info.extend(await asyncio.gather(*[self.format_json_artists(result) for i in range(0,1)]))
        return artist_info

    async def get_top_tracks(self, artist_id: str) -> dict:
        aiohttp = self.aiohttp
        endpoints = self.api_endpoints
        response = await aiohttp.post(endpoints.artist_top_tracks + artist_id)
        result = await response.json()
        track_seokeys = []
        for track in result['entities']:
            track_seokeys.append(track['seokey'])
        track_data = await self.get_track_info(track_seokeys)
        return track_data

    async def format_json_artists(self, results: dict) -> dict:
        functions = self.functions
        errors = self.errors
        data = {}
        try:
            data['seokey'] = results['artist'][0]['seokey']
        except (IndexError, TypeError, KeyError):
            return await errors.invalid_seokey()
        data['artist_id'] = results['artist'][0]['artist_id']
        data['name'] = results['artist'][0]['name']
        data['song_count'] = results['artist'][0]['songs']
        data['album_count'] = results['artist'][0]['albums']
        data['favorite_count'] = results['artist'][0]['favorite_count']
        data['artist_url'] = f"https://gaana.com/artist/{data['seokey']}"
        data['images'] = {'urls': {}}
        data['images']['urls']['large_artwork'] = (results['artist'][0]['atw']).replace("size_m", "size_l")
        data['images']['urls']['medium_artwork'] = (results['artist'][0]['atw']).replace("size_m", "size_m")
        data['images']['urls']['small_artwork'] = (results['artist'][0]['atw']).replace("size_m", "size_s")
        if self.info == True:
            data['top_tracks'] = await self.get_top_tracks(data['artist_id'])
        self.info = False
        return data