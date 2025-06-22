import asyncio

class Songs:
    async def search_songs(self, search_query: str, limit: int) -> list:
        aiohttp = self.aiohttp
        endpoints = self.api_endpoints
        errors = self.errors
        response = await aiohttp.post(endpoints.search_songs_url + search_query)
        result = await response.json()
        track_ids = []
        for i in range(0,int(limit)):
            try:
              track_ids.append(result['gr'][0]['gd'][int(i)]['seo'])
            except (IndexError, TypeError, KeyError):
              pass
        if len(track_ids) == 0:
          return await errors.no_results()
        track_info = await self.get_track_info(track_ids)
        return track_info

    async def get_track_info(self, track_id: list) -> list:
        aiohttp = self.aiohttp
        endpoints = self.api_endpoints
        track_info = []
        for i in track_id:
          response = await aiohttp.post(endpoints.song_details_url + i)
          result = await response.json()
          track_info.extend(await asyncio.gather(*[self.format_json_songs(i) for i in result['tracks']]))
        return track_info

    async def format_json_songs(self, results: dict) -> dict:
        functions = self.functions
        errors = self.errors
        data = {}
        try:
          data['seokey'] = results['seokey']
        except KeyError:
          return await errors.invalid_seokey()
        data['album_seokey'] = results['albumseokey']
        data['track_id'] = results['track_id']
        data['title'] = results['track_title']
        data['artists'] = await functions.findArtistNames(results['artist'])
        data['artist_seokeys'] = await functions.findArtistSeoKeys(results['artist'])
        data['artist_ids'] = await functions.findArtistIds(results['artist'])
        data['artist_image'] = (results['artist_detail'][0]['atw'])
        data['album'] = results['album_title']
        data['album_id'] = results['album_id']
        data['duration'] = results['duration']
        data['popularity'] = results['popularity']
        data['genres'] = await functions.findGenres(results['gener'])
        data['is_explicit'] = results['parental_warning']
        data['language'] = results['language']
        data['label'] = results['vendor_name']
        data['release_date'] = results['release_date']
        data['play_count'] = results['play_ct']
        data['favorite_count'] = results['total_favourite_count']
        data['song_url'] = f"https://gaana.com/song/{data['seokey']}"
        data['album_url'] = f"https://gaana.com/album/{data['album_seokey']}"
        data['images'] = {'urls': {}}
        data['images']['urls']['large_artwork'] = (results['artwork_large'])
        data['images']['urls']['medium_artwork'] = (results['artwork_web'])
        data['images']['urls']['small_artwork'] = (results['artwork'])
        data['stream_urls'] = {'urls': {}}
        base_url = await functions.decryptLink(results['urls']['medium']['message'])
        
        data['stream_urls']['urls']['very_high_quality'] = base_url.replace("64.mp4", "320.mp4")
        data['stream_urls']['urls']['high_quality'] = base_url.replace("64.mp4", "128.mp4")
        data['stream_urls']['urls']['medium_quality'] = base_url
        data['stream_urls']['urls']['low_quality'] = base_url.replace("64.mp4", "16.mp4")
        return data