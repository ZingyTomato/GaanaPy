class Playlists():
    async def get_playlist_info(self, playlist_id: str) -> dict:
        aiohttp = self.aiohttp
        endpoints = self.api_endpoints
        errors = self.errors
        response = await aiohttp.post(endpoints.playlist_details_url + playlist_id)
        result = await response.json()
        track_count = result['count']
        track_ids = []
        for i in range(0,int(track_count)):
            try:
                track_ids.append(result['tracks'][int(i)]['seokey'])
            except (IndexError, TypeError, KeyError):
                pass
        track_data = await self.get_track_info(track_ids)
        return track_data