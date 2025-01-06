from flask_restx import Resource
import starkbank
import random
from faker import Faker
from brutils import generate_cpf
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import time
from datetime import datetime, timedelta
from models.invoice import invoice
from models.transfer import transfer
from server import api, app
import threading



fake = Faker()

def getPrivateKey():
    return """
    -----BEGIN EC PRIVATE KEY-----
    MHQCAQEEIK0UNdMVIBr580wKY0UgFhWa3CxEEcaeDaUQk8PuElHyoAcGBSuBBAAK
    oUQDQgAE4B79u5bVd2kmbmMRuGKCv0EvnJJp+J5AuN7mzzBRUUNmDE+0c62l7cAY
    6AmACizFXXyPBaIKJQSUYfWtjruucg==
    -----END EC PRIVATE KEY-----
    """

def authentication():
    user = starkbank.Project(
        environment="sandbox",
        id="6241750020521984",
        private_key=getPrivateKey()
    )
    starkbank.user = user
    print("Authentication successful")

authentication()      

def schedule_for_three_hours(invoiceGenerator, invoice_list):
    runs = random.randint(8, 12)  
    interval = (3 * 60 * 60) / runs  

    print(f"Scheduling {runs} tasks for the next 3 hours with an interval of {interval:.2f} seconds.")
    for i in range(runs):
        def task_wrapper():
            invoice = invoiceGenerator()
            invoice_list.append(invoice)
        threading.Timer(interval * i, task_wrapper).start()
        
def generateInvoices():       
    return starkbank.invoice.create([
        starkbank.Invoice(
            amount=random.randint(1, 9999999998),
            name=fake.name(),
            tax_id=generate_cpf(),
        )
    ])        


@api.route('/invoice')
class Starbank(Resource):
    @api.marshal_list_with(invoice)      
    def post(self):   
        """This endpoint issues 8 to 12 Invoices every 3 hours to random people for 24 hours."""
        invoicesCreated = []
        start_time = datetime.now()
        end_time = start_time + timedelta(hours=0.0625)

        print(f"Scheduler started at {start_time}. Will stop after onde day.")
    
        while datetime.now() < end_time:
            schedule_for_three_hours(generateInvoices, invoicesCreated)
            time.sleep(3 * 60 * 60)  
    
        print(f"Scheduler stopped at {datetime.now()}.")
        
        return invoicesCreated

        
@api.route('/transfer')
class Starbank(Resource):  
    @api.marshal_with(transfer)      
    def post(self): 
        """This endpoint processes webhook callbacks for Invoice credits and transfers the net amount (after fees) to the specified account."""
        invoices = starkbank.invoice.query(
            after=datetime.now() - timedelta(hours=24),
            before=datetime.now(),
            limit=100
        )
        
        total_to_be_transfered = 0
                
        for invoice in invoices: 
            if invoice.status == 'paid':
                total_to_be_transfered += invoice.amount - invoice.fee
        
        transfers = starkbank.transfer.create([
            starkbank.Transfer(
                amount=total_to_be_transfered,
                tax_id="20.018.183/0001-80",
                name="Stark Bank S.A.",
                bank_code="20018183",
                branch_code="0001",
                account_number="6341320293482496",
                account_type="payment"
            )
        ])
    
        return list(transfers)

if __name__ == '__main__':
    app.run(debug=True)