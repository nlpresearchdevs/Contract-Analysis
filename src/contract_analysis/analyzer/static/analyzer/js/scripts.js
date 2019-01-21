// shows category and nature-party popover
$(function () {
    $("[data-toggle=popover]").popover({
        html: true,
        content: function() {
            return $(this).next("#popover-content").html();
        }
    });
});

// shows suggestions popover
$(function () {
    $("[class='suggestions']").popover({
        html: true,
        content: function() {
            console.log('click');
            return $(this).next("#suggestions-popover-content").html();
        }
    });
});

// closes popover upon clicking page body
$(document).on('click', function (e) {
    $('[data-toggle="popover"]').each(function () {
        //the 'is' for buttons that trigger popups
        //the 'has' for icons within a button that triggers a popup
        if (!$(this).is(e.target) && $(this).has(e.target).length === 0 && $('.popover').has(e.target).length === 0) {                
            (($(this).popover('hide').data('bs.popover')||{}).inState||{}).click = false  // fix for BS 3.3.6
        }
    });
});

// checks if jquery loaded
window.onload = function() {
    if (window.jQuery) {  
        // jQuery is loaded  
        console.log("jQuery is loaded");
    } else {
        // jQuery is not loaded
        console.log("jQuery is not loaded");
    }
};

// highlights text element based on category and nature-party
$(function () {
    $('.filterPaneCheckBox').on('click', function(e) {
        var $lis = $('.click'),
            $checked = $('input:checked');	
        if ($checked.length)
        {							
            var selector = '';
            $($checked).each(function(index, element){
                var elementClass = $(this).attr('class');
                // console.log('element: ' + $(this).attr('class'));                     

                if(elementClass.includes("categoryCheckBox")) {
                    selector += "[data-categoryList*='" + element.id + "']";                            
                }
                else if(elementClass.includes("natureCheckBox") || elementClass.includes("partyCheckBox")) {
                    selector += "[data-naturePartyList*='" + element.id + "']";
                }
                // console.log('element: ' + $(this).attr('class'));                     
                // selector += "[data-categoryList*='" + element.id + "']";                            
            });
            // $lis.hide();  
            $lis.css({"background": ""});                      
            // $('.click').filter(selector).show();	
            $('.click').filter(selector).css({"background": "#9ad7ff"});			   
        }
        else
        {
            // $lis.show();
            $lis.css({"background": ""});
        }
    });
});
