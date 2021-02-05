# Copyright (c) 2013, Patrick Ruckstuhl and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
import frappe

def execute(filters=None):
	columns = [{
		"fieldname": "name",
		"fieldtype": "Data",
		"label": "Name",
	},
  	{
		"fieldname": "zyklus",
		"fieldtype": "Int",
		"label": "Zyklus",
	},
	]
	
	cycles = frappe.db.get_list('ServiceCycle',
		fields=['name', 'zyklus'],
	)

	data = []
	for cycle in cycles:
		data.append({
			'name': cycle.name,
			'zyklus': cycle.zyklus,
		})


	return columns, data
