import frappe
from frappe.utils import flt
@frappe.whitelist()
def item_check_with_purchase_order(item_code_checking=None,checking_purchase_order=None):
	matched_item=0
	item_code_from_purchase_order=frappe.get_doc("Purchase Order",checking_purchase_order)
	total_item=item_code_from_purchase_order.__dict__["items"]
	len_items=len(total_item)
	if(item_code_checking != None):
		for j in range(0,len_items,1):
			if(item_code_checking == total_item[j].__dict__["item_code"]):
				item_code=total_item[j].__dict__["item_code"]
				matched_item=matched_item+1
				break
	if(matched_item==1):
		matched_item=0
		return item_code
	else:
		return 0
	
@frappe.whitelist()
def adding_barcode(barcode,item_code):
	item_barcode=frappe.get_doc("Item",item_code)
	item_barcode.append('barcodes',{'barcode':barcode})
	item_barcode.save()

from frappe.utils import getdate
@frappe.whitelist()
def auto_batch_creation(expiry_date=None,item_rate=None,item_code=None,item_mrp=None,total_barcode_number_item=None,total_barcode_item_code=None,against_purchase_order_name=None,doctype_name=None,document_name=None):
    expiry_date=eval(expiry_date)
    item_rate=eval(item_rate)
    item_code=eval(item_code)
    item_mrp=eval(item_mrp)
    total_barcode_item_code=eval(total_barcode_item_code)
    total_barcode_number_item=eval(total_barcode_number_item)
    matched_batch_name=[]
    matched_creation_date=[]
    item_changes_count=0
    item_changes_details=[]
    correct_batch_name=0
    changed_barcode=0
    batch_expiry=frappe.get_all("Batch",fields=["name","posa_btach_price","item","expiry_date","creation","ts_mrp"])
    for i in range(0,len(item_code),1):
        for j in range(0,(len(batch_expiry)),1):
                if(item_code[i]==batch_expiry[j]["item"]):
                    matched_batch_name.append(batch_expiry[j]["name"])
        for l in range(0,len(matched_batch_name),1):
            for n in range(0,(len(batch_expiry)),1):
                if(matched_batch_name[l]==batch_expiry[n]["name"]):
                    matched_creation_date.append(batch_expiry[n]["creation"])
        for c in range(0,(len(batch_expiry)),1):
            if(matched_creation_date!=[]):
                if(max(matched_creation_date)==batch_expiry[c]["creation"]):
                    correct_batch_name=batch_expiry[c]["name"]
                    formatted_expiry_date=getdate(expiry_date[i])
                    if(batch_expiry[c]["expiry_date"]!=formatted_expiry_date):
                        item_changes_count=item_changes_count+1
                        item_changes_details.append("Expiry date")
                    if(batch_expiry[c]["ts_mrp"]!=item_mrp[i]):
                        item_changes_count=item_changes_count+1
                        item_changes_details.append("MRP")
                    if(batch_expiry[c]["posa_btach_price"]!=item_rate[i]):
                        item_changes_count=item_changes_count+1
                        item_changes_details.append("Price")
        for b in range(0,len(total_barcode_item_code),1):
            if(item_code[i]==total_barcode_item_code[b]):
                item_changes_count=item_changes_count+1
                item_changes_details.append("Barcode")
                changed_barcode=total_barcode_number_item[b]
        item_document=frappe.get_doc(doctype_name,document_name)
        if(item_changes_count==0):
            frappe.db.set_value("Item",item_code[i],"create_new_batch",0)
            for item in item_document.items:
                if(item_code[i]==item.__dict__["item_code"]):
                    if(correct_batch_name!=0):
                        frappe.set_value(item.doctype,item.name,"batch_no",correct_batch_name)
        else:
            if(total_barcode_number_item):
                for item in item_document.items:
                    if(item_code[i]==item.__dict__["item_code"]):
                        if(changed_barcode!=0):
                            frappe.set_value(item.doctype,item.name,"barcode",changed_barcode)
            frappe.db.set_value("Item",item_code[i],"create_new_batch",1)
        item_changes_count=0
        item_changes_details=[]
    return 0
        
        
@frappe.whitelist()
def purchase_price_checking_with_order(e,po):
   item_changed=[]
   price_change_count=0
   item_code=[]
   item_rate=[]
   e=eval(e)
   k=(list(e.keys()))
   v=(list(e.values()))
   doc=frappe.get_doc("Purchase Order",po)
   total_item=doc.__dict__["items"]
   len_items=len(total_item)
   for j in range(0,len_items,1):
       item_code.append(total_item[j].__dict__["item_code"])
       item_rate.append(total_item[j].__dict__["rate"])
   for i in range(0,len(k),1):
           if(k[i]==item_code[i]):
               if(item_rate[i]!=v[i][0]):
                   item_changed.append(total_item[i].__dict__["item_name"])
                   price_change_count=price_change_count+1
   if(price_change_count==0):
        return 0
   else:
       return  item_changed


def markup_and_markdown_calculator(document,event):
    ts_items=document.items
    if ts_items:
        ts_val_rate=0
        ts_landed_cost_voucher_table=document.ts_landed_cost_voucher_table
        if ts_landed_cost_voucher_table:
            ts_val_rate=1
            ts_valuation_details=calculating_landed_cost_voucher_amount(document)
            ts_val_item=[]
            ts_val_rate=[]
            ts_val_tot_item=ts_valuation_details[0]
            ts_val_tot_rate=ts_valuation_details[1]
            for v in range(0,len(ts_val_tot_item),1):
                ts_val_item.append(ts_val_tot_item[v])
                ts_val_rate.append(ts_val_tot_rate[v])
            for item in document.get('items'):
                for vi in range(0,len(ts_val_item),1):
                    if ts_val_item[vi]==item.item_code:
                        ts_rate=ts_val_rate[vi]+item.rate
                        item.ts_valuation_rate=ts_rate
        else:
            for item in document.get('items'):
                item.ts_valuation_rate=item.rate
                        

        ts_item_code=[]
        ts_mrp=[]
        ts_valuation_rate=[]
        for item in document.get('items'):
            ts_item_code.append(item.item_code)
            ts_mrp.append(item.ts_mrp)
            ts_valuation_rate.append(item.ts_valuation_rate)
         
        ts_unmatched_item=[]
        ts_unmatched_selling_rate=[]
        ts_matched_item=[]
        ts_matched_selling_rate=[]
        for i in range(0,len(ts_item_code),1):
            ts_item_detais=frappe.get_doc("Item",ts_item_code[i])
            if ts_item_detais:
                if(ts_item_detais.__dict__["select_selling_price_type"]=="Markdown"):
                    ts_markdown=(ts_mrp[i]/100)*ts_item_detais.__dict__["ts_markdown_price"]
                    ts_markdown=ts_mrp[i]-ts_markdown
                    if(ts_markdown<ts_mrp[i] and ts_markdown>ts_valuation_rate[i]):
                        ts_matched_item.append(ts_item_code[i])
                        ts_matched_selling_rate.append(ts_markdown)
                    else:
                        ts_unmatched_item.append(ts_item_code[i])
                        ts_unmatched_selling_rate.append(ts_markdown)
                        
                elif(ts_item_detais.__dict__["select_selling_price_type"]=="Markup"):
                    ts_markup=(ts_mrp[i]/100)*ts_item_detais.__dict__["ts_markup_price"]
                    ts_markup=ts_valuation_rate[i]+ts_markup
                    if(ts_markup<ts_mrp[i] and ts_markup>ts_valuation_rate[i]):
                        ts_matched_item.append(ts_item_code[i])
                        ts_matched_selling_rate.append(ts_markup)
                    else:
                        ts_unmatched_item.append(ts_item_code[i])
                        ts_unmatched_selling_rate.append(ts_markup)
        for item in document.get('items'):
            for m in range (0,len(ts_matched_item),1):
                if item.item_code==ts_matched_item[m]:
                    item.ts_selling_rate=ts_matched_selling_rate[m]


def calculating_landed_cost_voucher_amount(self):
    total_item_cost = 0.0
    total_charges = 0.0
    item_count = 0
    ts_item_code=[]
    ts_separate_amount=[]
    based_on_field = frappe.scrub(self.ts_distribute_charges_based_on)
    for item in self.get('items'):
            total_item_cost += item.get(based_on_field)
    for item in self.get('items'):
            ts_total_value = flt(flt(item.get(based_on_field)) * (flt(self.ts_total_amount) / flt(total_item_cost)),
                )
            total_charges += ts_total_value
            item_count += 1
            ts_item_code.append(item.item_code)
            ts_separate_amount.append(ts_total_value)
    return ts_item_code,ts_separate_amount