__author__ = 'adam1'
#!C:\Python26\python.exe

'''
Programmer: Adam Bouzourene

filename: multiDownload.py

This is a python script that reads a text file and downloads all the files inside

text file format should be title then url and alternating for each file

'''

import ssl
import threading
from Queue import Queue
import os
import requests


class DownloadThread(threading.Thread):
    def __init__(self, queue, destfolder):
        super(DownloadThread, self).__init__()
        self.queue = queue
        self.destfolder = destfolder
        self.daemon = True

    def run(self):
        while True:
            request = self.queue.get()
            try:
                self.downloadFile(request[0], request[1])
            except Exception, e:
                print "   Error: %s" % e
            self.queue.task_done()

    def downloadFile(self, url, fname):
        #here's where file extension is resolved
        dest = os.path.join(self.destfolder, (fname + ".mp4"))
        print "[thread: {}] Downloading {} from ({})".format(self.ident, fname, url)
        downloadBar(url, dest, fname)
        print


def downloadBar(url, path, fname):
    r = requests.get(url, stream=True)
    with open(path, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        downloaded = 0
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                downloaded += len(chunk)
                done = int(float(downloaded) / float(total_length) * 100.0)
                f.write(chunk)
                f.flush()
                print "{}: {}%\n".format(fname, done)


def download(urls, destfolder, names, numthreads):
    """
    creates download threads and queue of downloads
    :param urls: all links parsed from links file
    :param d: second object amount

    """
    queue = Queue()
    namQ = 0
    assert (len(urls) == len(names))
    for url in urls:
        obj = [url, names[namQ]]
        queue.put(obj)
        namQ += 1
    for i in range(numthreads):
        t = DownloadThread(queue, destfolder)
        t.start()
    queue.join()


def main():
    lNames = []
    urls = []
    title = True
    fn = raw_input("enter your links filename: ")
    dir = raw_input("which directory do you wish to use: ")
    thrdCount = int(raw_input("how many threads do you wish to use: "))

    ifile = open(fn, 'r')

    for line in ifile:
        if title:
            lNames.append(line.rstrip(" \n"))
            title = False
        else:
            urls.append(line.rstrip(" \n"))
            title = True

    download(urls, dir, lNames, thrdCount)

    print("all downloads done")

main()

