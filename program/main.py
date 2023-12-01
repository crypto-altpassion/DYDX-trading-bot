from constants import ABORT_ALL_POSITIONS, FIND_COINTEGRATED, PLACE_TRADES, MANAGE_EXITS

from fonction_connections import connect_dydx
from fonction_private import abort_all_positions
from fonction_public import construct_market_prices
from fonction_cointegration import store_cointegration_results
from fonction_entry_pairs import open_positions
from fonction_exit_pairs import manage_trade_exits
from fonction_messaging import send_message
from v4_func_connection import get_address_info_v4
from v4_func_public import get_candles_v4

#    from func_connections import connect_dydx
#    from func_private import abort_all_positions
#    from func_public import construct_market_prices
#    from func_cointegration import store_cointegration_results
#    from func_entry_pairs import open_positions
#    from func_exit_pairs import manage_trade_exits
#    from func_messaging import send_message

def main(is_new):

    while is_new:

        # Connect to client
        try:
            print("Connecting to client...")
            client = connect_dydx()
        except Exception as e:
            print("Error connecting to client: ", e)
            # SEND MESSAGE 
            send_message(f"Failed to connect to client {e}")
            main(True)

        # abort all open positions
        if ABORT_ALL_POSITIONS:
            try:
                print("Closing all positions...")
                close_orders = abort_all_positions(client)
            except Exception as e:
                print("Error closing all positions: ", e)
                # SEND MESSAGE 
                send_message(f"Failed to closing all positions {e}")
                exit(1)

        # Find Cointegrated Pairs
        if FIND_COINTEGRATED:

            # Construct Market Prices
            try:
                print("Fetching market prices, please allow 3 minutes...")
                df_market_prices = construct_market_prices(client)
            except Exception as e:
                print("Error constructing market prices: ", e)
                # SEND MESSAGE 
                send_message(f"Failed to construct market prices {e}")
                exit(1)
            
            # Store Cointegrated Pairs 
            try:
                print("Storing cointegrated pairs...")
                stores_result = store_cointegration_results(df_market_prices)
                if stores_result != "saved":
                    print("Error saving cointegrated pairs")
                    # SEND MESSAGE 
                    send_message("Failed to construct market prices")
                    exit(1)
            except Exception as e:
                print("Error saving cointegrated pairs: ", e)
                # SEND MESSAGE 
                send_message(f"Failed to construct market prices {e}")
                exit(1)

        # Run as always on
        while True:

            # Place trades for opening positions
            if MANAGE_EXITS:
                try:
                    print("Managing exits...")
                    manage_trade_exits(client)
                except Exception as e:
                    print("Error managing exiting positions : ", e)
                    # SEND MESSAGE 
                    send_message(f"Failed to manage exiting positions {e}")
                    exit(1)


            # Place trades for opening positions
            if PLACE_TRADES:
                try:
                    print("Findind trading opportunities...")
                    open_positions(client)
                except Exception as e:
                    print("Error trading pairs : ", e)
                    # SEND MESSAGE 
                    send_message(f"Failed to place trades orders {e}")
                    exit(1)

    else:
                # Run as always on
        while True:

            # Place trades for opening positions
            if MANAGE_EXITS:
                try:
                    print("Managing exits...")
                    manage_trade_exits(client)
                except Exception as e:
                    print("Error managing exiting positions : ", e)
                    # SEND MESSAGE 
                    send_message(f"Failed to manage exiting positions {e}")
                    exit(1)

            # Place trades for opening positions
            if PLACE_TRADES:
                try:
                    print("Findind trading opportunities...")
                    open_positions(client)
                except Exception as e:
                    print("Error trading pairs : ", e)
                    # SEND MESSAGE 
                    send_message(f"Failed to place trades orders {e}")
                    exit(1)


# MAIN FUNCTION
if __name__ == "__main__":
    get_address_info_v4("mon_adresse")
    get_candles_v4("BTC-USD","1MIN",limit=100)
    #main(True)