class NewReleases:
    async def get_new_releases(self, language: str, limit: int) -> dict:
        endpoints = self.api_endpoints
        errors = self.errors
        result = await self._safe_request("POST", endpoints.new_releases_url + language)
        if isinstance(result, dict) and "error" in result:
            return result
        track_seokeys = []
        album_seokeys = []
        entities_list = result.get('entities', [])
        for i in range(min(limit, len(entities_list))):
            entity = entities_list[i]
            if not isinstance(entity, dict):
                continue
            etype = entity.get('entity_type')
            seo = entity.get('seokey')
            if etype == "AL" and seo:
                album_seokeys.append(seo)
            elif etype == "TR" and seo:
                track_seokeys.append(seo)
        if len(track_seokeys) == 0 and len(album_seokeys) == 0:
            return await errors.no_results()
        data = {}
        data['tracks'] = await self.get_track_info(track_seokeys)
        data['albums'] = await self.get_album_info(album_seokeys, False)
        return data
