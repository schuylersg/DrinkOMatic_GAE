$(document).ready(function() {
	var totHeight = $(window).height();
	var totWidth = $(window).width();
	var titleHeight = $('#title-image').outerHeight(true);
	var optionsHeight = $('#options-bar').outerHeight(true);
	$("#main-div").height(totHeight-18);
	$("#main-div").width(totWidth-8);	
	
	drawableHeight = $("#main-div").innerHeight() - titleHeight - optionsHeight;
	
	$("#canvas-wrap").height(drawableHeight);
	$("#canvas-wrap").width($("#main-div").innerWidth());
	$("canvas").height(drawableHeight);
	
	$("#selected-liquors").height(drawableHeight);
	$("#selected-liquors").width(100);
	
	$("#selected-mixers").height(drawableHeight);
	$("#selected-mixers").width(100);

	$("#cocktails-div").height(drawableHeight);
	$("#cocktails-div").width(totWidth-8-200);
	
	$(".menu-item").click(function() {
		$( this ).toggleClass("menu-item-select ");
		if($(this).hasClass("menu-item-select")){
			dataToSend = {ingr: $(this).text(), change: 'Add'};
		}else{
			dataToSend = {ingr: $(this).text(), change: 'Rem'};
		}
		$( "#overlay" ).empty();
		$( "#overlay" ).load( "/UpdateIngr", dataToSend, function() {

			var totHeight = $(window).height();
			var totWidth = $(window).width();
			var titleHeight = $('#title-image').outerHeight(true);
			var optionsHeight = $('#options-bar').outerHeight(true);
			$("#main-div").height(totHeight-18);
			$("#main-div").width(totWidth-8);	
			
			drawableHeight = $("#main-div").innerHeight() - titleHeight - optionsHeight;
			
			$("#canvas-wrap").height(drawableHeight);
			$("#canvas-wrap").width($("#main-div").innerWidth());
			$("canvas").height(drawableHeight);
			
			$("#selected-liquors").height(drawableHeight);
			$("#selected-liquors").width(100);
			
			$("#selected-mixers").height(drawableHeight);
			$("#selected-mixers").width(100);

			$("#cocktails-div").height(drawableHeight);
			$("#cocktails-div").width(totWidth-8-200);	
		
		});
	});
	
	$("#change-view").click(function() {
		$("#canvas-wrap").toggleClass("show hide");
		$("#ing-menu-div").toggleClass("show hide");
		($(this).text() === "Menu") ? $(this).text("Ingredients") : $(this).text("Menu");		
	});
	
});