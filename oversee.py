import time
import json
import flask
import pynvml
import threading
from flask_cors import CORS
from watchdog.events import *
from watchdog.observers import Observer


class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_created(self, event):
        searcher = ""
        try:
            searcher = re.findall(r"\d+", event.src_path.split("\\")[-1])[0].lstrip("0")
        except IndexError:
            searcher = "0"
            print("Search Error - <文件没有数字>")
        finally:
            counter['count'] = eval(searcher) or 0
        computeTimer()


def returnObj(methods: str = "") -> dict:
    if methods == "post":
        return {
            "total": counter['total'],
            "count": counter['count'] if counter['count'] != 0 else '未开始',
            "timer": "{}".format(counter['allTime']),
            "gpu": "{}%".format(pynvml.nvmlDeviceGetUtilizationRates(GPU).gpu),
            "complete": "{}%".format(counter['complete']),
            "expected": "{}".format(counter['expected'])
        }
    else:
        return {
            "总帧数": counter['total'],
            "目前渲染帧数": counter['count'] if counter['count'] != 0 else '未开始',
            "此帧渲染时间": "{}".format(counter['allTime']),
            "GPU使用率": "{}%".format(pynvml.nvmlDeviceGetUtilizationRates(GPU).gpu),
            "已渲染": "{}%".format(counter['complete']),
            "预计完成时间": "{}".format(counter['expected'])
        }


def computeTimer() -> object:
    counter['endTime'] = time.time()
    counter['allTime'] = round(counter['endTime'] - counter['startTime'], 2)
    counter['expected'] = (counter['total'] - counter['count']) * counter['allTime']
    # 预计渲染时间
    if counter['expected'] >= 86400:
        d = counter['expected'] / 86400
        h = counter['expected'] % 86400 / 3600
        m = counter['expected'] % 3600 / 60
        counter['expected'] = "{}天{}小时{}分钟".format(int(d), int(h), int(m))
    elif counter['expected'] >= 3600:
        h = counter['expected'] / 3600
        m = counter['expected'] % 3600 / 60
        counter['expected'] = "{}小时{}分钟".format(int(h), int(m))
    elif counter['expected'] >= 60:
        m = counter['expected'] / 60
        s = counter['expected'] % 60
        counter['expected'] = "{}分钟{}秒".format(int(m), int(s))
    elif counter['expected'] > 0:
        counter['expected'] = "{}秒".format(int(counter['expected']))
    else:
        counter['expected'] = "渲染完毕"
    # 此帧渲染时间
    if counter['allTime'] >= 3600:
        h = counter['allTime'] / 3600
        m = counter['allTime'] % 3600 / 60
        s = counter['allTime'] % 60
        counter['allTime'] = "{}小时{}分钟{}秒".format(int(h), int(m), int(s))
    elif counter['allTime'] >= 60:
        m = counter['allTime'] / 60
        s = counter['allTime'] % 60
        counter['allTime'] = "{}分钟{}秒".format(int(m), int(s))
    else:
        counter['allTime'] = str(counter['allTime']) + "秒"
    counter['startTime'] = counter['endTime']
    counter['complete'] = round(counter['count'] / counter['total'] * 100, 2)
    print(returnObj())
    return counter


def run_server(port: int = 3000):
    server = flask.Flask(__name__)
    CORS(server, resources={r'/*': {"origins": "*"}}, supports_credentials=True)

    @server.route('/', methods=['get'])
    def getter():
        datas = returnObj()
        text = ""
        for line in datas:
            text += "<h1>{}:{}</h1>".format(line, datas[line])
        return text

    @server.route('/', methods=['post'])
    def poster():
        return json.dumps({'data': returnObj("post")}, ensure_ascii=False)

    print("端口:{}\n".format(port))
    server.run(debug=False, port=port, threaded=True, host='0.0.0.0')


def run_oversee():
    observer = Observer()
    event_handler = FileEventHandler()
    observer.schedule(event_handler, dirName, True)
    observer.start()
    print("开始监测")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    dirName = input("输入文件夹名称,默认<render> : ").strip('"') or "render"
    if not os.path.exists(dirName):
        os.makedirs(dirName)
    counter = {'total': 0, 'count': 0, 'allTime': 0.0 or "", 'startTime': time.time(), 'endTime': 0.0, 'complete': 0.0}
    try:
        counter['total'] = eval(input("总帧数 : ")) or 0
    except NameError or SyntaxError:
        counter['total'] = 0
    pynvml.nvmlInit()
    GPU = pynvml.nvmlDeviceGetHandleByIndex(0)
    threading.Thread(target=run_oversee).start()
    threading.Thread(target=run_server,).start()
