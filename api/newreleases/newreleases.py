class NewReleases():
    async def get_new_releases(self, language: str, limit: int) -> dict:
        aiohttp = self.aiohttp
        endpoints = self.api_endpoints
        errors = self.errors
        response = await aiohttp.post(endpoints.new_releases_url + language)
        result = await response.json()
        track_seokeys = []
        album_seokeys = []
        for i in range(0,int(limit)):
            try:
                if result['entities'][int(i)]['entity_type'] == "AL":
                    album_seokeys.append(result['entities'][int(i)]['seokey'])
                elif result['entities'][int(i)]['entity_type'] == "TR":
                    track_seokeys.append(result['entities'][int(i)]['seokey'])
            except (IndexError, TypeError, KeyError):
                pass
        if len(track_seokeys) and len(album_seokeys) == 0:
            return await errors.no_results()
        data = {}
        data['tracks'] = await self.get_track_info(track_seokeys)
        data['albums'] = await self.get_album_info(album_seokeys, False)
        return data