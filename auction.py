import time
import threading
import random

class AuctionItem:
    def __init__(self, name, starting_bid):
        self.name = name
        self.starting_bid = starting_bid
        self.current_bid = starting_bid
        self.highest_bidder = None
        self.active = True
        self.countdown = 10  # Total countdown in seconds
        self.lock = threading.Lock()

    def place_bid(self, bidder_name, bid_amount):
        with self.lock:
            if not self.active:
                print("The auction for this item has ended.")
                return False
            if bid_amount > self.current_bid:
                self.current_bid = bid_amount
                self.highest_bidder = bidder_name
                print(f"New highest bid of {bid_amount} by {bidder_name}")
                self.countdown = 10  # Reset countdown
                return True
            else:
                print("Bid amount must be higher than the current bid.")
                return False

    def start_countdown(self):
        while self.countdown > 0:
            time.sleep(1)
            with self.lock:
                self.countdown -= 1
                if self.countdown <= 3:
                    print(f"Countdown: {self.countdown} seconds remaining...")
        self.finalize_auction()

    def finalize_auction(self):
        with self.lock:
            self.active = False
            if self.highest_bidder:
                print(f"Auction closed! {self.name} sold to {self.highest_bidder} for {self.current_bid}.")
            else:
                print(f"Auction closed! No bids were placed on {self.name}.")

class Auction:
    def __init__(self):
        self.items = []

    def add_item(self, name, starting_bid):
        item = AuctionItem(name, starting_bid)
        self.items.append(item)
        print(f"Item {name} added with a starting bid of {starting_bid}.")

    def start_auction(self, item_name):
        for item in self.items:
            if item.name == item_name:
                print(f"Starting auction for {item_name}.")
                countdown_thread = threading.Thread(target=item.start_countdown)
                countdown_thread.start()
                return item
        print(f"Item {item_name} not found in auction list.")
        return None

    def place_bid(self, item_name, bidder_name, bid_amount):
        for item in self.items:
            if item.name == item_name:
                return item.place_bid(bidder_name, bid_amount)
        print(f"Item {item_name} not found in auction list.")
        return False

    def computer_bid(self, item_name):
        for item in self.items:
            if item.name == item_name and item.active:
                time.sleep(1)  # Simulate a slight delay for computer response
                bid_amount = random.randint(item.current_bid + 10, item.current_bid + 100)
                self.place_bid(item_name, "Computer", bid_amount)

# Example usage
if __name__ == "__main__":
    auction_system = Auction()
    
    # Auctioneer adds items to the auction
    auction_system.add_item("Vintage Vase", 100)
    
    # Start auction
    item = auction_system.start_auction("Vintage Vase")
    
    # Simulating user and computer interaction
    bid_count = 0
    max_bids = 2  # Computer will bid twice

    while item and item.active and bid_count < max_bids:
        user_bid = input("Enter your bid amount (or 'exit' to stop bidding): ")
        if user_bid.lower() == 'exit':
            break
        if user_bid.isdigit():
            if auction_system.place_bid("Vintage Vase", "User", int(user_bid)):
                bid_count += 1
                auction_system.computer_bid("Vintage Vase")
                bid_count += 1
        else:
            print("Please enter a valid number.")
    
    # Allow user to place the final bid after the computer's third bid
    if item and item.active and bid_count == max_bids:
        user_bid = input("Enter your final bid amount (or 'exit' to stop bidding): ")
        if user_bid.isdigit():
            auction_system.place_bid("Vintage Vase", "User", int(user_bid))

    # Wait for auction to close before ending the program
    if item:
        while item.active:
            time.sleep(1)
