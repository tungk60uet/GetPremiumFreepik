function getLink(){
	$("body").append("<p id='txtWait'>Đợi tí nhóe đang xử lý hihi</p>");
	$("#btnSubmit").remove();
    $.ajax({
        method: "POST",
        url: "/getlink",
        data: { link: $("#iplink").val()}
      }).done(function(msg) {
      	$("#txtWait").remove();
      	$("body").append("<br><a href='"+msg+"' target='_blank'>Download</a>");
      });
}