from data_collection import *
DATE_B = "20000101"
DATE_E = datetime.today().strftime("%Y%m%d")


def get_price(sec, date_b, date_e, filename=None):
    if filename is None:
        possible_filename = "/CSV_price_google/" + sec + ".csv"
        if os.path.isfile(possible_filename):
            return read_api_csv(possible_filename, sec).get_price(date_b, date_e)
        else:
            qt = GoogleQuote(sec, DATE_B, DATE_E)
            qt.write_csv(possible_filename)
            return read_api_csv(possible_filename, sec).get_price(date_b, date_e)
    else:
        try:
            return read_yahoo_csv(filename, sec).get_price(date_b, date_e)
        except:
            return read_sse_csv(filename, sec).get_price(date_b, date_e)


def get_low_price(sec, date_b, date_e, filename=None):
    if filename is None:
        possible_filename = "/CSV_price_google/" + sec + ".csv"
        if os.path.isfile(possible_filename):
            return read_api_csv(possible_filename, sec).get_low_price(date_b, date_e)
        else:
            qt = GoogleQuote(sec, DATE_B, DATE_E)
            qt.write_csv(possible_filename)
            return read_api_csv(possible_filename, sec).get_low_price(date_b, date_e)
    else:
        try:
            return read_yahoo_csv(filename, sec).get_low_price(date_b, date_e)
        except:
            return read_sse_csv(filename, sec).get_low_price(date_b, date_e)


def get_high_price(sec, date_b, date_e, filename=None):
    if filename is None:
        possible_filename = "/Users/apple/Desktop/TCH_api/Technical/CSV_price_google/" + sec + ".csv"
        if os.path.isfile(possible_filename):
            return read_api_csv(possible_filename, sec).get_high_price(date_b, date_e)
        else:
            qt = GoogleQuote(sec, DATE_B, DATE_E)
            qt.write_csv(possible_filename)
            return read_api_csv(possible_filename, sec).get_high_price(date_b, date_e)
    else:
        try:
            return read_yahoo_csv(filename, sec).get_high_price(date_b, date_e)
        except Exception:
            return read_sse_csv(filename, sec).get_high_price(date_b, date_e)


def get_price_sma(sec, date_b, date_e, day_num, filename=None):
    trading_day_num = len(get_price(sec, date_b, date_e, filename)[1])
    trading_days_needed = trading_day_num + day_num - 1

    date_b = (datetime.strptime(date_b, "%Y%m%d") - timedelta(days=2*day_num)).strftime("%Y%m%d")
    raw_prices = get_price(sec, date_b, date_e, filename)[1][-trading_days_needed:]

    prev = np.array(raw_prices[:day_num]).sum() / day_num
    result = [prev]

    for i in range(day_num, trading_days_needed):
        prev = (prev * day_num + raw_prices[i] - raw_prices[i-day_num]) / day_num
        result.append(prev)

    return result


def get_price_sma_crossover(sec, date_b, date_e, fast, slow, filename=None):
    sma_fast = get_price_sma(sec, date_b, date_e, fast, filename=filename)
    sma_slow = get_price_sma(sec, date_b, date_e, slow, filename=filename)
    fast_slow = np.array(sma_fast) - np.array(sma_slow)
    dates, prices = get_price(sec, date_b, date_e, filename)

    cross_overs_up = []
    cross_overs_down = []

    for i in range(1, len(dates)):
        if fast_slow[i] > 0 and fast_slow[i-1] <= 0:
            cross_overs_up.append([i, prices[i]])
        elif fast_slow[i] < 0 and fast_slow[i-1] >= 0:
            cross_overs_down.append([i, prices[i]])

    return cross_overs_up, cross_overs_down


def get_price_return(sec, date_b, date_e, filename=None):
    day_to_day_return = []

    num_returned = len(get_price(sec, date_b, date_e, filename)[1])
    num_needed = num_returned + 1

    temps = get_price(sec, (datetime.strptime(date_b, "%Y%m%d") - timedelta(days=10)).strftime("%Y%m%d"), date_e, filename)
    datas = temps[1][-num_needed:]
    dates = temps[0][-num_returned:]
    for i in range(1, len(datas)):
        day_to_day_return.append((datas[i] - datas[i - 1]) / datas[i - 1] if datas[i - 1] != 0 else 0)

    return dates, day_to_day_return


def get_vol(sec, date_b, date_e, filename=None):
    if filename is None:
        possible_filename = "/Users/apple/Desktop/TCH_api/Technical/CSV_price_google/" + sec + ".csv"
        if os.path.isfile(possible_filename):
            return read_api_csv(possible_filename, sec).get_vol(date_b, date_e)
        else:
            qt = GoogleQuote(sec, DATE_B, DATE_E)
            qt.write_csv(possible_filename)
            return read_api_csv(possible_filename, sec).get_vol(date_b, date_e)
    else:
        try:
            return read_yahoo_csv(filename, sec).get_vol(date_b, date_e)
        except Exception:
            return read_sse_csv(filename, sec).get_vol(date_b, date_e)


def get_vol_change(sec, date_b, date_e, filename=None):
    day_to_day_change = []

    num_returned = len(get_vol(sec, date_b, date_e, filename)[1])
    num_needed = num_returned + 1

    temps = get_vol(sec, (datetime.strptime(date_b, "%Y%m%d") - timedelta(days=10)).strftime("%Y%m%d"), date_e, filename)
    datas = temps[1][-num_needed:]
    dates = temps[0][-num_returned:]
    for i in range(1, len(datas)):
        day_to_day_change.append((datas[i] - datas[i - 1]) / datas[i - 1] if datas[i - 1] != 0 else 0)

    return dates, day_to_day_change


def get_vol_sma(sec, date_b, date_e, day_num, filename=None):
    trading_day_num = len(get_vol(sec, date_b, date_e, filename)[1])
    trading_days_needed = trading_day_num + day_num - 1

    date_b = (datetime.strptime(date_b, "%Y%m%d") - timedelta(days=2*day_num)).strftime("%Y%m%d")
    raw_vols = get_vol(sec, date_b, date_e, filename)[1][-trading_days_needed:]

    prev = np.array(raw_vols[:day_num]).sum() / day_num
    result = [prev]

    for i in range(day_num, trading_days_needed):
        prev = (prev * day_num + raw_vols[i] - raw_vols[i-day_num]) / day_num
        result.append(prev)

    return result


def date_subtract_days(date_e, num_days):
    return (datetime.strptime(date_e, "%Y%m%d") - timedelta(days=num_days)).strftime("%Y%m%d")


def date_add_days(date_e, num_days):
    return (datetime.strptime(date_e, "%Y%m%d") + timedelta(days=num_days)).strftime("%Y%m%d")


def get_date_b(sec, date_e, num_periods, filename=None):
    dates = []
    datee = date_subtract_days(date_e, 2 * num_periods)
    while len(dates) < num_periods + 1:
        print(datee)
        dates = get_price(sec, datee, date_e, filename)[0]
        datee = date_subtract_days(datee, 2 * num_periods)

    return dates[-num_periods-1 if date_e in dates else -num_periods]


def get_date_e(sec, date_e, num_periods, filename=None):
    dates = []
    datee = date_add_days(date_e, 2 * num_periods)
    while len(dates) < num_periods + 1:
        print(datee)
        dates = get_price(sec, datee, date_e, filename)[0]
        datee = date_add_days(datee, 2 * num_periods)

    return dates[num_periods if date_e in dates else num_periods-1]


