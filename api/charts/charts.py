import asyncio

class Charts:
    async def get_charts(self, limit: int) -> list:
        aiohttp = self.aiohttp
        endpoints = self.api_endpoints
        errors = self.errors
        response = await aiohttp.post(endpoints.charts_url + str(limit))
        result = await response.json()
        chart_info = []
        chart_info.extend(await asyncio.gather(*[self.format_json_charts(result['entities'][int(i)]) for i in range(0, int(limit))]))
        return chart_info

    async def format_json_charts(self, results: dict) -> dict:
        functions = self.functions
        data = {}
        data['seokey'] = results['seokey']
        data['playlist_id'] = results['entity_id']
        data['title'] = results['name']
        data['language'] = results['language']
        data['favorite_count'] = results['favorite_count']
        data['is_explicit'] = await functions.isExplicit(results['entity_info'][6]['value'])
        data['play_count'] = results['entity_info'][-1]['value']
        data['playlist_url'] = f"https://gaana.com/playlist/{data['seokey']}"
        data['images'] = {'urls': {}}
        data['images']['urls']['large_artwork'] = (results['atw']).replace("size_m.jpg", "size_l.jpg")
        data['images']['urls']['medium_artwork'] = (results['atw'])
        data['images']['urls']['small_artwork'] = (results['atw']).replace("size_m.jpg", "size_s.jpg")
        return data