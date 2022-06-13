function checkLoggedIn(){
    allCookies = document.cookie;
    if(allCookies.includes("username")){
        document.getElementsByTagName("body")[0].innerHTML = "<nav class='navbar navbar-light bg-dark' style='padding-left:10px;color:white'><a href='/' style='text-decoration:none;color:white;'><img src='/static/kentel-light.png'style='margin-right:20px' width='30'>Kentel<a href='/inbox' style='text-align:right;margin-right:10px'><img src='/static/CORNDM.png' width='30'></a></a></nav>"+ document.getElementsByTagName("body")[0].innerHTML;
        
    }
    else{
        document.getElementsByTagName("body")[0].innerHTML = "<nav class='navbar navbar-light bg-dark' style='padding-left:10px;color:white'><a href='/' style='text-decoration:none; color:white'><img src='/static/kentel-light.png'style='margin-right:20px' width='30'>Kentel</a></nav>"+ document.getElementsByTagName("body")[0].innerHTML;
        
    }
}
checkLoggedIn()