class Errors:
    async def invalid_seokey(self) -> dict:
        return {"error": "Invalid Seokey!"}
    async def no_results(self) -> dict:
        return {"error": "Unable to find any results!"}