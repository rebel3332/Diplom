from datetime import datetime, timedelta
import pandas as pd



class Loging:
    def __init__(self) -> None:
        self.LOG_WRITE_TO_FILE = True

    def __log(self, level, *args):
        """Ведет лог в терминале сервера и, если требуется, сохраняет его в файл.
        
        ПРИМЕР вызова:  log('INFO', 'The Model is loaded')
        --> ggdsfgfdgfdsgs"""

        d = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        text = f'{d} [{level}] ' + " ".join(args)
        # print(f'{d} [{level}] ', *args)
        print(text)
        if self.LOG_WRITE_TO_FILE:
            with open('logs/log.txt', 'a') as logFile:
                logFile.write(text+'\n')


    def INFO(self, *args):
        self.__log('INFO', *args)

    def WARM(self, *args):
        self.__log('WARM', *args)

    def ERROR(self, *args):
        self.__log('ERROR', *args)


def loadData(*args, **kwargs):
    """Загружает таблицу с данными с сайта, 
    Входные параметры: weeks=10, days и т.д."""
    # Расчет timestamps для URL
    dateEnd = int(datetime.timestamp(datetime.now()))
    dateperiod = int(timedelta(*args, **kwargs).total_seconds()) # Загружаю одну дополнительную неделю т.к. close на последней неделе может быть еще не закрыт.
    dateStart = dateEnd - dateperiod

    url = f'https://query1.finance.yahoo.com/v7/finance/download/AMZN?period1={dateStart}&period2={dateEnd}&interval=1wk&events=history&includeAdjustedClose=true'
    data = pd.read_csv(url)
    # print(data)
    return data

loging = Loging()