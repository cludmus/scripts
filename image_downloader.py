from multiprocessing import Pool
import os
from pathlib import Path
from urllib.request import urlopen
from tqdm import tqdm

def job(iterable_item):
    url = iterable_item["url"]
    filename = iterable_item["filename"]
    response = urlopen(url)
    CHUNK = 16 * 1024
    with open(filename, 'wb') as f:
        while True:
            chunk = response.read(CHUNK)
            if not chunk:
                break
            f.write(chunk)
        f.close()

if __name__ == '__main__':
    search_dir = "Z:/wallpaper-net-data/images/"
    omit = ["nature", "animals"]
    for i in range(0, len(omit)):
        omit[i] = search_dir + omit[i]
        omit[i] = omit[i].replace("/", "\\")

    
    paths = sorted(Path(search_dir).iterdir(), key=os.path.getctime, reverse=False)
    for path in paths:
        #path = "Z:\\wallpaper-net-data\\images\\unusual"
        if(str(path) in omit):
            print("omit " + str(path))
            continue
        txtpath = str(path) + "\\" + str(path).split("\\")[-1] + ".txt"
        Path(str(path) + "\\lowres").mkdir(parents=True, exist_ok=True)
        Path(str(path) + "\\highres").mkdir(parents=True, exist_ok=True)
        Path(str(path) + "\\highrescropped").mkdir(parents=True, exist_ok=True)
        Path(str(path) + "\\using").mkdir(parents=True, exist_ok=True)
        download_path = Path(str(path) + "\\lowres\\")

        txtfile = open(txtpath, "r")
        lines = txtfile.readlines()
        iterable = []
        i = 1
        for line in lines:
            url = ''.join(line.split(" ")[:-1])
            filename = str(path) + "\\lowres\\" + str(i) + ".jpeg"
            iterable.append({"url": url, "filename": filename})
            i+=1
        pool = Pool()
        with tqdm(total=len(lines)) as pbar:
            pbar.set_description(str(path).split("\\")[-1])
            for tmp in pool.imap(func=job, iterable=iterable, chunksize=1):
                pbar.update(1)





        
