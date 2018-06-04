function handle(e){
	search=document.getElementById("search-box").value;
    if(e.keyCode === 13){
      $.post("receiver", search, function(){
      });
    }
	return false;
}

// Execute when DOM is fully loaded
$(document).ready(function() {
	var dataObject = {
		0: {"version":"xxx-xxx-123","status":true,"creation":"mm/dd/yy at hh:mm:ss","last_mod":"mm/dd/yy at hh:mm:ss","last_active":"task123","tag":1},
		1: {"version":"xxx-xxx-456","status":true,"creation":"mm/dd/yy at hh:mm:ss","last_mod":"mm/dd/yy at hh:mm:ss","last_active":"task456","tag":2}
	};

	// Cache of the template
	var template = document.getElementById("template-dashboard-list");
	// Get the contents of the template
	var templateHtml = template.innerHTML;
	// Final HTML variable as empty string
	var listHtml = "";

	// Loop through dataObject, replace placeholder tags
	// with actual data, and generate final HTML
	for (var key in dataObject) {
	  listHtml += templateHtml.replace(/{{version}}/g, dataObject[key]["version"])
	                          .replace(/creation/g, dataObject[key]["creation"])
	                          .replace(/{{last_change}}/g, dataObject[key]["last_mod"])
	                          .replace(/{{last_active}}/g, dataObject[key]["last_active"])
	                          .replace(/{{tag}}/g, dataObject[key]["tag"]);
	}

	document.getElementById("dashboard-list").innerHTML = listHtml;
});
