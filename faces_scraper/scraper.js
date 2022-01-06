
ville = "{{keyword}}"
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  
function isHidden(el) {
    return (el.offsetParent === null)
}

(async () => {
    data = []
    url = []
    while (isHidden(document.querySelectorAll(".Yu2Dnd")[0])){
        if(!isHidden(document.querySelectorAll(".mye4qd")[0])){
            document.querySelectorAll(".mye4qd")[0].click()
        }

        window.scrollTo(0, window.scrollY+750);
        document.querySelectorAll(".Q4LuWd").forEach((el) => {
            if (!url.includes(el.getAttribute("src")) && el.getAttribute("src")!= null){
                data.push({
                    "src": el.getAttribute("src"),
                    "alt":el.getAttribute("alt"),
                    "keyword" : ville
                })
                url.push(el.getAttribute("src"))
            }
        });
        await sleep(500)
    }
    console.log("got "+data.length+" out of "+document.querySelectorAll(".Q4LuWd").length)
    console.log(data.length*100/document.querySelectorAll(".Q4LuWd").length+"%")
})();

