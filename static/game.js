function tdclick(coordinate) {
    chosenpiece = selectedPiece()
    if(document.getElementById(coordinate).style.backgroundColor == "red"){
        movePiece(chosenpiece, coordinate)
    }
    else{
        console.log(document.getElementById(coordinate).getAttribute("moving"));

        darkspaces = document.getElementsByClassName('dark');
        lightspaces = document.getElementsByClassName('light');
        for (let i = 0; i < darkspaces.length; i++) {
            darkspaces[i].style.backgroundColor = "#aaa";
            lightspaces[i].style.backgroundColor = "#eee";
        }
        
        document.getElementById(coordinate).style.border = "medium solid #000"
        document.getElementById(coordinate).setAttribute("moving", "true")
    
        let xhr = new XMLHttpRequest();
        paths = window.location.pathname.split("/");
        code = paths[paths.length - 1];
        console.log(paths)
        console.log(code)
        xhr.open("GET", "/legalmoves/" + code + "/" + coordinate, false);
        xhr.onload = function () {
            // Process our return data
            if (xhr.status >= 200 && xhr.status < 300) {
                // Runs when the request is successful
                moves = xhr.responseText;
            } else {
                // Runs when it's not
                moves = "None";
            }
        };
        xhr.send();
        moveArray = moveParser(moves);
        console.log(moveArray);
        console.log(moveArray.length);
        for (let i = 0; i < moveArray.length; i++) {
            console.log(moveArray[0]);
            document.getElementById(String(moveArray[i])).style.backgroundColor = "red";
        }
    }
}

function moveParser(moves){
    myArr = [];
    for(let i = 0; i < moves.length; i+=2){
        myArr.push(moves.substring(i,i+2))
    }
    return myArr;
}

function selectedPiece(){
    let cols = ["a", "b", "c", "d", "e", "f", "g", "h"]
    let rows = ["1", "2", "3", "4", "5", "6", "7", "8"]
    let selected_piece = "none"
    for(let i = 0; i < 8; i++){
        idx1 = cols[i]
        for(let j = 0; j < 8; j++){
            idx2 = rows[j]
            if(document.getElementById(idx1+idx2).getAttribute("moving") == "true"){
                selected_piece = idx1+idx2;
            }
            document.getElementById(idx1+idx2).style.border = "none"
            document.getElementById(idx1+idx2).setAttribute("moving", "false")
        }
    }
    return selected_piece
}

function movePiece(piece, move){
    alternateClocks();
    let xhr = new XMLHttpRequest();
    paths = window.location.pathname.split("/");
    code = paths[paths.length - 1];
    console.log(move)
    console.log(piece)
    xhr.open("POST", "/move/" + code, false);
    xhr.setRequestHeader(
      "content-type",
      "application/x-www-form-urlencoded;charset=UTF-8"
    );
    xhr.onload = function () {
      // Process our return data
      if (xhr.status >= 200 && xhr.status < 300) {
        // Runs when the request is successful
        newhtml = xhr.responseText;
        document.getElementById("chessgamebelow").innerHTML = newhtml;
        
      } else {
        // Runs when it's not
      }
    };
    xhr.send("move=" + move+ "&piece=" +piece);
}

function sendMessage(){
    paths = window.location.pathname.split("/");
    code = paths[paths.length - 1];
    const comment = document.getElementById("myMessage").value;
    document.getElementById("myMessage").value = ""
    socket.send(JSON.stringify({comment: comment, code: code}))
}

socket.on("newMessage", function (msg) {
    message = msg["messages"];
    document.getElementById("messages").innerHTML += "<p>"+message+"</p>"
  });

socket.on("newMove", function (move) {
    alternateClocks();
    let xhr = new XMLHttpRequest();
    paths = window.location.pathname.split("/");
    code = paths[paths.length - 1];
    xhr.open("GET", "/game/" + code, false);
    xhr.onload = function () {
        // Process our return data
        if (xhr.status >= 200 && xhr.status < 300) {
            // Runs when the request is successful
            newhtml = xhr.responseText;
            document.getElementById("chessgamebelow").innerHTML = newhtml;
        } else {
            // Runs when it's not
        }
    };
    xhr.send();
  });



function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(";");
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == " ") {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "none";
}

function alternateClocks() {
    let xhr = new XMLHttpRequest();
    paths = window.location.pathname.split("/");
    code = paths[paths.length - 1];
    xhr.open("GET", "/turn/" + code, false);
    xhr.onload = function () {
        // Process our return data
        if (xhr.status >= 200 && xhr.status < 300) {
            // Runs when the request is successful
            turn = xhr.responseText;
            console.log(turn)
        } else {
            // Runs when it's not
        }
    };
    xhr.send();
    try{
        clearInterval(clock1)
        updateWhiteTime(document.getElementById("countdown1").innerHTML)
    } catch (error){
        console.log("ERROR")
    }
    try{
        clearInterval(clock2)
        updateBlackTime(document.getElementById("countdown2").innerHTML)
    } catch (error){
        console.log("ERROR")
    }
    if(turn == "white"){
        clock1 = setInterval(updateCountdown1, 1000);
    }
    else{
        clock2 = setInterval(updateCountdown2, 1000);
    }
}

function updateCountdown1() {
    let time = document.getElementById('countdown1').innerHTML;
    const countdownElement = document.getElementById('countdown1');
    const minutes = Math.floor(time/60);
    let seconds = time % 60;

    seconds = seconds < 10 ? '0' + seconds : seconds;
    time--;
    countdownElement.innerHTML = `${time}`;
    
}

function updateCountdown2() {
    let time = document.getElementById('countdown2').innerHTML;
    const countdownElement = document.getElementById('countdown2');
    const minutes = Math.floor(time/60);
    let seconds = time % 60;

    seconds = seconds < 10 ? '0' + seconds : seconds;
    time--;
    countdownElement.innerHTML = `${time}`;
    if(time <= 0){
        
    }
}

function updateWhiteTime(seconds) {
    let xhr = new XMLHttpRequest();
    paths = window.location.pathname.split("/");
    code = paths[paths.length - 1];
    xhr.open("POST", "/whitetime/" + code, false);
    xhr.setRequestHeader(
      "content-type",
      "application/x-www-form-urlencoded;charset=UTF-8"
    );
    xhr.onload = function () {
      // Process our return data
      if (xhr.status >= 200 && xhr.status < 300) {
        // Runs when the request is successful
      } else {
        // Runs when it's not
      }
    };
    xhr.send("time=" + seconds);
}

function updateBlackTime(seconds) {
    let xhr = new XMLHttpRequest();
    paths = window.location.pathname.split("/");
    code = paths[paths.length - 1];
    xhr.open("POST", "/blacktime/" + code, false);
    xhr.setRequestHeader(
      "content-type",
      "application/x-www-form-urlencoded;charset=UTF-8"
    );
    xhr.onload = function () {
      // Process our return data
      if (xhr.status >= 200 && xhr.status < 300) {
        // Runs when the request is successful
      } else {
        // Runs when it's not
      }
    };
    xhr.send("time=" + seconds);
}