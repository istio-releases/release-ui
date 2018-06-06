// Filter function for the search bar
function searchBar() {
  // Declare variables
  var input, filter, table, tr, td, i;
  input = document.getElementById("search-box");
  filter = input.value.toUpperCase();
  table = document.getElementById("dashboard");
  rows = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
	for (i = 0; i < rows.length; i++) {
		var exists = false
		for (j = 0; j < rows[i].getElementsByTagName("td").length; j++){
			td = rows[i].getElementsByTagName("td")[j];
			if (td) {
				if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
					exists = true;
					break;
				}
			}
		}
		if (!exists){
			rows[i].style.display = "none";
		}
		else {
			rows[i].style.display = "";
		}
	}
}

// Filter function for the tag and status dropdowns
// column 0 == status, column 5 == tags
function filter(label, column) {

	// Declare variables
  table = document.getElementById("dashboard");
  rows = table.getElementsByTagName("tr");

	for (i = 0; i < rows.length; i++) {
			td = rows[i].getElementsByTagName("td")[column];
			if (td) {
				if (td.innerHTML.toUpperCase().indexOf(label) > -1 || label == 0) {
					rows[i].style.display = "";
				} else {
					rows[i].style.display = "none";
				}
			}
	}
}

function statusFilter(label) {
	filter(label, 0)
}

function tagFilter(label) {
	filter(label, 5)
}

// Sort table alphabetically or reverse chronologically depending on column clicked
// function source: https://www.w3schools.com/howto/howto_js_sort_table.asp
function sortTable(column) {
  var table, rows, switching, i, x, y, shouldSwitch;
  table = document.getElementById("dashboard");
  switching = true;

  /* loop that will continue until no switching has been done: */
  while (switching) {

    switching = false;
    rows = table.getElementsByTagName("tr");

    for (i = 0; i < (rows.length - 1); i++) {
      shouldSwitch = false;
      /* Get the two elements you want to compare,
      one from current row and one from the next: */
      x = rows[i].getElementsByTagName("td")[column];
      y = rows[i + 1].getElementsByTagName("td")[column];

      var compare;
      if (column == 2 || column == 3){
        compare = Date.parse(x.innerHTML) < Date.parse(y.innerHTML)
      }
      else {
        compare = x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()
      }
      // Check if the two rows should switch place:
      if (compare) {
        // If so, mark as a switch and break the loop:
        shouldSwitch = true;
        break;
      }
    }
    if (shouldSwitch) {
      /* If a switch has been marked, make the switch
      and mark that a switch has been done: */
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
    }
  }
}

// Sort by Last Modified date when DOM is fully loaded
$(document).ready(function() {
    sortTable(3)
});
