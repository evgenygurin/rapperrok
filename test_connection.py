"""Test connection to AI Music API."""
import asyncio
import os
import httpx

async def test_credits():
    api_key = os.getenv('AIMUSIC_API_KEY', 'test')
    url = 'https://api.aimusicapi.ai/v1/credits'

    print(f'Testing URL: {url}')
    print(f'API Key present: {bool(api_key and api_key != "test")}')

    async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
        try:
            response = await client.get(
                url,
                headers={'Authorization': f'Bearer {api_key}'}
            )
            print(f'\n✓ Status: {response.status_code}')
            print(f'  Final URL: {response.url}')
            print(f'  Response: {response.text[:500]}')
        except Exception as e:
            print(f'\n✗ Error: {type(e).__name__}: {e}')

asyncio.run(test_credits())
