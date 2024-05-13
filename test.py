import server, asyncio
async def main():
    test = server.server(guild_id=1234, channel=1234, class_identifier='3H')

    await test.update()

    await test.update()

if __name__ == '__main__': asyncio.run(main())