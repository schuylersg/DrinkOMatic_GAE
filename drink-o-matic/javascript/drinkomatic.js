

$(document).ready(function() {
	var height = $(window).height() - 75; 
	$("#main-div").height(height);

	$("#canvas-wrap").height(height-100);
	$("canvas").height(height-100);
	
	$(".menu-item").click(function() {
		$( this ).toggleClass("menu-item-select ");
		if($(this).hasClass("menu-item-select")){
			dataToSend = {ingr: $(this).text(), change: 'Add'};
		}else{
			dataToSend = {ingr: $(this).text(), change: 'Rem'};
		}
		$( "#overlay" ).empty();
		$( "#overlay" ).load( "/UpdateIngr", dataToSend, function() {
			;
		});
	});
	
	$("#change-view").click(function() {
		$("#canvas-wrap").toggleClass("show hide");
		$("#ing-menu-div").toggleClass("show hide");
	});
	
});