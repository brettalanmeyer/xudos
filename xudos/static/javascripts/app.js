$(function(){

	jQuery.fn.extend({
		exists: function(){
			return this.length > 0;
		}
	});

	$(".alert-dismissible").each(function(){
		var source = $(this);

		if(source.hasClass("auto-close")){
			setTimeout(function(){
				source.fadeOut();
			}, 3000);
		}

		source.find(".close").on("click", function(){
			source.fadeOut("fast");
		});
	});

	var deleteConfirm = $("#deleteConfirmModal");

	$("form .action-delete").on("click", function(){
		$(this).addClass("modal-active-delete-button");
		deleteConfirm.modal();
		return false;
	});

	deleteConfirm.find(".action-confirm").on("click", function(){
		$(".modal-active-delete-button").parent("form").submit();
	});

	deleteConfirm.on("hide.bs.modal", function(){
		$(".modal-active-delete-button").removeClass("modal-active-delete-button");
	});


	var slideShow = $("#xudo-slideshow");

	if(slideShow.exists()){

		var slide = 0;
		var xudos = slideShow.find(".xudo");

		setInterval(next, slideShow.data("delay"));

		function next(){
			xudos.eq(slide).removeClass("active");

			slide++;

			if (slide >= xudos.length){
				slide = 0;
			}

			xudos.eq(slide).addClass("active");
		}


		var navigation = $("nav");
		var navHidden = false;

		function hideNav() {
			navigation.fadeOut("slow");
			navHidden = true;
		}

		function showNav() {
			navHidden = false;
			navigation.fadeIn("slow");
			setTimeout(hideNav, 5000);
		}

		setTimeout(hideNav, 2000);

		$(document).on("mousemove", function(event){
			if(navHidden && event.pageY < 60){
				showNav();
			}
		});

	}

});
