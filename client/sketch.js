let asciiDiv

function setup()
{
    noCanvas()

    const ws = new WebSocket("ws://localhost:8000/ws");
    asciiDiv = createDiv()


    
    ws.onmessage = function(event) {
        
        let data = JSON.parse(event.data)

        ascii = data["ascii"]
        

        //used to make my string here but its faster on the server
        /*str = ""

        arr.forEach(el => {
            str += el.join('') + '<br/>'
        });
        
        ascii = ""


        for(let i = 0; i < str.length; i++) {
            let ch = str[i]
            if(ch == " ") {
                ascii += "&nbsp;"
            } else {
                ascii += ch;
            }
            
        }*/
        
        asciiDiv.innerHTML = "";
        asciiDiv.html(ascii)
    }
}

function draw()
{

}