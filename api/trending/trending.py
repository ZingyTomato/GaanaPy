class Trending():
    async def get_trending(self, language: str, limit: int) -> dict:
        aiohttp = self.aiohttp
        endpoints = self.api_endpoints
        errors = self.errors
        headers = {'Cookie': f'__ul={language};'}
        response = await aiohttp.post(endpoints.trending_url, headers=headers)
        result = await response.json()
        track_seokeys = []
        for i in range(0,int(limit)):
            try:
                track_seokeys.append(result['entities'][int(i)]['seokey'])
            except (IndexError, TypeError, KeyError):
                pass
        if len(track_seokeys) == 0:
          return await errors.no_results()
        track_data = await self.get_track_info(track_seokeys)
        return track_data