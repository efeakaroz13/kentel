function themeset(){
    const darkThemeMq = window.matchMedia("(prefers-color-scheme: dark)");
    if (darkThemeMq.matches) {
        document.getElementById("icon").href = "/static/kentel-light.png"
        // var link = document.querySelector("link[rel~='icon']");
        // if (!link) {
        //     link = document.createElement('link');
        //     link.rel = 'icon';
        //     document.getElementsByTagName('head')[0].appendChild(link);
        // }
        // link.href = 'https://stackoverflow.com/favicon.ico';
    } else {
        document.getElementById("icon").href = "/static/kentel.png"
    }
}
themeset()
setInterval(themeset,5000)