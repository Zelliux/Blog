
// error pop-up event
$(document).ready(function() {

    if (error) {

        if (modal === 'sign-in') {
            open_sign_in_modal()
        }

        if (modal === 'sign-up') {
            open_sign_up_modal()
        }

    // show error message
    error_pop_up(2000, error_message)
    show_overlay()

    // redirect if not-found error (404)
    setTimeout(() => {
        if (modal==='') {
            hide_overlay()
        }
        if (error==='not-found' | error==='redirect') {
            window.location.replace("/");
        }
    }, 2000);
}


    $('.modal-form-sign-up').on('submit', function(event){

        // get total password length
        let len_password = $('#sign-up-password').val().length
        
        if (len_password<6) {
            
            //creating fade effect
            event.preventDefault();
            error_pop_up(2000)
        }
        
        
    
        let len_name = $('#sign-up-name').val().length
        let len_email = $('#sign-up-email').val().length

        if (len_name>500 || len_email>500) {

            //creating fade effect
            event.preventDefault();
            error_pop_up(2000, 'Too large name or email')
        }
    });
});

function error_pop_up(time, text) {
    let error = $('.error-pop-up')
    $('.pop-up-text').text(text)

    error.removeClass('d-none')
    error.removeClass('fade-out')
    error.addClass('fade-in')
    
    // timeout to match the animation
    setTimeout(() => {
        error.removeClass('fade-in')
        error.addClass('fade-out')
    }, time);
    
    setTimeout(() => {
        error.addClass('d-none')
    }, time+220);
}
    
    

function show_overlay() {
    // show overlay
    $('.page-overlay').removeClass('d-none')
    $('.page-overlay').removeClass('fade-out')
    $('.page-overlay').addClass('fade-in')
}

function hide_overlay() {
    // hide overlay
    $('.page-overlay').removeClass('fade-in')
    $('.page-overlay').addClass('fade-out')
    setTimeout(() => {
        $('.page-overlay').addClass('d-none')
    }, 210);
}

function close_modal() {
    // hide modals
    $('.modal-form-sign-up, .modal-form-sign-in').addClass('hide-form')
    $('.modal-form-sign-up, .modal-form-sign-in').removeClass('show-form')
    hide_overlay()

    // redirect if sign-in or create
    let url = (window.location.href);
    let is_sign_in = url.substr(url.lastIndexOf('/') + 1).replace('#', '');
    if (is_sign_in==='sign-in' | is_sign_in==='create') {
        window.location.replace("/");
    }
}

// on press ESC exit the modal
$(document).on( 
    'keydown', function(event) { 
        if (event.key == "Escape") { 
            if ($('.modal-form').hasClass('show-form')) {
                close_modal()
            }
        } 
    }); 

$('.close-modal-form').click(function(){
    close_modal()
});


function open_sign_up_modal() {
    // hide other modal
    $('.modal-form-sign-in').addClass('hide-form')
    $('.modal-form-sign-in').removeClass('show-form')
    $('.modal-form-sign-in').addClass('d-none')

    // show correct modal
    $('.modal-form-sign-up').removeClass('d-none')
    $('.modal-form-sign-up').removeClass('hide-form')
    $('.modal-form-sign-up').addClass('show-form')
    
    show_overlay()
}

function open_sign_in_modal() {
    // hide other modal
    $('.modal-form-sign-up').addClass('hide-form')
    $('.modal-form-sign-up').removeClass('show-form')
    $('.modal-form-sign-up').addClass('d-none')

    // show correct modal
    $('.modal-form-sign-in').removeClass('d-none')
    $('.modal-form-sign-in').removeClass('hide-form')
    $('.modal-form-sign-in').addClass('show-form')
    
    show_overlay()
}


$('.pop-sign-up-modal').click(function(){
    open_sign_up_modal()
});

$('.pop-sign-in-modal').click(function(){
    open_sign_in_modal()
});



// password view toggle

function toggle_password(target) {

    $('.show-password-btn').click(function(){
        var password = document.getElementById(target);
        
        // get current password class
        var $this = $(this) 
        var this_class = $this.attr("class");

        // change input type to show the text
        if (password.type === 'password') {
            password.type = 'text'
            $('.'+this_class).text('Hide')

        } 
        
        else {
            password.type = 'password'
            $('.'+this_class).text('Show')
        }
    });
}

toggle_password("sign-up-password")
toggle_password("sign-in-password")