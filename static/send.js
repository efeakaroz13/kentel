function sendmsg(chatid,theid){
    $.post("/msg/send/"+chatid,{msg:document.getElementById(theid).value},function(data){
        console.log(data)
    })
}