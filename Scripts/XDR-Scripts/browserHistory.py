"""
A script to retrieve a user's browser history and download history

By default this grabs the last 7 days, but this parameter can be adjusted
"""

import os, sqlite3, shutil
from datetime import datetime, timedelta

def date_to_webkit(dt):
    """Convert local datetime to webkit(utc)"""
    epoch_start = datetime(1601, 1, 1)
    delta = dt - epoch_start
    delta_micro_sec = (delta.days * 60 * 60 * 24 + delta.seconds) * 1000 * 1000
    return delta_micro_sec

def time_range_set(dt_from, dt_to):
    time_to = date_to_webkit(dt_to)
    time_from = date_to_webkit(dt_from)
    return time_from, time_to

def get_downloads(fp, user_id, time_from, time_to):

    try:
        conn = sqlite3.connect(fp)
        c = conn.cursor()
        sql_string = f"""
                      SELECT * FROM downloads
                      WHERE {time_from} < start_time
                      AND start_time < {time_to}
                      ORDER BY last_modified DESC;
                      """
        c.execute(sql_string)
        fetch = c.fetchall()
        converted = [convert_json_downloads(x) for x in fetch]
        conn.close()
        return {'user': user_id, 'data': converted}

    except: return None

def get_browser_history(fp, user_id, time_from, time_to):

    try:
        conn = sqlite3.connect(fp)
        c = conn.cursor()
        sql_string = f"""
                      SELECT * FROM urls
                      WHERE {time_from} < last_visit_time
                      AND last_visit_time < {time_to}
                      ORDER BY last_visit_time DESC;
                      """
        c.execute(sql_string)
        fetch = c.fetchall()
        converted = [convert_json(x) for x in fetch]
        conn.close()
        return {'user': user_id, 'data': converted}

    except: return None

def convert_json(data):
    headers = ['id', 'url', 'title', 'visit_count', 'typed_count', 'last_visit_time', 'hidden']
    return dict(zip(headers, list(data)))

def convert_json_downloads(data):
    headers = ['id', 'guid', 'current_path', 'target_path', 'start_time', 'received_bytes', 'total_bytes', 'state', 'danger_type',
               'interrupt_reason', 'hash', 'end_time', 'opened', 'last_access_time', 'transient', 'referrer', 'site_url', 'tab_url', 'tab_referrer_url',
               'http_method', 'by_ext_id', 'by_ext_name', 'etag', 'last_modified', 'mime_type', 'original_mime_type', 'embedder_download_data']

    data = [z.decode() if isinstance(z, (bytes, bytearray)) else z for z in data]
    data = [repr(x) if isinstance(x, str) and '\u0000' in x else x for x in data]


    return dict(zip(headers, data))

def create_tmp_file(fp, tp):
    try:
        shutil.copy2(fp, tp)
    except: pass


def delete_tmp_file(tp):
    try: os.remove(tp)
    except: pass


def main():
    
    # define the date ranges
    dt_to = datetime.now().utcnow()
    dt_from = datetime.now().utcnow() - timedelta(days=7)
    # format timestamps to webkit time
    time_from, time_to = time_range_set(dt_from, dt_to)
    # define values that should be ignored as a user path
    ignored_values = ['All Users', 'Default', 'Default User', 'desktop.ini', 'Public']
    """
    URLs Section
    """
    # define the history paths
    chrome_history_path = r'C:\Users\<username>\AppData\Local\Google\Chrome\User Data\Default\History'
    edge_extensions_path = r'C:\Users\<username>\AppData\Local\Microsoft\Edge\User Data\Default\History'
    # define the tmp file path
    tmp_chrome_path = r'C:\Users\<username>\AppData\Local\Google\Chrome\User Data\Default\tmpHistory'
    tmp_edge_path = r'C:\Users\<username>\AppData\Local\Microsoft\Edge\User Data\Default\tmpHistory'
    # get all items under the C:\Users path
    users = os.listdir(r'C:\Users')
    # filter out known bad values
    users = [x for x in users if x not in ignored_values]
    # create the tmp files
    [create_tmp_file(chrome_history_path.replace('<username>', x), tmp_chrome_path.replace('<username>', x)) for x in users]
    [create_tmp_file(edge_extensions_path.replace('<username>', x), tmp_edge_path.replace('<username>', x)) for x in users]
    # get the url history
    chrome_history = [get_browser_history(tmp_chrome_path.replace('<username>', x), x, time_from=time_from, time_to=time_to) for x in users if x]
    edge_history = [get_browser_history(tmp_edge_path.replace('<username>', x), x, time_from=time_from, time_to=time_to) for x in users if x]

    # remove null values
    chrome_history = [x for x in chrome_history if x]
    edge_history = [x for x in edge_history if x]
    """
    Downloads Section
    """
    # get the url history
    chrome_downloads = [get_downloads(tmp_chrome_path.replace('<username>', x), x, time_from=time_from, time_to=time_to) for x in users if x]
    edge_downloads = [get_downloads(tmp_edge_path.replace('<username>', x), x, time_from=time_from, time_to=time_to) for x in users if x]
    # remove null values
    chrome_downloads = [x for x in chrome_downloads if x]
    edge_downloads = [x for x in edge_downloads if x]

    # delete tmp file
    [delete_tmp_file(tmp_chrome_path.replace('<username>', x)) for x in users]
    [delete_tmp_file(tmp_edge_path.replace('<username>', x)) for x in users]

    return {'chromeHistory': chrome_history, 'edgeHistory': edge_history,
            'chromeDownloads': chrome_downloads, 'edgeDownloads': edge_downloads,
            'information': {'time_from': time_from, 'time_to': time_to}}

main()
