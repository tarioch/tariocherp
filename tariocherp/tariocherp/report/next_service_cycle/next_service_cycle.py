# Copyright (c) 2013, Patrick Ruckstuhl and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from dateutil.relativedelta import relativedelta
import datetime

def execute(filters=None):
	columns = [{
		"fieldname": "name",
		"fieldtype": "Data",
		"label": "Name",
	},
  	{
		"fieldname": "cycle",
		"fieldtype": "Int",
		"label": "Zyklus",
	},
	{
		"fieldname": "lastService",
		"fieldtype": "Date",
		"label": "Letzer Service",
	},
  	{
		"fieldname": "yearsToNextService",
		"fieldtype": "Int",
		"label": "Jahre bis nächster Service",
	},
	]
	
	cycles = frappe.get_list('ServiceCycle',
		fields=['name', 'cycle'],
	)

	data = []
	for cycle in cycles:
		lastServices = frappe.get_all('Service',
			fields = ['date'],
			filters = [
				["parent","=", cycle.name]
			],
			order_by = 'date desc',
			page_length = 1,
		)

		lastService = None
		yearsSinceService = cycle.cycle
		if lastServices:
			lastService = lastServices[0]
			yearsSinceService = relativedelta(datetime.date.today(), lastService.date).years

		data.append({
			'name': cycle.name,
			'cycle': cycle.cycle,
			'lastService': lastService,
			'yearsToNextService': cycle.cycle - yearsSinceService,
		})

	return columns, data
