// From http://stackoverflow.com/a/10727155
function randomString(length) {
    return Math.round((Math.pow(36, length + 1) - Math.random() * Math.pow(36, length))).toString(36).slice(1);
}


$(document).on("click", "#upload", function(){
	validateForm();
})

$(document).ready(function() {
	var uploadID = randomString(6);

	$("#uploadID").val(uploadID)
});

function validateForm() {
	var email, filters, format, uploadID;

	email = $("#email").val();
	format = $("input[name=format]:checked").val();

		console.log("email")
        console.log(email)
	console.log("")
	console.log("format")
	console.log(format)

	uploadID = randomString(6);

	$("#uploadID").attr("value", upload)
}


