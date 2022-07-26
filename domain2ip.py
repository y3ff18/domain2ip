import socket
from threading import Thread
import queue
import argparse
from concurrent.futures import ThreadPoolExecutor,as_completed,wait

from sqlalchemy import null

parse = argparse.ArgumentParser()
parse.add_argument("-f",'--file',help="InPut Domain File",default=null)
parse.add_argument("-o",'--output',help="Set Save File",default=null)
parse.add_argument("-t","--thread",help='Set Thread,default 100',default=100,type=int)
args = parse.parse_args()
save_file = args.output
task_file = args.file
thread = args.thread


save_file = open(save_file,'a',encoding='utf-8')
    
def run(domain):
        try:
            ip = socket.gethostbyname(domain)
            save(domain=domain,ip=ip)
        except:
            print("Warring")

def save(domain,ip):
    save_file.write(domain+" || "+ip+'\n')
    print(f"[+] {domain} >> {ip}")

        
domains_queue = queue.Queue()
def get_file():
    with open(task_file,'r',encoding='utf-8') as fi:
        for i in fi:
            domains_queue.put(str(i).strip())
    print(f"[+] file size {domains_queue.qsize()}")


if __name__ == "__main__":
    get_file()
    obj_list = []
    with ThreadPoolExecutor(max_workers=thread) as t:
        while domains_queue.qsize() > 0:
            domain = domains_queue.get()
            obj = t.submit(run,domain)
            obj_list.append(obj)
        wait(obj_list)
    save_file.close()



            

