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
	
	$(".menu-item").click(function() {
		$( this ).toggleClass("menu-item-select ");
		if($(this).hasClass("menu-item-select")){
			dataToSend = {menuname: $("input[name='menuname']").val(), ingr: $(this).text(), change: 'Add'};
		}else{
			dataToSend = {menuname: $("input[name='menuname']").val(), ingr: $(this).text(), change: 'Rem'};
		}
		$( "#overlay" ).empty();
		$( "#overlay" ).load( "/UpdateIngr", dataToSend, function() {

			var totHeight = $(window).height();
			var totWidth = $(window).width();
			var titleHeight = $('#title-image').outerHeight(true);
			var optionsHeight = $('#options-bar').outerHeight(true);
			
			drawableHeight = $("#main-div").innerHeight() - titleHeight - optionsHeight;
			
			$("#selected-liquors").height(drawableHeight);
			$("#selected-liquors").width(100);
			
			$("#selected-mixers").height(drawableHeight);
			$("#selected-mixers").width(100);
			
			$("#cocktails-div").height(drawableHeight);
			$("#cocktails-div").width(totWidth-8-$("#selected-liquors").outerWidth(true) - $("#selected-mixers").outerWidth(true));
			
			var numItems = $('.liquor-ing').length + 1;
			var itemHeight = $('.liquor-ing').first().height();
			marg = (drawableHeight - numItems*itemHeight)/(numItems); 
			$('.liquor-ing').css( "margin-top",  marg);
						
			numItems = $('.mixer-ing').length + 1;
			itemHeight = $('.mixer-ing').outerHeight(true);
			marg = (drawableHeight - numItems*itemHeight)/(numItems); 
			$('.mixer-ing').css( "margin-top",  marg);
			$('.mixer-ing').css( "margin-bottom",  marg);
			
			numItems = $('.cocktail').length + 1;
			itemHeight = $('.cocktail').outerHeight(true);
			marg = (drawableHeight - numItems*itemHeight)/(numItems); 
			$('.cocktail').css( "margin-top",  marg);
			$('.cocktail').css( "margin-bottom",  marg);
			
			
		});
	});
	
	$("#change-view").click(function() {
//		$("#canvas-wrap").toggleClass("show hide");
		$("#ing-menu-div").toggleClass("show hide");
		$(".mixer-ing").toggleClass("show hide");
		$(".liquor-ing").toggleClass("show hide");
		$(".cocktail").toggleClass("show hide");
		($(this).text() === "Menu") ? $(this).text("Ingredients") : $(this).text("Menu");		
	});
	
});