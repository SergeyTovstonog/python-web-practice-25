import asyncio


async def baz():
    await asyncio.sleep(1)
    return 'Hello world!'


async def main() -> str:
    r = baz()
    print(r)  # coroutine
    result = await r  # result
    print(f'In function: {result}')
    return result


if __name__ == '__main__':
    msg = asyncio.run(main())
    print(f'In main process: {msg}')


