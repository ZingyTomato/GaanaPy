import asyncio

class Charts:
    async def get_charts(self, limit: int) -> list:
        endpoints = self.api_endpoints
        errors = self.errors
        result = await self._safe_request("POST", endpoints.charts_url + str(limit))
        if isinstance(result, dict) and "error" in result:
            return result
        entities = []
        entities_list = result.get('entities', [])
        for i in range(min(limit, len(entities_list))):
            entities.append(entities_list[i])
        if len(entities) == 0:
            return await errors.no_results()
        chart_info = []
        chart_info.extend(await asyncio.gather(*[self.format_json_charts(entity) for entity in entities]))
        return chart_info

    async def format_json_charts(self, results: dict) -> dict:
        functions = self.functions
        data = {}
        data['seokey'] = results.get('seokey', '')
        data['playlist_id'] = results.get('entity_id', '')
        data['title'] = results.get('name', '')
        data['language'] = results.get('language', '')
        data['favorite_count'] = results.get('favorite_count', '')
        entity_info = results.get('entity_info') or []
        data['is_explicit'] = await functions.isExplicit(
            entity_info[6].get('value', 0) if len(entity_info) > 6 else 0
        )
        data['play_count'] = entity_info[-1].get('value', '') if entity_info else ''
        data['playlist_url'] = f"https://gaana.com/playlist/{data['seokey']}" if data['seokey'] else ''
        atw = results.get('atw', '')
        data['images'] = {'urls': {}}
        data['images']['urls']['large_artwork'] = atw.replace("size_m.jpg", "size_l.jpg") if atw else ''
        data['images']['urls']['medium_artwork'] = atw
        data['images']['urls']['small_artwork'] = atw.replace("size_m.jpg", "size_s.jpg") if atw else ''
        return data
