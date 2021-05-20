from aiohttp import web
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

async def test(request):
    logger.info('Handler function called')
    logger.info('log from handler')
    # a = 1/0
    return web.Response(text="Hello")

@web.middleware
async def error_middleware(request, handler):
    logger.info('error middleware called')
    try:
        response = await handler(request)
    # except HttpProcessingError as e:
    #     logger.info('from http_exceptions.HttpProcessingError')
    #     logger.error(e)
    #     return web.json_response({'error': e.reason}, status=e.status_code)
    except web.HTTPException as e:
        logger.info('from web.HTTPException')
        logger.error(e)
        return web.json_response({'error': e.reason}, status=e.status_code)
        # raise
    except Exception as e:
        logger.info('from Exception')
        logger.error(e)
        return web.json_response({'error': e.reason}, status=500)
    else:
        if response.status >= 400:
            logger.info('from >= 400')
            logger.error(response.status)
        return response


@web.middleware
async def middleware1(request, handler):
    logger.info('Middleware 1 called')
    # response = await handler(request)
    # logger.info(f'metric sended {response.status}')
    # return response
    try:
        response = await handler(request)
    except web.HTTPException as e:
        logger.error(e)
        logger.info(f'metric sended {e.status_code}')
        raise
    except BaseException as e:
        logger.error(e)
        logger.info(f'metric sended {e.status_code}')
        return web.json_response({'error': e.reason}, status=500)
    else:
        logger.info(f'metric sended {response.status}')
        return response

        
    # status_code = response.status
    # logger.info(f'{status_code}')
    logger.info('Middleware 1 finished')
    # return response

@web.middleware
async def middleware2(request, handler):
    logger.info('Middleware 2 called')
    response = await handler(request)
    logger.info('Middleware 2 finished')
    return response

middlewares = []
middlewares.append(error_middleware)
middlewares.append(middleware1)
middlewares.append(middleware2)

app = web.Application(middlewares=middlewares)

app.router.add_get('/', test)

web.run_app(app)

