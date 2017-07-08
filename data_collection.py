import requests
from pandas import *
from numpy import *
from datetime import *
import os


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)     Chrome/37.0.2049.0 Safari/537.36'
}

src_dir = os.getcwd()
csv_dir = os.path.join(src_dir, "CSV_price")


def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def RepresentsFloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


class Quote(object):
    CLASS_AND_FUNC_FMT = '%Y%m%d'
    CSV_INPUT_AND_OUTPUT_FMT = "%Y-%m-%d"

    def __init__(self, symbol):
        self.symbol = symbol
        self.date, self.time, self.open_, self.high, self.low, self.close, self.volume = ([] for _ in range(7))

    def append(self, dt, open_, high, low, close, volume):
        if RepresentsFloat(open_) and RepresentsFloat(high) and RepresentsFloat(low) and RepresentsFloat(close) and \
                RepresentsFloat(volume):
            self.date.append(dt)
            self.open_.append(float(open_))
            self.high.append(float(high))
            self.low.append(float(low))
            self.close.append(float(close))
            self.volume.append(float(volume))

    def prepend(self, dt, open_, high, low, close, volume):
        if RepresentsFloat(open_) and RepresentsFloat(high) and RepresentsFloat(low) and RepresentsFloat(close) and \
                RepresentsFloat(volume):
            self.date = [dt] + self.date
            self.open_ = [float(open_)] + self.open_
            self.high = [float(high)] + self.high
            self.low = [float(low)] + self.low
            self.close = [float(close)] + self.close
            self.volume = [float(volume)] + self.volume

    def return_list(self):
        return [d.strftime(self.CLASS_AND_FUNC_FMT) for d in
                self.date], self.open_, self.high, self.low, self.close, self.volume

    def get_vol(self, date_b=None, date_e=None):
        if date_e is None or date_b is None:
            return [d.strftime(self.CLASS_AND_FUNC_FMT) for d in self.date], self.volume
        else:
            date_b = datetime.strptime(date_b, "%Y%m%d")
            date_e = datetime.strptime(date_e, "%Y%m%d")

            b, e = 0, len(self.date) - 1

            while b < len(self.date) and date_b > self.date[b]:
                b += 1

            while e >= 0 and date_e < self.date[e]:
                e -= 1

            return [d.strftime(self.CLASS_AND_FUNC_FMT) for d in self.date[b:e+1]], self.volume[b:e+1]

    def get_price(self, date_b=None, date_e=None):
        if date_e is None or date_b is None:
            return [d.strftime(self.CLASS_AND_FUNC_FMT) for d in self.date], self.close
        else:
            date_b = datetime.strptime(date_b, "%Y%m%d")
            date_e = datetime.strptime(date_e, "%Y%m%d")

            b, e = 0, len(self.date) - 1

            while b < len(self.date) and date_b > self.date[b]:
                b += 1

            while e >= 0 and date_e < self.date[e]:
                e -= 1

            return [d.strftime(self.CLASS_AND_FUNC_FMT) for d in self.date[b:e+1]], self.close[b:e+1]

    def get_high_price(self, date_b=None, date_e=None):
        if date_e is None or date_b is None:
            return [d.strftime(self.CLASS_AND_FUNC_FMT) for d in self.date], self.high
        else:
            date_b = datetime.strptime(date_b, "%Y%m%d")
            date_e = datetime.strptime(date_e, "%Y%m%d")

            b, e = 0, len(self.date) - 1

            while b < len(self.date) and date_b > self.date[b]:
                b += 1

            while e >= 0 and date_e < self.date[e]:
                e -= 1

            return [d.strftime(self.CLASS_AND_FUNC_FMT) for d in self.date[b:e+1]], self.high[b:e+1]

    def get_low_price(self, date_b=None, date_e=None):
        if date_e is None or date_b is None:
            return [d.strftime(self.CLASS_AND_FUNC_FMT) for d in self.date], self.low
        else:
            date_b = datetime.strptime(date_b, "%Y%m%d")
            date_e = datetime.strptime(date_e, "%Y%m%d")

            b, e = 0, len(self.date) - 1

            while b < len(self.date) and date_b > self.date[b]:
                b += 1

            while e >= 0 and date_e < self.date[e]:
                e -= 1

            return [d.strftime(self.CLASS_AND_FUNC_FMT) for d in self.date[b:e+1]], self.low[b:e+1]

    def get_date(self):
        return [d.strftime(self.CLASS_AND_FUNC_FMT) for d in self.date]

    def to_csv(self):
        return ''.join(["{0},{1:.2f},{2:.2f},{3:.2f},{4:.2f},{5}\n".format(self.date[bar].strftime(
            self.CSV_INPUT_AND_OUTPUT_FMT),
            self.open_[bar], self.high[bar],
            self.low[bar], self.close[bar],
            self.volume[bar])
            for bar in range(len(self.close))])

    def write_csv(self, filename=None):
        with open(os.path.join("/Users/apple/Desktop/TCH_api/Technical/CSV_price", self.symbol + ".csv") if filename is None
                  else os.path.join("/CSV_price", filename), 'w') as f:
            f.write(self.to_csv())

    def read_api_csv(self, filename):
        """
        It reads csv of entry format "yyyy-mm-dd, open, high, low, close, volume". 
        This format is exactly the same as the output of write_csv().
        :param filename: filename.
        :return: return a boolean indicating the success of this function.
        """
        self.date, self.open_, self.high, self.low, self.close, self.volume = ([] for _ in range(6))
        for line in open(os.path.join("/CSV_price", filename), 'r'):
            ds, open_, high, low, close, volume = line.rstrip().split(',')
            dt = datetime.strptime(ds, self.CSV_INPUT_AND_OUTPUT_FMT)
            self.append(dt, open_, high, low, close, volume)
        return True

    def read_yahoo_csv(self, filename):
        """
        It reads csv of entry format "yyyy-mm-dd, open, high, low, close, adjclose, volume".
        It also has one extra row at the beginning of the file specify the name of each column.
        This format is the format of data from yahoo finance.
        :param filename: filename.
        :return: return a boolean indicating the success of this function.
        """
        flag = True
        self.date, self.open_, self.high, self.low, self.close, self.volume = ([] for _ in range(6))
        for line in open(os.path.join("/CSV_price", filename), 'r'):
            if flag:
                flag = False
                continue
            ds, open_, high, low, close, adj_close, volume = line.rstrip().split(',')
            dt = datetime.strptime(ds, self.CSV_INPUT_AND_OUTPUT_FMT)
            self.append(dt, open_, high, low, adj_close, volume)
        return True

    def __repr__(self):
        return self.to_csv()


class GoogleQuote(Quote):
    """ 
    Daily quotes from Google. input date format='yyyymmdd' 

    """

    def __init__(self, symbol, start_date, end_date):
        super(GoogleQuote, self).__init__(symbol)
        self.symbol = symbol.upper()
        start = datetime(int(start_date[0:4]), int(start_date[4:6]), int(start_date[6:8]))
        end = datetime(int(end_date[0:4]), int(end_date[4:6]), int(end_date[6:8]))
        url_string = "http://www.google.com/finance/historical?q={0}".format(self.symbol)
        url_string += "&startdate={0}&enddate={1}&output=csv".format(
            start.strftime('%b %d, %Y'), end.strftime('%b %d, %Y'))
        csv = requests.get(url_string, headers=headers).text.split("\n")
        csv.reverse()
        for bar in range(1, len(csv) - 1):
            ds, open_, high, low, close, volume = csv[bar].split(',')
            # The condition is here because a date may only have a closing price.
            # We can simply assign a fake value to the rest of the fileds because closing price is the only one we need.
            open_, high, low, close = [float(x) if x != "-" else 0.0 for x in [open_, high, low, close]]
            dt = datetime.strptime(ds, '%d-%b-%y')
            self.append(dt, open_, high, low, close, volume)


def read_api_csv(filename, symbol):
    q = Quote(symbol)
    q.read_api_csv(filename)
    return q


def read_yahoo_csv(filename, symbol):
    q = Quote(symbol)
    q.read_yahoo_csv(filename)
    return q

def write_csv(q, filename):
    q.write_csv(filename)





