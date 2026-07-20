import asyncio


class Albums:
    async def search_albums(self, search_query: str, limit: int) -> list:
        endpoints = self.api_endpoints
        errors = self.errors
        result = await self._safe_request("POST", endpoints.search_albums_url + search_query)
        if isinstance(result, dict) and "error" in result:
            return result
        album_ids = []
        gd = (result.get('gr') or [{}])[0].get('gd', [])
        for i in range(min(limit, len(gd))):
            seo = gd[i].get('seo') if isinstance(gd[i], dict) else None
            if seo:
                album_ids.append(seo)
        if len(album_ids) == 0:
            return await errors.no_results()
        album_info = await self.get_album_info(album_ids, False)
        return album_info

    async def get_album_info(self, album_id: list, info: bool) -> list:
        endpoints = self.api_endpoints
        errors = self.errors
        results = await asyncio.gather(*[
            self._safe_request("POST", endpoints.album_details_url + i)
            for i in album_id
        ])
        album_info = []
        for result in results:
            if isinstance(result, dict) and "error" in result:
                continue
            album_info.append(await self.format_json_albums(result, info=info))
        if len(album_info) == 0:
            return await errors.no_results()
        return album_info

    async def get_album_tracks(self, album_id: str) -> list:
        endpoints = self.api_endpoints
        result = await self._safe_request("POST", endpoints.album_details_url + album_id)
        if isinstance(result, dict) and "error" in result:
            return result
        track_seokeys = []
        for i in result.get('tracks', []):
            seo = i.get('seokey') if isinstance(i, dict) else None
            if seo:
                track_seokeys.append(seo)
        result = await self.get_track_info(track_seokeys)
        return result

    async def format_json_albums(self, results: dict, info: bool = False) -> dict:
        functions = self.functions
        errors = self.errors
        data = {}

        album = results.get('album')
        if not album or not album.get('seokey'):
            return await errors.no_results()

        data['seokey'] = album['seokey']
        data['album_id'] = album.get('album_id', '')
        data['title'] = album.get('title', '')
        try:
            data['artists'] = await functions.findArtistNames(
                album.get('artist') or []
            )
            tracks = results.get('tracks')
            first_track_artist = (
                tracks[0].get('artist') or []
                if tracks and isinstance(tracks, list) and len(tracks) > 0
                else []
            )
            data['artist_seokeys'] = await functions.findArtistSeoKeys(first_track_artist)
            data['artist_ids'] = await functions.findArtistIds(first_track_artist)
        except (KeyError, IndexError):
            data['artists'] = ""
            data['artist_seokeys'] = ""
            data['artist_ids'] = ""
        data['duration'] = album.get('duration', '')
        data['is_explicit'] = await functions.isExplicit(
            album.get('parental_warning', 0)
        )
        data['language'] = album.get('language', '')
        data['label'] = album.get('recordlevel', '')
        data['track_count'] = album.get('trackcount', '')
        data['release_date'] = album.get('release_date', '')
        data['play_count'] = album.get('al_play_ct', '')
        data['favorite_count'] = album.get('favorite_count', '')
        data['album_url'] = f"https://gaana.com/album/{data['seokey']}"
        artwork = album.get('artwork', '')
        data['images'] = {'urls': {}}
        data['images']['urls']['large_artwork'] = artwork.replace("size_s.jpg", "size_l.jpg") if artwork else ''
        data['images']['urls']['medium_artwork'] = artwork.replace("size_s.jpg", "size_m.jpg") if artwork else ''
        data['images']['urls']['small_artwork'] = artwork

        if info:
            data['tracks'] = await self.get_album_tracks(data['seokey'])
        return data
