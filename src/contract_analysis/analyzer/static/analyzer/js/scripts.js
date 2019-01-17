$(function () {
    $("[data-toggle=popover]").popover({
        html: true,
        content: function() {
            return $(this).next("#popover-content").html();
        }
    });
});

$(document).on('click', function (e) {
    $('[data-toggle="popover"]').each(function () {
        //the 'is' for buttons that trigger popups
        //the 'has' for icons within a button that triggers a popup
        if (!$(this).is(e.target) && $(this).has(e.target).length === 0 && $('.popover').has(e.target).length === 0) {                
            (($(this).popover('hide').data('bs.popover')||{}).inState||{}).click = false  // fix for BS 3.3.6
        }

    });
});

window.onload = function() {
    if (window.jQuery) {  
        // jQuery is loaded  
        console.log("jQuery is loaded");
    } else {
        // jQuery is not loaded
        console.log("jQuery is not loaded");
    }
};

$(function () {
    $('input[type=checkbox]').on('click', function(e) {
        var checkBoxId = $(this).attr('id');
        var categoryText = $('.click[data-categoryList*="' + checkBoxId + '"], .click[data-naturePartyList*="' + checkBoxId + '"]');
        if(categoryText.length) {
            if ($(this).is(':checked')) {
                // console.log('has ' + checkBoxId );
                // console.log(categoryText.data());
                categoryText.first($(this).focus());
                categoryText.each(function(){
                    // $(this).addClass("focus");
                    // $(this).focus();
                    $(this).css({"background": "#9ad7ff"});
                    // console.log(this);
                    $(this).popover({
                        html: true,
                        content: function() {
                            return $(this).next("#popover-content").html();
                        }
                    });
                })
            }
            else {
                categoryText.each(function(){
                    $(this).css({"background": ""});
                })
            }
        } else {
            console.log( 'Does not have ' + checkBoxId );
            // console.log(categoryText.data());
        }     
        
    });
});
