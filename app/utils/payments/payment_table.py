def get_payment_table(db, payments):
    payment_table = []    
    balance = 0
    for payment in payments:
        balance = balance + payment.payment_amount
        if payment.payment_method == None:
            txn_number = payment.txn_name + " *" + payment.txn_number+"* " + "Método de pago: " + "N/A" 
        else:
            txn_number = payment.txn_name + " *" + payment.txn_number+"* " + "Método de pago: " +payment.payment_method  
        payment_table.append(
            {
                "id": payment.id,
                "payment_date": payment.payment_date,
                "txn_number": txn_number, 
                "payment_amount": payment.payment_amount,
                "balance": balance                  
            }
        )
    return payment_table
        
    