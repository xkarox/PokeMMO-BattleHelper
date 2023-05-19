import asyncio
import logging
import websockets
from websockets import WebSocketServerProtocol
import time
import threading
import json
from datetime import datetime
from src.Database_service import Database_service
from src.game_data_service import game_data_service
import threading


logging.basicConfig(level=logging.INFO)


class Server:

    clients = set()
    logging.info(f'Starting Server')

    def __init__(self):
        logging.info(f' init happened ...')
        
    async def register(self, ws: WebSocketServerProtocol) -> None:
        self.clients.add(ws)
        logging.info(f' {ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol) -> None:
        self.clients.remove(ws)
        logging.info(f' {ws.remote_address} disconnects')

    async def send_to_clients(self, message: str) -> None:
        if self.clients:
            logging.info("trying to send")
            await asyncio.wait([client.send(message) for client in self.clients])

    async def ws_handler(self, ws: WebSocketServerProtocol, url: str) -> None:
        await self.register(ws)
        try:
            await self.distribute(ws)
        finally:
            await self.unregister(ws)

    async def distribute(self, ws: WebSocketServerProtocol) -> None:
        async for message in ws:
            await self.send_to_clients(message)


async def checkAndSend(server, data):
    await server.send_to_clients(data)

# helper routine to allow thread to call async function
def between_callback(server):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(gameDataThread(server))
    loop.close()

async def gameDataThread(server):
    
    pokemon_temp = []
        
    gds = game_data_service()
    db = Database_service()

    window_handle = gds.find_window()
    
    while True:
        
        img = gds.capture_screen( window_handle, showWindow=False)
        data = gds.process_image(img)
        found_pokemon = gds.find_pokemon_names(data)
        
        print(f'Found pokemon: {len(found_pokemon)}, {found_pokemon}')
        
        if len(found_pokemon) != 0:
            
            if (pokemon_temp != found_pokemon):
                #iterate through all pokemon found on screen
                for pokemon in found_pokemon:
                
                    db_pokemon = db.get_pokemon(pokemon)
                    
                    types = db.get_pokemon_types(db_pokemon)
                    
                    stats = db.get_pokemon_stats(db_pokemon)
                    # damage_relations = db.get_damage_relations(type)
                    damage_relations = {}
                    for type in types:
                        damage_relations[type] = db.get_damage_relations(type)
                    
                    sprite = db_pokemon.sprites.front_default
                    
                    data =  {}
                    data['name'] = pokemon
                    data['type'] = types
                    data['stats'] = stats
                    data['damage-relations'] = damage_relations
                    data['sprite'] = sprite
                    data['timestamp'] = datetime.now().strftime("%H:%M:%S")
                    data_string = json.dumps(data)
                    
                    await checkAndSend(server, data_string)
                    
                    pokemon_temp = found_pokemon
                time.sleep(2)
