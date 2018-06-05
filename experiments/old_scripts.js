// Execute when DOM is fully loaded
$(document).ready(function() {
	var dataObject = {
		0: {"version":"xxx-xxx-123","status":true,"creation":"mm/dd/yy at hh:mm:ss","last_mod":"mm/dd/yy at hh:mm:ss","last_active":"task123","tag":[1,3]},
		1: {"version":"xxx-xxx-456","status":true,"creation":"mm/dd/yy at hh:mm:ss","last_mod":"mm/dd/yy at hh:mm:ss","last_active":"task456","tag":[2]}
	};

	// Cache of the template
	var template = document.getElementById("template-dashboard-list");
	// Get the contents of the template
	var templateHtml = template.innerHTML;

	var button = document.getElementById("template-tag");
	var buttonHtml = button.innerHTML;

	// Final HTML variable as empty string
	var listHtml = "";

	// Loop through dataObject, replace placeholder tags
	// with actual data, and generate final HTML
	for (var key in dataObject) {

		var buttons = "";
		for (var i in dataObject[key]["tag"]){
			var label;
			if (dataObject[key]["tag"][i] == 1){
				label = "auto"
			} else if (dataObject[key]["tag"][i] == 2){
				label = "daily"
			} else if (dataObject[key]["tag"][i] == 3){
				label = "weekly"
			} else {
				label = "monthly"
			}

			buttons += buttonHtml.replace(/tag/g, label);
		}

	  listHtml += templateHtml.replace(/version/g, dataObject[key]["version"])
	                          .replace(/creation/g, dataObject[key]["creation"])
	                          .replace(/last_change/g, dataObject[key]["last_mod"])
	                          .replace(/last_active/g, dataObject[key]["last_active"])
														.replace(/tags/g, buttons);
	}

	document.getElementById("dashboard-list").innerHTML = listHtml;
});
