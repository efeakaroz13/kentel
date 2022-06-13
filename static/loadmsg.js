function loadmsg(){
    var username;
    
    $.getJSON("/getUsername",function(data){
        username = data.username
        $.getJSON("/fetch/msgs",function(data){
            console.log(data.val.length)
            document.getElementById("msgs").innerHTML = "";
            data.val.reverse();
            for (let c = 0; c < data.val.length; c++) {
                const element = data.val[c];
                console.log(element)
                if (data["val"][c]["sender"] == username) {
                    userclass = "sender";
                    
                }
                else{
                    userclass = "reciever";
                    
                }
                
                document.getElementById("msgs").innerHTML = document.getElementById("msgs").innerHTML+"<p class="+userclass+">"+data["val"][c]["content"]+"</p>";
                document.scrollingElement.scrollBy(0,1000)

                
            }
        })
    })

    
}