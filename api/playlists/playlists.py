class Playlists:
    async def get_playlist_info(self, playlist_id: str) -> dict:
        endpoints = self.api_endpoints
        errors = self.errors
        result = await self._safe_request("POST", endpoints.playlist_details_url + playlist_id)
        if isinstance(result, dict) and "error" in result:
            return result
        track_count = result.get('count')
        if not track_count:
            return await errors.no_results()
        track_ids = []
        tracks = result.get('tracks', [])
        for i in range(min(int(track_count), len(tracks))):
            seo = tracks[i].get('seokey') if isinstance(tracks[i], dict) else None
            if seo:
                track_ids.append(seo)
        if len(track_ids) == 0:
            return await errors.no_results()
        track_data = await self.get_track_info(track_ids)
        return track_data
