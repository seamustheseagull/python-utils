import requests
import os
import time

def run_download(url):

    data = {"download_time" : -1, "filesize" : -1}

    detail = requests.get(url, stream=True)

    if(detail.status_code and int(detail.status_code) < 400):
        start_dl = time.time()
        
        data['filesize'] = int(detail.headers['Content-Length'])
        
        with open(os.devnull,"w") as fd:
            for chunk in detail.iter_content(chunk_size=128):
                fd.write(chunk)
        
        end_dl = time.time()

        data['download_time'] = (end_dl - start_dl)
           
    return data

def main(): 
    test_url = "http://ftp.heanet.ie/mirrors/videolan/vlc/3.0.0/vlc-3.0.0.tar.xz"

    backup_url = "http://ftp.halifax.rwth-aachen.de/videolan/vlc/3.0.0/vlc-3.0.0.tar.xz"

    download_detail = run_download(test_url)

    if(download_detail['download_time'] > 0):        
        print("Download took %.3f seconds (%.3fMB/s)" % (download_detail['download_time'], (download_detail['filesize']/download_detail['download_time'])/1024/1024) )
    else:
        print("Trying backup URL")
        download_detail = run_download(backup_url)

        if(download_detail['download_time'] > 0):        
            print("Download took %.3f seconds (%.3fMB/s)" % (download_detail['download_time'], (download_detail['filesize']/download_detail['download_time'])/1024/1024) )
        else:
            print("Downloads failed. Network connection may be down")


if __name__ == "__main__":
    main()