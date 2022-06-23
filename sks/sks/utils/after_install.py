from sks.sks.utils.buying.purchase_order.purchase_order_custom_fields import purchase_order_customization
from sks.sks.utils.buying.purchase_receipt.purchase_receipt_custom import purchase_receipt_customization
from sks.sks.utils.buying.purchase_invoice.purchase_invoice_custom_fields import purchase_invoice_customization          
from sks.sks.utils.selling.delivery_note.delivery_note_custom_fields import delivery_note_customization
from sks.sks.utils.selling.sales_order.sales_order_custom_fields import sales_order_customization
from sks.sks.utils.selling.sales_invoice.sales_invoice_custom_fields import sales_invoice_customization
from sks.sks.utils.stock.item.item_custom_fields import item_customization
from sks.sks.utils.crm.customer.customer_custom_fields import customer_customization
from sks.sks.utils.stock.item.item_barcode_custom_fields import item_barcode_customization
from sks.sks.utils.stock.item.item_tax_custom_fields import item_tax_customization
from sks.sks.utils.stock.material_request.material_request_custom_fields import material_request_customization
from sks.sks.utils.stock.batch.batch_custom_fields import batch_customization
from sks.sks.utils.stock.delivery_trip.delivery_trip_custom_fields import delivery_trip_customization
from sks.sks.utils.hr.driver.driver_custom_fields import driver_customization
from sks.sks.utils.hr.attendance.attendance_custom_fields import create_attendance_property_setter
from sks.sks.utils.hr.employee.employee_custom_fields import create_employee_property_setter
from sks.sks.utils.hr.employee_checkin.employee_checkin_custom_fields import create_employee_checkin_property_setter
from sks.sks.utils.hr.payroll_entry.payroll_entry_custom_fields import create_payroll_entry_property_setter
from sks.sks.utils.hr.salary_slip.salary_slip_custom_fields import create_salary_slip_property_setter
from sks.sks.utils.hr.salary_structure.salary_structure_custom_fields import create_salary_structure_property_setter

def after_install():
    purchase_order_customization()
    delivery_note_customization()
    sales_order_customization()
    sales_invoice_customization()
    item_customization()
    purchase_invoice_customization()
    purchase_receipt_customization()
    customer_customization()
    item_tax_customization()
    item_barcode_customization()
    material_request_customization()
    batch_customization()
    delivery_trip_customization()
    driver_customization()
    create_attendance_property_setter()
    create_employee_property_setter()
    create_employee_checkin_property_setter()
    create_payroll_entry_property_setter()
    