import subprocess


class TKstStart(object):
    """class use to start and stop the kst plotting prog"""

    def __init__(self):
        self.PlotterKst = None

    def start(self, fileNameKst):
        self.stop()
        self.PlotterKst = subprocess.Popen(["kst2", fileNameKst, "shell=True", "stdout=subprocess.PIPE"])

    def stop(self):
        if self.PlotterKst:
            self.PlotterKst.kill()
            self.PlotterKst.wait()
            self.PlotterKst = None
