
function loadmsg(){
    var username;
    
    $.getJSON("/getUsername",function(data1){

        oldData = window.localStorage.getItem("old")
        console.log(oldData);
        username = data1.username
        $.getJSON("/fetch/msgs",function(data){

            if (data["val"].length != oldData){
                // console.log(data.val.length)
                document.getElementById("msgs").innerHTML = "";
                data.val.reverse();
                for (let c = 0; c < data.val.length; c++) {
                    const element = data.val[c];

                    if (data["val"][c]["sender"] == username) {
                        userclass = "sender";
                        
                    }
                    else{
                        userclass = "reciever";
                        
                    }

                    
                    document.getElementById("msgs").innerHTML = document.getElementById("msgs").innerHTML+"<p class="+userclass+">"+data["val"][c]["content"]+"</p>";
                    document.scrollingElement.scrollBy(0,1000)

                    
                }
            }
            window.localStorage.setItem('old', data["val"].length); 
        })
    })

    
}