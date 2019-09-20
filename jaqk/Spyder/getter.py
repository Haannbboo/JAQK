import asyncio
import aiohttp


async def getter(url, timeout=20, error=True, retry=0, cnt=0):
    """Main get function for most the website crawler

    It uses asynchronous coroutine and asynchronous request sessions (aiohttp)

    Args:
        url: str - target url
        timeout: int - timeout set for each request, default 10 second (recommend >10)
        error: bool - Recursive error handler, identify state of request
        retry: int - time of retry
        cnt: int - count time of retry

    Returns:
        if successfully requested, returns html information in string
        else, returns None
    """
    if cnt > retry:
        return
        # error = "Failed to request data from url {}".format(url)
        # raise GetterRequestError(error)

    user_agent = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 \
        Safari/537.36', ]
    headers = {
        'User-Agent': user_agent[0],  # User agent
    }

    try:
        # aiohttp client request session, asynchronous request library
        async with aiohttp.ClientSession(headers=headers, connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            r = await session.get(url, timeout=timeout)
            html = await r.text()
        error = False
    # except (aiohttp.ClientTimeout, aiohttp.ClientConnectionError) as e:
    except asyncio.TimeoutError:
        error = True

    if not error:
        return html
    else:
        await getter(url, timeout, error=error, cnt=cnt+1)  # retry
