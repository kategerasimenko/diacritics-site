$(document).ready(function(){
	$("#send").click(function(){
		var textarea = document.getElementById("text")
		var text = $('#text').val();
		var lang = $('#lang').val();
		$("#loading").show();
		$.post(
			'/',
			{'text':text,'selectlang':lang},
			function(response) {
				$("#diacritics").html(response['dias']);
				textarea.value = response['text'];
				$("#restored").show();
				$("#loading").hide();
				console.log("Sent");
			},
			"json"
		).error(function() {
			$("#restoredtext").html("Что-то пошло не так. Свяжитесь, пожалуйста, с создателем проекта по электронной почте: katgerasimenko@gmail.com.");
			$("#restored").show();
			$("#loading").hide();
		});
	});
});
