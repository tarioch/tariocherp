// Copyright (c) 2016, Patrick Ruckstuhl and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Next Service Cycle"] = {
	"filters": [
	],
	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (column.id == "yearsToNextService"){
			var color = 
				data["yearsToNextService"] > 0 ? "green" : 
				data["yearsToNextService"] == 0 ? "orange": "red";
			var $value = $(value).css("background-color", color);
			value = $value.wrap("<p></p>").parent().html();
		}
		return value;
	},
};

