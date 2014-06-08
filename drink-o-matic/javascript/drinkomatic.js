

$(document).ready(function() {
	$(".menu-item").click(function() {
		$( this ).toggleClass("menu-item-select ");
		if($(this).hasClass("menu-item-select")){
			dataToSend = {ingr: $(this).text(), change: 'Add'};
		}else{
			dataToSend = {ingr: $(this).text(), change: 'Rem'};
		}
		$( "#recipes" ).empty();
		$( "#recipes" ).load( "/UpdateIngr", dataToSend, function() {
			;
		});
	});	
});