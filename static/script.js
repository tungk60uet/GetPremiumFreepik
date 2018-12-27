function getLink(){
    $("#btnSubmit").attr("disabled", "disabled");
    t=10;
    var countDown=setInterval(function(){
      if(t>0){
        $("#btnSubmit").val("Wait about "+t+"s");
      }
      else{
        $("#btnSubmit").val("Processing..."); 
        clearInterval(countDown);
      }
      t--;
    }, 1000);
    
    $.ajax({
        method: "POST",
        url: "/getlink",
        data: { link: $("#iplink").val()}
      }).done(function(msg) {
        clearInterval(countDown)
        $("#btnSubmit").removeAttr('disabled');
        $("#btnSubmit").val("Get Link");
        $("#result").prepend(msg);   
      });
}