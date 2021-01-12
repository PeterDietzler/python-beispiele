

#ifdef WINDOWS
    if self.recievedList[0] == '$batV':
        try:
            self.batVoltage = (round(float(self.recievedList[1]), 2))
            f = open(cwd + "/log/PlotBat.txt", 'a+')
            f.write("{}\n".format(time.strftime("%X,") + self.receivedMessage))
            f.close()
        except Exception as e:
            print('$batV received: ', e)
#endif

#ifdef PI
#PRE     if self.recievedList[0] == '$per':
#PRE         try:
#PRE             f = open(cwd + "/log/PlotPer.txt", 'a+')
#PRE             f.write("{}\n".format(self.receivedMessage))
#PRE             f.close()
#PRE         except Exception as e:
#PRE             print('per: ', e)
#endif

