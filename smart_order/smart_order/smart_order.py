from __future__ import unicode_literals
import frappe
from frappe import msgprint
from frappe.model.document import Document
from frappe.utils import money_in_words

def makeMR(doc,method):
	items = []
	for d in doc.items:
		if d.qty > d.actual_qty:
			mr = frappe.get_doc({
			"doctype": "Material Request", 
			"material_request_type": "Purchase", 
			"schedule_date": doc.transaction_date,
			"items": [{
				"item_code": d.item_code,
				"qty": d.qty-d.actual_qty,
				"so_qty": d.qty,
				"warehouse":d.warehouse
				}]
			})
			mr.insert(ignore_permissions=True)
			mr.save()

def addBarcode(doc,method):
	if not doc.barcode:
		br = frappe.get_doc({
		"doctype" : "Barcode Print",
		"item_code" : doc.item_code,
		"item_name" : doc.item_name,
		"barcode" : doc.barcode,
		"item_price":doc.standard_rate
		})
		br.insert(ignore_permissions=True)
		br.save()
	else:
		pass

def updateBarcode(doc,method):
	if doc.barcode:
		br = frappe.get_doc("Barcode Print",doc.item_code)
		br.barcode = doc.barcode
		br.item_price = doc.standard_rate
		br.save()
	else:
		pass
