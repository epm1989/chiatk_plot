import os
import asyncio
from app.models import run
from tortoise import run_async
from app.controllers import PlotController
import subprocess


async def run_app():

    await run(generate_schemas=True)
    plot = PlotController()
    #await plot.queue()
    await plot.create()
    await asyncio.sleep(2)
    #PlotController().delete_plot_temp_files(plot_id='26e166159e87c293b516cfa2355a7b56c44d1badaa7959515cdb5bf0c1bb8943',
    #                                              t='/home/epm1989c7/Pictures/chia/temp')

    result = subprocess.Popen(['python', 'manager.py', 'status'])
    #print(result)


if __name__ == '__main__':

    if not os.path.exists('logs'):
        os.makedirs('logs')
    run_async(run_app())
