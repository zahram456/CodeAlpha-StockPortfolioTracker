# Hardcoded stock prices
stock_prices = {
    "AAPL": 180,
    "TSLA": 250,
    "GOOGL": 2800,
    "MSFT": 320,
    "AMZN": 3500
}

total_investment = 0
portfolio = []

print("Welcome to Stock Portfolio Tracker\n")

num_stocks = int(input("How many different stocks do you want to add? "))

for _ in range(num_stocks):
    stock_name = input("Enter stock symbol (e.g., AAPL): ").upper()
    
    if stock_name in stock_prices:
        quantity = int(input("Enter quantity: "))
        price = stock_prices[stock_name]
        investment = quantity * price
        
        total_investment += investment
        
        portfolio.append((stock_name, quantity, investment))
        
        print(f"Added {quantity} shares of {stock_name}")
        print(f"Investment value: ${investment}\n")
    else:
        print("Stock not found in price list.\n")

print("----- Portfolio Summary -----")
for stock in portfolio:
    print(f"{stock[0]} - {stock[1]} shares - ${stock[2]}")

print(f"\nTotal Investment Value: ${total_investment}")

# Optional: Save to file
with open("portfolio_summary.txt", "w") as file:
    file.write("Stock Portfolio Summary\n")
    file.write("------------------------\n")
    for stock in portfolio:
        file.write(f"{stock[0]} - {stock[1]} shares - ${stock[2]}\n")
    file.write(f"\nTotal Investment Value: ${total_investment}")

print("\nPortfolio saved to 'portfolio_summary.txt'")
