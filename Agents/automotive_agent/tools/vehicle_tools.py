from langchain_core.tools import Tool

# Simple mock data
VEHICLES = {
    ("toyota", "camry", 2024): 28000,
    ("honda", "civic", 2024): 25000,
    ("ford", "f150", 2024): 35000,
}

# Tool functions without Pydantic
def get_vehicle_price(make: str, model: str, year: int) -> str:
    key = (make.lower(), model.lower(), year)
    price = VEHICLES.get(key)
    if price is None:
        return f"Price not found for {year} {make} {model}"
    return f"The {year} {make} {model} costs ${price:,}"

def calculate_payment(price: str, down_payment: int, interest_rate: float) -> str:
    import re
    price_match = re.search(r'\$(\d+(?:,\d+)*)', price)
    if not price_match:
        return "Could not parse price"
    price_value = int(price_match.group(1).replace(',', ''))
    loan_amount = price_value - down_payment
    monthly_rate = interest_rate / 100 / 12
    months = 60
    if monthly_rate == 0:
        payment = loan_amount / months
    else:
        payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
    return f"Monthly payment: ${payment:.2f} for 60 months"

# Wrap functions as LangChain Tools
get_vehicle_price_tool = Tool(
    name="get_vehicle_price",
    func=get_vehicle_price,
    description="Get the price of a vehicle given make, model, and year"
)

calculate_payment_tool = Tool(
    name="calculate_payment",
    func=calculate_payment,
    description="Calculate monthly car payment given price, down payment, and interest rate"
)

# List of tools for the agent
ALL_TOOLS = [get_vehicle_price_tool, calculate_payment_tool]
