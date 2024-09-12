from aiohttp import web

# Handler for the root route
async def hello(request):
    return web.Response(text="Hello, World!")

# Create the application instance
app = web.Application()

# Add route to the app
app.add_routes([web.get('/', hello)])

# Start the app
if __name__ == '__main__':
    web.run_app(app)