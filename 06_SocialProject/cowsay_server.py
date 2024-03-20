#!/usr/bin/env python3
import asyncio
import cowsay

all_cows = set(cowsay.list_cows())
clients = {}

async def chat(reader, writer):
    queue = asyncio.Queue()
    is_registered = False
    me = None
    command_parse = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(queue.get())
    while not reader.at_eof():
        done, pending = await asyncio.wait([command_parse, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is command_parse:
                command_parse = asyncio.create_task(reader.readline())
                command = q.result().decode().strip().split()
                if len(command) > 1:
                    args = command[1:]
                else:
                    args = None
                command = command[0]
                if command == "yield":
                    if not is_registered:
                        writer.write("You need to login.\n".encode())
                        await writer.drain()
                    else:
                        if args and len(args) == 1:
                            for out in clients.values():
                                if out is not clients[me]:
                                    await out.put(f"{cowsay.cowsay(args[0], cow=me)}")
                elif command == "who":
                    registered_cows = clients.keys()
                    if args:
                        cows_str = f"<COMPLETION> {args[0]} {','.join(registered_cows)}\n"
                    else:
                        cows_str = f"Registered cows: {' '.join(registered_cows)}\n"
                    writer.write(cows_str.encode())
                    await writer.drain()
                elif command == "cows":
                    cows = set.difference(all_cows, clients.keys())
                    if args:
                        cows_str = f"<COMPLETION> {args[0]} {','.join(cows)}\n"
                    else:
                        cows_str = f"Free cows: {' '.join(cows)}\n"
                    writer.write(cows_str.encode())
                    await writer.drain()
                elif command == "login":
                    if is_registered:
                        writer.write(f"You are registered.\n".encode())
                        await writer.drain()
                    else:
                        me = args[0]
                        if me not in all_cows:
                            writer.write(f"The cow {me} doesn't exist.\n".encode())
                            await writer.drain()
                        elif me in clients:
                            writer.write(f"The cow {me} is occupied by another user.\n".encode())
                            await writer.drain()
                        else:
                            clients[me] = queue
                            is_registered = True
                elif command == "say":
                    if not is_registered:
                        writer.write("You need to login.\n".encode())
                        await writer.drain()
                    elif len(args) != 2:
                        writer.write("You need to pass message and receiver.\n".encode())
                        await writer.drain()
                    else:
                        reciever, message = args[0], args[1]
                        if reciever in clients:
                            await clients[reciever].put(f"{cowsay.cowsay(message, cow=me)}\n")
                            await writer.drain()
                        else:
                            writer.write(f"{reciever} is not registered.\n".encode())
                            await writer.drain()
                elif command == 'quit':
                    command_parse.cancel()
                    receive.cancel()
                    print(me, "DONE")
                    del clients[me]
                    writer.close()
                    await writer.wait_closed()
                else: 
                    writer.write("Incorrect command.\n".encode())
                    await writer.drain()
                    
                        
                    
            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()


async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())