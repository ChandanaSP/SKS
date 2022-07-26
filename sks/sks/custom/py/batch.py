import frappe
def item_price_creator(doc,action):
	# if doc.reference_doctype=="Purchase Receipt":
		ts_new_item_price=frappe.get_doc({
			"doctype":"Item Price",
			"item_code":doc.item,
			"price_list":"Standard Selling",
			"batch_no":doc.name,
			"price_list_rate":doc.ts_selling_price
		})
		ts_new_item_price.insert()
		ts_new_item_price.save()



# To remove is batch for already created item
def is_batch_remover():
	ts_items_doc=frappe.get_all("Item")
	if ts_items_doc:
		for ts_items in ts_items_doc:
			ts_item=frappe.get_doc("Item",ts_items)
			ts_item.has_batch_no=0
			ts_item.save()
