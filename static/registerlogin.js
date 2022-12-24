const username = document.getElementById('username')
const password = document.getElementById('password')
const confirmpassword = document.getElementById('confirmpassword')
const form = document.getElementById('form')
const errorElement = document.getElementById('error')

if(form){
    form.addEventListener('submit', (e) => {
        let messages = []
        console.log(username)
        if (username.value === '' || username.value === null){
            messages.push('Username field empty')
        }
    
        if (password.value === '' || password.value === null){
            messages.push('Password field empty')
        }

        if (confirmpassword.value === '' || confirmpassword.value === null){
            messages.push('Confirm password field empty')
        }
        
        if (messages.length > 0){
            e.preventDefault()
            errorElement.innerText = messages.join(', ')
        }
    })
}
