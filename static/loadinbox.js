function loadinbox(){
    $.getJSON("/api/dmbox",function(data){
        document.body.getElementsByTagName("ul")[0].innerHTML = "";
        listThing = document.body.getElementsByTagName("ul")[0]
        for (let i = 0; i < data.inbox.length; i++) {
            const element = data.inbox[i];
            console.log(data.inbox[i])
            document.body.getElementsByTagName("ul")[0].innerHTML = document.body.getElementsByTagName("ul")[0].innerHTML+"<li  class='list-group-item'><a href='/chat/"+data.inbox[i]["chatid"]+"'>"+data.inbox[i]["username"]+"</a></li>"
            
        }


    })
}
loadinbox()
setInterval(loadinbox,5000)