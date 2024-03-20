import cmd
import threading
import time
import readline
import shlex
import socket

response = {}

class CowClient(cmd.Cmd):
    
    def initialize_connection(self):
        HOST = "127.0.0.1" 
        PORT = 1337
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT)) 
        self.msg_num = 0 
        

    def do_login(self, arg):
        self.s.send(f"login {arg}\n".encode())
        
    def complete_login(self, text, line, begidx, endidx):
        args = shlex.split(text)
        if line[-1] == " ":
            start = None
        elif len(args) == 1:
            start = args[-1]
        else: 
            return []
        
        self.s.sendmsg([f"cows {self.msg_num}\n".encode()])
        response[self.msg_num] = None
        
        while not response[self.msg_num]:
            pass
        
        cows = response[self.msg_num]
        self.msg_num += 1
        if start:
            return [i for i in cows if i.startswith(start)]
        else:
            return cows
        
    def do_cows(self, arg):
        self.s.send("cows\n".encode())
        
    def do_who(self, arg):
        self.s.send("who\n".encode())
        
    def do_yield(self, arg):
        self.s.send(f"yield {arg}\n".encode())
        
    def do_quit(self, arg):
        self.s.send("quit\n".encode())
        exit(0)
        
    def do_say(self, arg):
        self.s.send(f"say {arg}\n".encode())
        
    def complete_say(self, text, line, begidx, endidx):
        args = shlex.split(text)
        if line[-1] == " ":
            start = None
        elif len(args) == 1:
            start = args[-1]
        else: 
            return []
        
        
        self.s.send(f"who {self.msg_num}\n".encode())
        response[self.msg_num] = None
        while not response[self.msg_num]:
            pass
        cows = response[self.msg_num]
        self.msg_num += 1
        if start:
            return [i for i in cows if i.startswith(start)]
        else:
            return cows
        
        


def read_response(socket):
    
    while True:
        try:
            buf = socket.recv(1024).decode()
            if not buf:
                break
            if buf.startswith("<COMPLETION>"):
                _, msg_num_response, result = buf.split(maxsplit=2)
                response[int(msg_num_response)] = result.split(",")
            else:
                print(f"{buf}\n{client.prompt} {readline.get_line_buffer()}", end="", flush=True)
        except:
            exit(0)
            
        
        

            
client = CowClient()
client.initialize_connection()
s = client.s

response_reader = threading.Thread(target=read_response, args=(s,))
response_reader.start()
client.cmdloop()

