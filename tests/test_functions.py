import pytest
from api.functions import Functions

functions = Functions()

@pytest.mark.asyncio
async def test_decryptLink():
    encrypted_link = """/PXDlMo67L4ssymkjHOGPNgaoh8Ou9LKJSyF01YhszT3suEhlTJHPnFc++I6/5mIBC0
        1vAoAWio8FxdsItmcEDREN4A9UQ21NaErv7ADx77RSbVb60Z1C8p16Od5bQ2CA4oKJN9sj1F1U0
        +g6EGRvlPd0fh05Rz8im1tL4bbRAwUIHPflvlsjVOrQ5TgREsX9iTSfRMeuotyc3Dy5nMagK4/s/GUXY
        Gkzf1nb+zVUrLem1LjMozs+su0wKsMwMHK"""
    decrypted_link = """https://vodhlsgaana.akamaized.net/hls/3/3487503/32408795/64.mp4.master.m3u8?hdnts=st=1750928699~exp=1750943099~acl=/*~hmac=d7eea4e6396b27dc8591c405cc57fa205e6cca82dd831406055e01bebe493632"""
    
    result = await functions.decryptLink(encrypted_link.strip())
    assert result == decrypted_link.strip()

@pytest.mark.asyncio
async def test_unpad():
    padded = "GaanaPy" + chr(2) + chr(2)
    result = await functions.unpad(padded)
    assert result == "GaanaPy"
    with pytest.raises(IndexError):
        await functions.unpad("")
    
@pytest.mark.asyncio
async def test_findArtistNames():
    artists = [{"name": "Gaana"}, {"name": "Py"}]
    result = await functions.findArtistNames(artists)
    assert result == "Gaana, Py"
    assert await functions.findArtistNames([]) == ""
    
@pytest.mark.asyncio
async def test_findArtistSeoKeys():
    seokeys = [{"seokey": "Gaana"}, {"seokey": "Py"}]
    result = await functions.findArtistSeoKeys(seokeys)
    assert result == "Gaana, Py"
    assert await functions.findArtistSeoKeys([]) == ""
    
@pytest.mark.asyncio
async def test_findArtistIds():
    artist_ids = [{"artist_id": "Gaana"}, {"artist_id": "Py"}]
    result = await functions.findArtistIds(artist_ids)
    assert result == "Gaana, Py"
    assert await functions.findArtistIds([]) == ""
    
@pytest.mark.asyncio
async def test_isExplicit():
    is_explicit = 1
    is_not_explicit = 0
    explicit_result = await functions.isExplicit(is_explicit)
    not_explicit_result = await functions.isExplicit(is_not_explicit)
    assert explicit_result == True
    assert not_explicit_result == False