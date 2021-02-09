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
	services = frappe.get_list('Service',
		fields=['parent', 'date'],
	)

	data = []
	for cycle in cycles:
		lastService = max([s.date for s in services if s.parent == cycle.name])
		yearsSinceService = None
		if lastService:
			yearsSinceService = relativedelta(datetime.date.today(), lastService).years

		data.append({
			'name': cycle.name,
			'cycle': cycle.cycle,
			'lastService': lastService,
			'yearsToNextService': cycle.cycle - yearsSinceService,
		})

	return columns, data
