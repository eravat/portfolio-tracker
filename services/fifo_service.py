from database_models.transactions_model import Transactions
from sqlalchemy.orm import Session


def get_quantity_and_RPL(transaction, temp_list, total_quantity, realised_PL):
    if transaction.type == "buy":
        temp_list.append({"quantity": transaction.quantity, "price": transaction.price})
        total_quantity += transaction.quantity
    elif transaction.type == "sell":
        total_quantity -= transaction.quantity
        quantity = transaction.quantity
        while quantity > 0:
            firstElement = temp_list[0]
            firstElement["quantity"] -= quantity
            if firstElement["quantity"] <= 0:                               #thanks to pytest realised that before this was only < so if the total quantity of shares in temp list exactly matched the sell value the list wouldn't be returned as empty
                original_quantity = firstElement["quantity"] + quantity
                realised_PL += (transaction.price - firstElement["price"])*original_quantity
                quantity = abs(firstElement["quantity"])
                temp_list.pop(0)
            else:
                realised_PL += (transaction.price-firstElement["price"])*quantity
                quantity = 0
    return temp_list, total_quantity, realised_PL

def calculate_ticker_res(db: Session, portfolio_id: int):
    ticker_dict = {}
    transactions = db.query(Transactions).filter(portfolio_id==Transactions.portfolio_id).order_by(Transactions.transaction_date).all()

    for transaction in transactions:
        if transaction.ticker not in ticker_dict:
            ticker_dict[transaction.ticker] = [transaction]
        else:
            ticker_dict[transaction.ticker].append(transaction)

    ticker_res = {}
    for ticker in ticker_dict:
        total_quantity = 0
        avg_price = 0
        realised_PL = 0
        temp_list = []
        for transaction in ticker_dict[ticker]:
            temp_list, total_quantity, realised_PL = get_quantity_and_RPL(transaction, temp_list, total_quantity, realised_PL)
        
        if total_quantity > 0:
            net_value=0
            for tempDict in temp_list:
                net_value += (tempDict["quantity"]*tempDict["price"])

            avg_price = net_value/total_quantity

        else:
            avg_price = 0

        ticker_res[ticker] = {"total quantity":total_quantity, "average price":avg_price, "realised pnl":realised_PL}
    return ticker_res