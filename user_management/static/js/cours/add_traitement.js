var current_fs, next_fs, previous_fs; 
var left, opacity, scale; 
var animating;
var selectedValue="";

var traitement_name="";
var image_name="";
var image_path="";
var text_label="";

var next_error=""

// var qr_name="";
// var qr_path="";

$("input[type='radio'][name='type_traitement']").change(function() {
    selectedValue = $("input[type='radio'][name='type_traitement']:checked").val();
    // alert( "Handler for .change() called." + selectedValue );
});

$("textarea[name='label_traitement']").change(function() {
    text_label = $("textarea[name='label_traitement']").val()
})

// $("textarea[name='label_traitement']").change(function() {
//     text_label = $(this).find("textarea[name='label_traitement']").text()
// })

$("input[type='text'][name='name_image']").change(function() {
    image_name = $("input[type='text'][name='name_image']").val()
})

$("input[type='text'][name='titre_traitement']").change(function() {
    traitement_name = $("input[type='text'][name='titre_traitement']").val()
})

$("#id_path_image").change(function() {
    image_path = $("input[type='file']").val()
    console.log(image_path)
})

// $("#id_path_image")[0].change(function() {
//     image_path = $("input[type='file']:nth-child(1)")
//     console.log(image_path)
// })

// $("#id_path_image")[1].change(function() {
//     image_path = $("input[type='file']:nth-child(1)").val()
//     console.log(image_path)
// })

$(".next-to-2").click(function(){

    if(traitement_name != "" && selectedValue != "") {

        next_error=$("#next-error")
        if (next_error!="") {
            $("#next-error").remove()
            next_error=""
        }

        if(animating) return false;
        animating = true;

        current_fs = $(this).parent();

        // alert(traitement_name);
    
        switch (selectedValue) {
            case "Image":
                next_fs = $("#fs-image")
                break;
            case "QR-Code":
                next_fs = $("#fs-qr")
                // next_fs = $("#fs-qrcode")
                break;
            case "Texte":
                next_fs = $("#fs-texte")
                break;
            default:
                next_fs = $("#fs-image")
                break;
        }
        $("#li-second").addClass("active");
        next_fs.show(); 
        current_fs.animate({opacity: 0}, {
            step: function(now, mx) {
                scale = 1 - (1 - now) * 0.2;
                left = (now * 50)+"%";
                opacity = 1 - now;
                current_fs.css({
                    'transform': 'scale('+scale+')',
                    'position': 'absolute'
                });
                next_fs.css({'left': left, 'opacity': opacity});
            }, 
            duration: 800, 
            complete: function(){
                current_fs.hide();
                animating = false;
            }, 
            easing: 'easeInOutBack'
        });
    }
    else {
        next_error=$("#next-error")
        if (next_error!="") {
            $("#next-error").remove()
            next_error=""
        }
        $('<div class="alert alert-danger" id="next-error" role="alert">Vous devez remplir tous les champs avant de pouvoir continuer</div>').insertBefore( "#row-content" );
    }
});

$(".previous-to-1").click(function(){
    if(animating) return false;
    animating = true;
    current_fs = $(this).parent();
    previous_fs = $("#fs-1");
    $("#li-second").removeClass("active");
    previous_fs.show();
    current_fs.animate({opacity: 0}, {
        step: function(now, mx) {
            scale = 0.8 + (1 - now) * 0.2;
            left = ((1-now) * 50)+"%";
            opacity = 1 - now;
            current_fs.css({'left': left});
            previous_fs.css({'transform': 'scale('+scale+')', 'opacity': opacity});
        }, 
        duration: 800, 
        complete: function(){
            current_fs.hide();
            animating = false;
        },
        easing: 'easeInOutBack'
    });
});


// var next_to_3 = function(){

//     if(animating) return false;
//     animating = true;
    
//     current_fs = $(this).parent();
//     next_fs = $("#fs-3");
//     $("#li-third").addClass("active");
//     next_fs.show();
//     current_fs.animate({opacity: 0}, {
//         step: function(now, mx) {
//             scale = 1 - (1 - now) * 0.2;
//             left = (now * 50)+"%";
//             opacity = 1 - now;
//             current_fs.css({
//                 'transform': 'scale('+scale+')',
//                 'position': 'absolute'
//             });
//             next_fs.css({'left': left, 'opacity': opacity});
//         }, 
//         duration: 800, 
//         complete: function(){
//             current_fs.hide();
//             animating = false;
//         },
//         easing: 'easeInOutBack'
//     });
// }


$(".next-to-3").click(function(){
    
    switch (selectedValue) {
        case "Image":
            // alert(image_name);
            if(image_name != "" && image_path != "") {

                next_error=$("#next-error")
                if (next_error!="") {
                    $("#next-error").remove()
                    next_error=""
                }

                // alert(image_path);
                if(animating) return false;
                animating = true;
                
                current_fs = $(this).parent();
                next_fs = $("#fs-3");
                $("#li-third").addClass("active");
                next_fs.show();
                current_fs.animate({opacity: 0}, {
                    step: function(now, mx) {
                        scale = 1 - (1 - now) * 0.2;
                        left = (now * 50)+"%";
                        opacity = 1 - now;
                        current_fs.css({
                            'transform': 'scale('+scale+')',
                            'position': 'absolute'
                        });
                        next_fs.css({'left': left, 'opacity': opacity});
                    }, 
                    duration: 800, 
                    complete: function(){
                        current_fs.hide();
                        animating = false;
                    },
                    easing: 'easeInOutBack'
                });
            }
            else {
                next_error=$("#next-error")
                if (next_error!="") {
                    $("#next-error").remove()
                    next_error=""
                }
                $('<div class="alert alert-danger" id="next-error" role="alert">Vous devez remplir tous les champs de la section Image avant de pouvoir continuer</div>').insertBefore( "#row-content" );
            }
            break;
        case "QR-Code":
            // if(
            //     // image_name != "" && 
            // image_path != "") {

                next_error=$("#next-error")
                if (next_error!="") {
                    $("#next-error").remove()
                    next_error=""
                }
                
                // alert(image_name);
                if(animating) return false;
                animating = true;
                
                current_fs = $(this).parent();
                next_fs = $("#fs-3");
                $("#li-third").addClass("active");
                next_fs.show();
                current_fs.animate({opacity: 0}, {
                    step: function(now, mx) {
                        scale = 1 - (1 - now) * 0.2;
                        left = (now * 50)+"%";
                        opacity = 1 - now;
                        current_fs.css({
                            'transform': 'scale('+scale+')',
                            'position': 'absolute'
                        });
                        next_fs.css({'left': left, 'opacity': opacity});
                    }, 
                    duration: 800, 
                    complete: function(){
                        current_fs.hide();
                        animating = false;
                    },
                    easing: 'easeInOutBack'
                });
            // }
            // else {
            //     next_error=$("#next-error")
            //     if (next_error!="") {
            //         $("#next-error").remove()
            //         next_error=""
            //     }
            //     $('<div class="alert alert-danger" id="next-error" role="alert">Vous devez remplir tous les champs de la section code QR avant de pouvoir continuer</div>').insertBefore( "#row-content" );
            // }
            break;
        case "Texte":
            // alert(text_label);
            if(text_label != "") {

                next_error=$("#next-error")
                if (next_error!="") {
                    $("#next-error").remove()
                    next_error=""
                }
                
                // alert(text_label);
                if(animating) return false;
                animating = true;
                
                current_fs = $(this).parent();
                next_fs = $("#fs-3");
                $("#li-third").addClass("active");
                next_fs.show();
                current_fs.animate({opacity: 0}, {
                    step: function(now, mx) {
                        scale = 1 - (1 - now) * 0.2;
                        left = (now * 50)+"%";
                        opacity = 1 - now;
                        current_fs.css({
                            'transform': 'scale('+scale+')',
                            'position': 'absolute'
                        });
                        next_fs.css({'left': left, 'opacity': opacity});
                    }, 
                    duration: 800, 
                    complete: function(){
                        current_fs.hide();
                        animating = false;
                    },
                    easing: 'easeInOutBack'
                });
            }
            else {
                next_error=$("#next-error")
                if (next_error!="") {
                    $("#next-error").remove()
                    next_error=""
                }
                $('<div class="alert alert-danger" id="next-error" role="alert">Vous devez remplir tous les champs de la secrion Texte avant de pouvoir continuer</div>').insertBefore( "#row-content" );
            }
            break;
        default:
            
            break;
    }

    // if(animating) return false;
    // animating = true;
    
    // current_fs = $(this).parent();
    // next_fs = $("#fs-3");
    // $("#li-third").addClass("active");
    // next_fs.show();
    // current_fs.animate({opacity: 0}, {
    //     step: function(now, mx) {
    //         scale = 1 - (1 - now) * 0.2;
    //         left = (now * 50)+"%";
    //         opacity = 1 - now;
    //         current_fs.css({
    //             'transform': 'scale('+scale+')',
    //             'position': 'absolute'
    //         });
    //         next_fs.css({'left': left, 'opacity': opacity});
    //     }, 
    //     duration: 800, 
    //     complete: function(){
    //         current_fs.hide();
    //         animating = false;
    //     },
    //     easing: 'easeInOutBack'
    // });
});

$(".previous-to-2").click(function(){
    if(animating) return false;
    animating = true;
    current_fs = $(this).parent();
    switch (selectedValue) {
        case "Image":
            previous_fs = $("#fs-image")
            break;
        case "QR-Code":
            previous_fs = $("#fs-image")
            // previous_fs = $("#fs-qrcode")
            break;
        case "Texte":
            previous_fs = $("#fs-texte")
            break;
        default:
            previous_fs = $("#fs-image")
            break;
    }
    $("#li-third").removeClass("active");
    previous_fs.show();
    current_fs.animate({opacity: 0}, {
        step: function(now, mx) {
            scale = 0.8 + (1 - now) * 0.2;
            left = ((1-now) * 50)+"%";
            opacity = 1 - now;
            current_fs.css({'left': left});
            previous_fs.css({'transform': 'scale('+scale+')', 'opacity': opacity});
        }, 
        duration: 800, 
        complete: function(){
            current_fs.hide();
            animating = false;
        }, 
        easing: 'easeInOutBack'
    });
});

// $(".submit_traitement").click(function() {
//     alert( "Handler for .change() called." );
// })