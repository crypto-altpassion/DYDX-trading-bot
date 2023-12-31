from datetime import datetime, timedelta
from func_utils import format_number
import time

from pprint import pprint

# Get existing open positions
def is_open_positions(client, market):

    # Protect API 
    time.sleep(1)

    # Get positions
    all_positions = client.private.get_positions(
        market= market,
        status= "OPEN"
    )

    # Determine if open
    if len(all_positions.data["positions"]) > 0:
        return True
    else:
        return False
    
def check_order_status_n_price(client, order_id):
    order = client.private.get_order_by_id(order_id)
    if order.data:
        if "order" in order.data.keys():
            status = order.data["order"]["status"]
            price = order.data["order"]["price"]  # Get the price of the order
            return price
    return None

# Check order status
def check_order_status(client, order_id):
    order = client.private.get_order_by_id(order_id)
    if order.data:
        if "order" in order.data.keys():
            return order.data["order"]["status"]
    return "FAILED"

# Place market order
def place_market_order(client, market, side, size, price, reduce_only):
    # Get position Id
    account_response = client.private.get_account()
    position_id = account_response.data["account"]["positionId"]
    
    # Get expiration time
    server_time = client.public.get_time()
    expiration = datetime.fromisoformat(server_time.data["iso"].replace("Z", "")) + timedelta(seconds=70)

    # Place an order
    placed_order = client.private.create_order(
        position_id=position_id,
        market=market,
        side=side, 
        order_type="MARKET",
        post_only=False,
        size=size,
        price=price,
        limit_fee="0.015",
        expiration_epoch_seconds=expiration.timestamp(),
        time_in_force="FOK",
        reduce_only=reduce_only 
    )
    # Return result
    return placed_order.data

# Abort all open positions
def abort_all_positions(client):
    
    # Cancel all orders
    client.private.cancel_all_orders()

    # Protect API
    time.sleep(1)

    # Get markets for reference of thick size
    markets = client.public.get_markets().data
    #pprint(markets)

    # Protect API
    time.sleep(1)

    # Get all open positions
    positions = client.private.get_positions(status="OPEN")
    all_positions = positions.data["positions"]

    #pprint(all_positions)

    # Handle open positions
    close_orders = []
    if len(all_positions) > 0:

        # Loopthrough each position
        for position in all_positions:

            # Determine Market
            market = position["market"]

            # Determine Side
            side = "BUY"
            if position["side"] == "LONG":
                side = "SELL"
            #print(market, side)

            # Get Price
            price = float(position["entryPrice"])
            accept_price = price * 1.7 if side == "BUY" else price * 0.3 # à modifier? (sert à déterminer quel est le montant maximum qu'on est pret a prendre pour un market trade)
            tick_size = markets["markets"][market]["tickSize"]
            accept_price = format_number(accept_price, tick_size)

            # Place order to close 
            order = place_market_order(
                client,
                market,
                side,
                position["sumOpen"],
                accept_price,
                True
            )
            
            # Append the result
            close_orders.append(order)

            # Pretect API
            time.sleep(1)

        # Return closed orders
        return close_orders
