function handle(e){
	search=document.getElementById("search-box").value;
    if(e.keyCode === 13){
      $.post("receiver", search, function(){

      });
    }
	return false;
}
