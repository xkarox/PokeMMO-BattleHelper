
import threading
from src.server import Server, between_callback
import websockets 
import asyncio 


def main():
    # start server
    server = Server()
    start_server = websockets.serve(server.ws_handler,'localhost',4000)
    counter = 0 

    # start timer thread
    threading.Thread(target=between_callback,args=(server,)).start()

    # start main event loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    loop.run_forever()


if __name__ in {"__main__", "__mp_main__"}:
    main()