import re
import frappe
from qrbill import QRBill
import tempfile

def create_address(name, address):
  p = re.compile(r'(?P<STREET>.*)\s(?P<HOUSE_NR>\d[0-9a-z]*)')
  line1 = address.address_line1
  street = line1
  house = None
  m = p.match(line1)
  if m:
    street = m.group('STREET')
    house = m.group('HOUSE_NR')

  return {
    'name': name,
    'street': street,
    'house_num': house,
    'pcode': address.pincode,
    'city': address.city,
    'country': address.country,
  }

@frappe.whitelist()
def generate_qrbill(doc):
  company = frappe.get_doc('Company', doc.company)
  account = frappe.db.get_value('Bank Account', {'account': company.default_bank_account}, 'iban')
  companyAddress = frappe.get_doc('Address', doc.company_address)
  customerAddress = frappe.get_doc('Address', doc.customer_address)

  bill = QRBill(
    language='de',
    font_factor=0.8,
    account=account,
    creditor=create_address(doc.company, companyAddress),
    debtor = create_address(doc.customer_name, customerAddress),
    amount=str(doc.grand_total),
  )
  with tempfile.TemporaryFile(encoding='utf-8', mode='r+') as temp:
    bill.as_svg(temp)
    temp.seek(0)

    content = temp.read().replace('<?xml version="1.0" encoding="utf-8" ?>', '')
    return content
