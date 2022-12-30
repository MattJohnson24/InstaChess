const username = document.getElementById('username')
const password = document.getElementById('password')
const confirmpassword = document.getElementById('confirmpassword')
const form = document.getElementById('form')
const errorElement = document.getElementById('error')

if(form){
    form.addEventListener('submit', (e) => {
        submit_error = false;
        if (username.value === '' || username.value === null){
            document.getElementById("missingusername-error").style.display = "block";
            submit_error = true;
        }
        else{
            document.getElementById("missingusername-error").style.display = "none";
        }
    
        if (password.value === '' || password.value === null){
            document.getElementById("missingpassword-error").style.display = "block";
            submit_error = true;
        }
        else{
            document.getElementById("missingpassword-error").style.display = "none";
        }

        try{
            if (confirmpassword.value === '' || confirmpassword.value === null){
                document.getElementById("missingconfirmpassword-error").style.display = "block";
                submit_error = true;
            }
            else{
                document.getElementById("missingconfirmpassword-error").style.display = "none";
            }
            
            if (confirmpassword.value !=  password.value){
                document.getElementById("matchingpassword-error").style.display = "block";
                submit_error = true;
            }
            else{
                document.getElementById("matchingpassword-error").style.display = "none";
            }
        }
        catch(error){

        }

        if (submit_error){
            e.preventDefault()
        }
    })
}

function currentSlide(slide){
    if(slide == 1){
        document.getElementsByClassName("profile-slide")[0].style.display = "none";
        document.getElementsByClassName("leaderboard-slide")[0].style.display = "none";
        document.getElementById("side-img").style.display = "block";
        document.getElementById("dot1").style.backgroundColor = "#000000";
        document.getElementById("dot2").style.backgroundColor = "#ffffff";
        document.getElementById("dot3").style.backgroundColor = "#ffffff";
    }
    else if(slide == 2){
        document.getElementsByClassName("profile-slide")[0].style.display = "block";
        document.getElementsByClassName("leaderboard-slide")[0].style.display = "none";
        document.getElementById("side-img").style.display = "none";
        document.getElementById("dot1").style.backgroundColor = "#ffffff";
        document.getElementById("dot2").style.backgroundColor = "#000000";
        document.getElementById("dot3").style.backgroundColor = "#ffffff";
    }
    else{
        document.getElementsByClassName("profile-slide")[0].style.display = "none";
        document.getElementsByClassName("leaderboard-slide")[0].style.display = "block";
        document.getElementById("side-img").style.display = "none";
        document.getElementById("dot1").style.backgroundColor = "#ffffff";
        document.getElementById("dot2").style.backgroundColor = "#ffffff";
        document.getElementById("dot3").style.backgroundColor = "#000000";
    }
}