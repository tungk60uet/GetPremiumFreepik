function getLink(){
    $("#btnSubmit").attr("disabled", "disabled");
    $("#btnSubmit").val("Processing")
    $.ajax({
        method: "POST",
        url: "/getlink",
        data: { link: $("#iplink").val()}
      }).done(function(msg) {
        $("#btnSubmit").removeAttr('disabled');
        $("#btnSubmit").val("Get Link");
        $("#ketqua").prepend(msg);   
      });
}