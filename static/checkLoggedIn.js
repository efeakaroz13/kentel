function checkLoggedIn(){
    allCookies = document.cookie;
    if(allCookies.includes("username")){
        document.getElementsByTagName("body")[0].innerHTML = "<nav class='navbar navbar-light' style='background-color: #d9a211;padding-left:10px;color:white'><a href='/' style='text-decoration:none;color:white;'><img src='/static/socialCorn.png' width='30'>Social Corn<a href='/inbox' style='text-align:right;margin-right:10px'><img src='/static/CORNDM.png' width='30'></a></a></nav>"+ document.getElementsByTagName("body")[0].innerHTML;
        
    }
    else{
        document.getElementsByTagName("body")[0].innerHTML = "<nav class='navbar navbar-light' style='background-color: #d9a211;padding-left:10px;color:white'><a href='/' style='text-decoration:none; color:white'><img src='/static/socialCorn.png' width='30'>Social Corn</a></nav>"+ document.getElementsByTagName("body")[0].innerHTML;
        
    }
}
checkLoggedIn()