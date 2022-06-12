function loadmsg(chatid){
    $.getJSON("/fetch/msgs/"+chatid,function(data){

        console.log(data)
    })
}