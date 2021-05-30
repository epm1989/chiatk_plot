import glob
import os
import signal
import subprocess
import datetime
import re
from typing import List, AnyStr
from typing.io import TextIO

from app.models.plot import Plot, Queue, StatusQueueType, StatusType
from app.settings import working_dir

from app.utils import is_windows


class PlotController:
    def __init__(self):
        self.k = '32'
        self.b = '4000'
        self.r = '2'
        self.u = '128'
        self.t = '/home/epm1989c7/Pictures/chia/temp'
        self.d = '/home/epm1989c7/Pictures/chia/persistent'
        self.f = '8dd0a6848abc98b91721f8dc524b4264ef57fd53d9b651106b38d2299481d7eb3568dc0c1b578b85692964973ae4aa68'
        self.p = '83c107cf162c1b22f0fcdedb998e9da81229f8ba1ad058ec3f9411e939ab90b4a24732726ec793c6a27b2598ef171976'

    @staticmethod
    def start(command: List[AnyStr], log_file: TextIO):
        kwargs = {}

        if is_windows():
            flags = 0
            flags |= 0x00000008
            kwargs = {
                'creationflags': flags,
            }
        process = subprocess.Popen(command, stdout=log_file, stderr=log_file, shell=False, **kwargs)
        return process

    async def queue(self):
        command = ['/usr/lib/chia-blockchain/resources/app.asar.unpacked/daemon/chia',
                   'plots', 'create', '-k', self.k, '-b', self.b,
                   '-t', self.t, '-d', self.d,
                   '-r', self.r, '-u', self.u,
                   '-f', self.f,
                   '-p', self.p]

        return await Queue.create(command=' '.join(command))

    async def create(self):

        task_pending = await Queue.filter(status=StatusQueueType.WAITING).order_by('created').limit(1)
        if not task_pending:
            return True
        task = task_pending[0]
        command = task.command.split(' ')
        unix_time = str(round(datetime.datetime.utcnow().timestamp()))
        log_file_path = working_dir + '/logs/temp_{{datetime}}.log'
        log_file_path = re.sub('{{datetime}}', unix_time, log_file_path)
        log_file = open(log_file_path, 'a')

        process = self.start(command, log_file)
        if process:
            plot = await Plot.create(t=self.t, d=self.d, r=self.r, u=self.u,
                                     f=self.f, p=self.p, k=self.k, b=self.b,
                                     pid=str(process.pid), log_file=log_file_path)
            task.status = StatusQueueType.RUNNING
            task.plot = plot
            await task.save()
            self.refresh()
            return True
        return False

    @staticmethod
    def kill(pid: int):
        try:
            os.kill(pid, signal.SIGTERM)
            return True
        except ProcessLookupError as err:
            return False

    @staticmethod
    def delete_plot_temp_files(plot_id: str, t: str):
        files_name = []

        os.chdir(t)
        for file in glob.glob(f"plot-*{plot_id}*.tmp"):
            files_name.append(f"{t}/{file}")

        for file in files_name:
            if os.path.isfile(file):
                os.remove(file)
        os.chdir(working_dir)

    @classmethod
    async def stop(cls, pid: int):
        if plot := await Plot.get_or_none(pid=str(pid)):
            plot_id = plot.plot_id
            t = plot.t
            if not cls.kill(pid):
                return False
            print(plot_id, t)
            cls.delete_plot_temp_files(plot_id=plot_id, t=t)
            plot.status = StatusType.DELETED
            await plot.save()
            queue = await Queue.get(plot=plot)
            queue.status = StatusQueueType.STOPPED
            await queue.save()
            return True
        return False

    @staticmethod
    def refresh():
        result = subprocess.Popen(['python', f'{working_dir}/manager.py', 'status'])
        return result

    @staticmethod
    async def all():
        PlotController.refresh()
        return await Plot.filter(status=StatusType.OPEN).values('id', 'pid', 'plot_id', 't', 'd',
                                                                'log_file', 'phase', 'progress',
                                                                'temp_size', 'status')
