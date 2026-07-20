import asyncio

class Songs:
    async def search_songs(self, search_query: str, limit: int) -> list:
        endpoints = self.api_endpoints
        errors = self.errors
        result = await self._safe_request("POST", endpoints.search_songs_url + search_query)
        if isinstance(result, dict) and "error" in result:
            return result
        track_ids = []
        gd = (result.get('gr') or [{}])[0].get('gd', [])
        for i in range(min(limit, len(gd))):
            seo = gd[i].get('seo') if isinstance(gd[i], dict) else None
            if seo:
                track_ids.append(seo)
        if len(track_ids) == 0:
            return await errors.no_results()
        track_info = await self.get_track_info(track_ids)
        return track_info

    async def get_track_info(self, track_id: list) -> list:
        endpoints = self.api_endpoints
        errors = self.errors
        results = await asyncio.gather(*[
            self._safe_request("POST", endpoints.song_details_url + i)
            for i in track_id
        ])
        track_info = []
        for result in results:
            if isinstance(result, dict) and "error" in result:
                continue
            tracks = result.get('tracks')
            if not tracks:
                continue
            track_info.extend(await asyncio.gather(*[self.format_json_songs(t) for t in tracks]))
        if len(track_info) == 0:
            return await errors.no_results()
        return track_info

    async def format_json_songs(self, results: dict) -> dict:
        functions = self.functions
        errors = self.errors
        data = {}

        seokey = results.get('seokey')
        if not seokey:
            return await errors.invalid_seokey()

        data['seokey'] = seokey
        data['album_seokey'] = results.get('albumseokey', '')
        data['track_id'] = results.get('track_id', '')
        data['title'] = results.get('track_title', '')
        data['artists'] = await functions.findArtistNames(
            results.get('artist') or []
        )
        data['artist_seokeys'] = await functions.findArtistSeoKeys(
            results.get('artist') or []
        )
        data['artist_ids'] = await functions.findArtistIds(
            results.get('artist') or []
        )
        artist_detail = results.get('artist_detail')
        data['artist_image'] = (
            artist_detail[0].get('atw', '')
            if artist_detail and isinstance(artist_detail, list) and len(artist_detail) > 0
            else ''
        )
        data['album'] = results.get('album_title', '')
        data['album_id'] = results.get('album_id', '')
        data['duration'] = results.get('duration', '')
        data['popularity'] = results.get('popularity', '')
        data['genres'] = await functions.findGenres(
            results.get('gener') or []
        )
        data['is_explicit'] = await functions.isExplicit(
            results.get('parental_warning', 0)
        )
        data['language'] = results.get('language', '')
        data['label'] = results.get('vendor_name', '')
        data['release_date'] = results.get('release_date', '')
        data['play_count'] = results.get('play_ct', '')
        data['favorite_count'] = results.get('total_favourite_count', '')
        data['song_url'] = f"https://gaana.com/song/{data['seokey']}"
        data['album_url'] = (
            f"https://gaana.com/album/{data['album_seokey']}"
            if data['album_seokey'] else ''
        )
        data['images'] = {'urls': {}}
        data['images']['urls']['large_artwork'] = results.get('artwork_large', '')
        data['images']['urls']['medium_artwork'] = results.get('artwork_web', '')
        data['images']['urls']['small_artwork'] = results.get('artwork', '')
        data['stream_urls'] = {'urls': {}}

        try:
            medium = results.get('urls', {}).get('medium', {})
            if medium.get('message'):
                base_url = await functions.decryptLink(medium['message'])
                data['stream_urls']['urls']['very_high_quality'] = (
                    base_url.replace("64.mp4", "320.mp4") if base_url else ""
                )
                data['stream_urls']['urls']['high_quality'] = (
                    base_url.replace("64.mp4", "128.mp4") if base_url else ""
                )
                data['stream_urls']['urls']['medium_quality'] = base_url
                data['stream_urls']['urls']['low_quality'] = (
                    base_url.replace("64.mp4", "16.mp4") if base_url else ""
                )
            else:
                raise KeyError
        except (KeyError, AttributeError):
            data['stream_urls']['urls']['very_high_quality'] = ""
            data['stream_urls']['urls']['high_quality'] = ""
            data['stream_urls']['urls']['medium_quality'] = ""
            data['stream_urls']['urls']['low_quality'] = ""

        return data
