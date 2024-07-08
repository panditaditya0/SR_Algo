import asyncio
import websockets
import random
import threading
import time
import json

# Define your global variables
message = 0
log = "Sample Log"
previous_day_low = 30000
previous_day_high = 36000
index_ltp = 35000
call_ltp = 200
put_ltp = 150
index_symbol = "NIFTY50"
call_symbol = "NIFTY50_CE"
put_symbol = "NIFTY50_PE"
pnl = 1000
symbol_bought = "NIFTY50"
bought_at = 34900

async def produce_data(websocket, path):
    global message, log, previous_day_low, previous_day_high, index_ltp, call_ltp, put_ltp, index_symbol, call_symbol, put_symbol, pnl, symbol_bought, bought_at
    while True:
        # Prepare the JSON structure
        data = {
            "log": log,
            "support": previous_day_low,
            "resistance": previous_day_high,
            "ltp1": index_ltp,
            "ltp2": call_ltp,
            "ltp3": put_ltp,
            "symbol1": index_symbol,
            "symbol2": call_symbol,
            "symbol3": put_symbol,
            "pnl": pnl,
            "bought_symbol": symbol_bought,
            "bought_at": bought_at
        }

        # Send the JSON structure to the client
        await websocket.send(json.dumps(data))

        # Wait for 1 second before sending the next value
        await asyncio.sleep(1)

async def start_server():
    server = await websockets.serve(produce_data, "localhost", 8765)
    await server.wait_closed()

def produce_data_thread():
    global message, log, previous_day_low, previous_day_high, index_ltp, call_ltp, put_ltp, index_symbol, call_symbol, put_symbol, pnl, symbol_bought, bought_at
    while True:
        # Update the global variables with new random values for testing
        message = random.randint(1, 100)
        index_ltp = random.randint(34000, 36000)
        call_ltp = random.randint(100, 300)
        put_ltp = random.randint(100, 200)
        pnl = random.randint(-500, 1500)
        bought_at = random.randint(34000, 36000)
        time.sleep(1)

if __name__ == "__main__":
    # Start the asyncio event loop in a separate thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Start the WebSocket server in a separate thread
    server_thread = threading.Thread(target=lambda: asyncio.run(start_server()))
    server_thread.start()

    # Start producing random data in the main thread
    produce_data_thread()

    # Join the server thread to the main thread
    server_thread.join()
