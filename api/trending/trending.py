class Trending:
    async def get_trending(self, language: str, limit: int) -> dict:
        endpoints = self.api_endpoints
        errors = self.errors
        headers = {'Cookie': f'__ul={language};'}
        result = await self._safe_request("POST", endpoints.trending_url, headers=headers)
        if isinstance(result, dict) and "error" in result:
            return result
        track_seokeys = []
        entities_list = result.get('entities', [])
        for i in range(min(limit, len(entities_list))):
            seo = entities_list[i].get('seokey') if isinstance(entities_list[i], dict) else None
            if seo:
                track_seokeys.append(seo)
        if len(track_seokeys) == 0:
            return await errors.no_results()
        track_data = await self.get_track_info(track_seokeys)
        return track_data
