function verify() {
    checkpass = document.getElementById('pass').value;
    split = 4;
    if (checkpass.substring(0, split * 2) == 'picoCTF{') {                                          
        if (checkpass.substring(7, 9) == '{n') {                                                    
            if (checkpass.substring(split * 2, split * 2 * 2) == 'not_this') {                      
                if (checkpass.substring(3, 6) == 'oCT') {
                    if (checkpass.substring(split * 3 * 2, split * 4 * 2) == '55670}') {
                        if (checkpass.substring(6, 11) == 'F{not') {
                            if (checkpass.substring(split * 2 * 2, split * 3 * 2) == '_again_0') {
                                if (checkpass.substring(12, 16) == 'this') {
                                    alert('Password Verified');
                                }
                            }
                        }
                    }
                }
            }
        }
    } else {
        alert('Incorrect password');
    }
}

// picoCTF{not_this_again_055670}