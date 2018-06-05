// Filter function for the search bar
function searchBar() {
  // Declare variables
  var input, filter, table, tr, td, i;
  input = document.getElementById("search-box");
  filter = input.value.toUpperCase();
  table = document.getElementById("dashboard-list");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
	for (i = 0; i < tr.length; i++) {
		var exists = false
		for (j = 0; j < tr[i].getElementsByTagName("td").length; j++){
			td = tr[i].getElementsByTagName("td")[j];
			if (td) {
				if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
					exists = true;
					break;
				}
			}
		}
		if (!exists){
			tr[i].style.display = "none";
		}
		else {
			tr[i].style.display = "";
		}
	}
}

// Filter function for the tag drop down
function tagFilter(label) {

	// Declare variables
  table = document.getElementById("dashboard-list");
  tr = table.getElementsByTagName("tr");

	for (i = 0; i < tr.length; i++) {
			td = tr[i].getElementsByTagName("td")[5];
			if (td) {
				if (td.innerHTML.toUpperCase().indexOf(label) > -1 || label == 0) {
					tr[i].style.display = "";
				} else {
					tr[i].style.display = "none";
				}
			}
	}
}
