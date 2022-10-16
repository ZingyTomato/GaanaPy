class Errors():
    async def invalid_seokey(self) -> dict:
        return {"ERROR": "Invalid Seokey!"}
    async def no_results(self) -> dict:
        return {'ERROR': 'Unable to find any results!'}