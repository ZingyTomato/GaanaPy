import asyncio

class Artists:
    async def search_artists(self, search_query: str, limit: int) -> list:
        endpoints = self.api_endpoints
        errors = self.errors
        result = await self._safe_request("POST", endpoints.search_artists_url + search_query)
        if isinstance(result, dict) and "error" in result:
            return result
        artist_ids = []
        gd = (result.get('gr') or [{}])[0].get('gd', [])
        for i in range(min(limit, len(gd))):
            seo = gd[i].get('seo') if isinstance(gd[i], dict) else None
            if seo:
                artist_ids.append(seo)
        if len(artist_ids) == 0:
            return await errors.no_results()
        artist_info = await self.get_artist_info(artist_ids, False)
        return artist_info

    async def get_artist_info(self, artist_id: list, info: bool, limit: int = 10, page: int = 1) -> list:
        endpoints = self.api_endpoints
        errors = self.errors
        results = await asyncio.gather(*[
            self._safe_request("POST", endpoints.artist_details_url + i)
            for i in artist_id
        ])
        artist_info = []
        for result in results:
            if isinstance(result, dict) and "error" in result:
                continue
            artist_info.append(await self.format_json_artists(result, limit, page, info=info))
        if len(artist_info) == 0:
            return await errors.no_results()
        return artist_info

    async def get_top_tracks(self, artist_id: str, limit: int = 10, page: int = 1) -> dict:
        endpoints = self.api_endpoints
        result = await self._safe_request("POST", endpoints.artist_top_tracks + artist_id)
        if isinstance(result, dict) and "error" in result:
            return result
        track_seokeys = []
        for track in result.get('entities', []):
            seo = track.get('seokey') if isinstance(track, dict) else None
            if seo:
                track_seokeys.append(seo)
        total = len(track_seokeys)
        offset = (page - 1) * limit
        paginated_seokeys = track_seokeys[offset:offset + limit]
        tracks = await self.get_track_info(paginated_seokeys)
        if isinstance(tracks, dict) and "error" in tracks:
            return {"tracks": [], "total": total}
        return {"tracks": tracks, "total": total}

    async def get_similar_artists(self, artist_id: str, limit: int) -> dict:
        endpoints = self.api_endpoints
        errors = self.errors
        result = await self._safe_request("GET", endpoints.similar_artists_url + artist_id)
        if isinstance(result, dict) and "error" in result:
            return result
        entities = []
        entities_list = result.get('entities', [])
        for i in range(min(limit, len(entities_list))):
            entities.append(entities_list[i])
        if len(entities) == 0:
            return await errors.no_results()
        similar_artists = []
        similar_artists.extend(await asyncio.gather(*[self.format_json_similar_artists(entity) for entity in entities]))
        return similar_artists

    async def format_json_artists(self, results: dict, limit: int = 10, page: int = 1, info: bool = False) -> dict:
        errors = self.errors
        data = {}

        artist_list = results.get('artist')
        if not artist_list or not isinstance(artist_list, list) or len(artist_list) == 0:
            return await errors.invalid_seokey()
        artist = artist_list[0]

        seokey = artist.get('seokey')
        if not seokey:
            return await errors.invalid_seokey()

        data['seokey'] = seokey
        data['artist_id'] = artist.get('artist_id', '')
        data['name'] = artist.get('name', '')
        data['song_count'] = artist.get('songs', '')
        data['album_count'] = artist.get('albums', '')
        data['favorite_count'] = artist.get('favorite_count', '')
        data['artist_url'] = f"https://gaana.com/artist/{data['seokey']}"
        atw = artist.get('atw', '')
        data['images'] = {'urls': {}}
        data['images']['urls']['large_artwork'] = atw.replace("size_m", "size_l") if atw else ''
        data['images']['urls']['medium_artwork'] = atw
        data['images']['urls']['small_artwork'] = atw.replace("size_m", "size_s") if atw else ''
        if info:
            top_tracks_data = await self.get_top_tracks(data['artist_id'], limit, page)
            data['top_tracks'] = top_tracks_data.get('tracks', [])
            data['total_tracks'] = top_tracks_data.get('total', 0)
        return data

    async def format_json_similar_artists(self, results: dict) -> dict:
        errors = self.errors
        data = {}

        seokey = results.get('seokey')
        if not seokey:
            return await errors.invalid_seokey()

        data['seokey'] = seokey
        data['artist_id'] = results.get('entity_id', '')
        data['name'] = results.get('name', '')
        entity_info = results.get('entity_info') or []
        data['song_count'] = entity_info[1].get('value', '') if len(entity_info) > 1 else ''
        data['album_count'] = entity_info[0].get('value', '') if len(entity_info) > 0 else ''
        data['favorite_count'] = results.get('favorite_count', '')
        data['artist_url'] = f"https://gaana.com/artist/{data['seokey']}"
        atw = results.get('atw', '')
        data['images'] = {'urls': {}}
        data['images']['urls']['large_artwork'] = atw.replace("size_m", "size_l") if atw else ''
        data['images']['urls']['medium_artwork'] = atw
        data['images']['urls']['small_artwork'] = atw.replace("size_m", "size_s") if atw else ''
        return data
