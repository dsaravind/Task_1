from jinja2 import Environment, FileSystemLoader
import pdfkit
from babel.numbers import format_currency
import os

def amount_in_words(number):
    from num2words import num2words
    return num2words(number, to='currency', lang='en_IN').replace('INR', 'Rupees')

def generate_invoice(data):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('invoice_template.html')

    for item in data['items']:
        item['net_amount'] = item['unit_price'] * item['quantity'] - item['discount']
        if data['place_of_supply'] == data['place_of_delivery']:
            item['tax_type'] = 'CGST & SGST'
            item['tax_amount'] = item['net_amount'] * item['tax_rate'] / 2
            item['total_amount'] = item['net_amount'] + item['tax_amount'] * 2
        else:
            item['tax_type'] = 'IGST'
            item['tax_amount'] = item['net_amount'] * item['tax_rate']
            item['total_amount'] = item['net_amount'] + item['tax_amount']

    data['total_amount'] = sum(item['total_amount'] for item in data['items'])
    data['amount_in_words'] = amount_in_words(data['total_amount'])

    html_content = template.render(data)

    pdfkit.from_string(html_content, 'invoice.pdf')

if __name__ == "__main__":
    data = {
        "logo": "path/to/logo.png",
        "seller_name": "Seller Name",
        "seller_address": "Seller Address, City, State, Pincode",
        "seller_pan": "ABCDE1234F",
        "seller_gst": "12ABCDE1234F1Z5",
        "place_of_supply": "State",
        "billing_name": "Billing Name",
        "billing_address": "Billing Address, City, State, Pincode",
        "shipping_name": "Shipping Name",
        "shipping_address": "Shipping Address, City, State, Pincode",
        "order_no": "ORD123456",
        "order_date": "2024-06-04",
        "invoice_no": "INV123456",
        "invoice_date": "2024-06-04",
        "reverse_charge": "No",
        "place_of_delivery": "State",
        "items": [
            {
                "description": "Item 1",
                "unit_price": 100.0,
                "quantity": 2,
                "discount": 10.0,
                "tax_rate": 0.18
            },
            {
                "description": "Item 2",
                "unit_price": 200.0,
                "quantity": 1,
                "discount": 0.0,
                "tax_rate": 0.18
            }
        ],
        "signature": "path/to/signature.png"
    }

    generate_invoice(data)

