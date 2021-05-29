import os
import asyncio
from app.models import run
from tortoise import run_async
from app.controllers import PlotController


async def run_app():

    await run(generate_schemas=True)
    #plot = PlotController()
    #await plot.create()

    await PlotController().delete_plot_temp_files(plot_id='89a016a2f891f900234f84ee6757da5d116b6cf375c7df0361cbe29a2551267f',
                                                  t='/home/epm1989c7/Pictures/chia/temp')


if __name__ == '__main__':

    if not os.path.exists('logs'):
        os.makedirs('logs')
    run_async(run_app())
