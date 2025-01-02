$(document).ready(function() {
    (function($) {
        "use strict";

        // Validate the contactForm
        $(function() {
            $('#contactForm').validate({
                rules: {
                    name: {
                        required: true,
                        minlength: 2
                    },
                    subject: {
                        required: true,
                        minlength: 4
                    },
                    number: {
                        required: true,
                        minlength: 5
                    },
                    email: {
                        required: true,
                        email: true
                    },
                    message: {
                        required: true,
                        minlength: 20
                    },
                    mobile: {
                        required: true,
                        minlength: 10,  // Adjust according to your requirements
                        maxlength: 15,  // Match max_length in your model
                        digits: true,    // Ensure only digits are entered
                    },
                },
                messages: {
                    name: {
                        required: "Come on, you have a name, don't you?",
                        minlength: "Your name must consist of at least 2 characters"
                    },
                    subject: {
                        required: "Come on, you have a subject, don't you?",
                        minlength: "Your subject must consist of at least 4 characters"
                    },
                    number: {
                        required: "Come on, you have a number, don't you?",
                        minlength: "Your number must consist of at least 5 characters"
                    },
                    email: {
                        required: "No email, no message"
                    },
                    message: {
                        required: "Um... yea, you have to write something to send this form.",
                        minlength: "That's all? Really?"
                    },
                    mobile: {
                        required: "Please enter your mobile number.",
                        minlength: "Mobile number must be at least 10 digits.",
                        maxlength: "Mobile number must be at most 15 digits.",
                        digits: "Please enter a valid mobile number." 
                    }
                },
                submitHandler: function(form) {
                    // Perform AJAX submission
                    $.ajax({
                        type: "POST",
                        url: form.action, // The form action URL
                        data: $(form).serialize(), // Serialize form data
                        headers: {
                            'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val() // Include CSRF token
                        },
                        success: function(response) {
                            // Clear previous messages
                            $('.messages').html('');
                            // Display the message based on the response
                            if (response.status === 'success') {
                                $('.messages').append('<div class="alert alert-success">' + response.message + '</div>');
                                // Optionally reset the form fields
                                $('#contactForm')[0].reset();
                            } else if (response.status === 'error') {
                                $('.messages').append('<div class="alert alert-danger">' + response.message + '</div>');
                            }
                            // Scroll to the messages section
                            $('html, body').animate({
                                scrollTop: $('.messages').offset().top - 100
                            }, 1000);
                        },
                        error: function(xhr, status, error) {
                            // Handle server errors
                            $('.messages').html('<div class="alert alert-danger">An unexpected error occurred. Please try again later.</div>');
                            // Scroll to the messages section
                            $('html, body').animate({
                                scrollTop: $('.messages').offset().top - 100
                            }, 1000);
                        }
                    });
                }
            });
        });

    })(jQuery);
});
