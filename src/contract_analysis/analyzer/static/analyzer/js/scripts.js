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
    // $('.click[data-categoryList~=]').bind('focus', function(){
    //     $(this).toggleClass('click');
    // });
    
    // $('input[type=checkbox]').each(function() {
    //     console.log($(this).attr('id'));
    // });

    $('input[type=checkbox]').on('click', function(e) {
        if ($('input[type=checkbox]').is(':checked')) {
            var checkBoxId = $(this).attr('id');
            // $('a[class="click"').focus()
            // var dataArray = this.attr()
                // console.log($(this).attr('id'));
                // console.log(checkBoxId);
            console.log($('a[class="click"').attr('style'))
        }
        // console.log($(this).attr('id'));
        // e.preventDefault();
    });
});

