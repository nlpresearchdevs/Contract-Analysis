$( document ).ready(function() {
    
    // shows category and nature-party popover
    $(function () {
        $(".click[data-toggle=popover]").popover({
            html: true,
            content: function() {
                return $(this).next("#popover-content").html();
            }
        });
    });


    // on click suggestions pane close button, hide suggestions pane
    $("#suggestionsPaneCloseBtn").click(function () {
        $("#suggestions-popover-content").toggleClass('hide');
    });


    // on click category close button, remove category from suggestions pane
    $('body').on('click', '#categoryBtnClose', function() {
        console.log($(this).parent());
        $(this).parent().remove();
    });


    // on click nature-party close button, remove nature-party from suggestions pane
    $('body').on('click', '#naturePartyBtnClose', function() {
        console.log($(this).parent());
        $(this).parent().remove();
    });


    // on click selection from list of category suggestions, 
    // add category as a closable button into suggestions pane
    // $('body').on('click', '#categoryLabelOpt', function() {
        $('#categorySuggestions').change(function() {
        console.log("add categoryLabel");
        $("<p class='categoryBtn'>" + $(this).next().attr("data-categoryLabel") + "<button type='button' id='categoryBtnClose' class='close' aria-label='Close'><span aria-hidden='true' style='font-size: 100%' >&times;</span></button></p>").insertAfter("#categoryLabel");
    });
    

    // on click nature-party from list of nature-party suggestions, 
    // add nature-party as a closable button into suggestions pane
    // $('body').on('click', '#naturePartyLabelOpt', function() {
        $('#naturePartySuggestions').change(function() {
        console.log("add naturePartyLabel");
        $("<p class='naturePartyBtn'>" + $(this).next().attr("data-naturePartyLabel") + "<button type='button' id='naturePartyBtnClose' class='close' aria-label='Close'><span aria-hidden='true' style='font-size: 100%' >&times;</span></button></p>").insertAfter("#naturePartyLabel");
    });

    // // on click button, remove category
    // $("#categoryBtnClose").click(function () {
    //     // console.log("remove: " + categoryBtnClose);
    //     // $(this).remove();
    //     console.log($(this).parent());
    // });

    // // on click button, remove natureParty
    // $("#naturePartyBtnClose").click(function () {
    //     // console.log("remove: " + naturePartyBtnClose);
    //     // $(this).remove();
    //     console.log($(this).parent());
    // });

    // // shows suggestions popover
    // $(function () {
    //     $(".suggestions[data-toggle=popover]").popover({
    //         html: true,
    //         content: function() {
    //             console.log('click');
    //             return $(this).next("#suggestions-popover-content").html();
    //         }
    //     });
    // });
    

    // on click page body, close popover
    $(document).on("click", function (e) {
        $("[data-toggle='popover']").each(function () {
            //the 'is' for buttons that trigger popups
            //the 'has' for icons within a button that triggers a popup
            if (!$(this).is(e.target) && $(this).has(e.target).length === 0 && $(".popover").has(e.target).length === 0) {                
                (($(this).popover("hide").data("bs.popover")||{}).inState||{}).click = false  // fix for BS 3.3.6
            }
        });
    });


    // on click suggestions anchor, show suggestions pane
    $(document).on("click", ".suggestions", function (e) {
        // $(".suggestions").on("click", function(e) {
            // console.log("prev: " + $(this).prev().html());
            // console.log("prevprev: " + $(this).prev().prev().html());

            // console.log("prevDataAttr: " + $(this).prev().data('text'));
            // console.log("prevprevDataAttr: " + $(this).prev().prev().data('text'));
            if($(".suggestions-popover-content").is(':hidden')) {
                $(".suggestions-popover-content").toggleClass('hide');
                // var popOverVisible = $(".hide");
                // if (popOverVisible) {
                //     // popover is visible
                //     popOverVisible.prev().popover("hide");
                //     // console.log("IN: " + popOverVisible.attr("visible"));
                // }
                // console.log("OUT: " + popOverVisible);  
            }

            if($('.categoryBtn').length) {
                $('.categoryBtn').remove();
            }
            if($('.naturePartyBtn').length) {
                $('.naturePartyBtn').remove();
            }

            // prev = Category
            // prev of prev = Nature-Party
            var prev = $(this).prev();
            var prevPrev = $(this).prev().prev();
            
            console.log("prevDataAttr: " + prev.attr('data-categoryList'));
            console.log("prevprevDataAttr: " + prevPrev.attr('data-naturePartyList'));
            console.log("arr: " + prevPrev.attr('data-naturePartyList').split(","));
            
            var categoryArr = prev.attr('data-categoryList').split(",");
            var naturePartyArr = prevPrev.attr('data-naturePartyList').split(",");

            for(var category of categoryArr) {
                category = category.replace("'", "");
                category = category.replace("'", "");
                category = category.replace("[", "");
                category = category.replace("]", "");
                
                $("<p class='categoryBtn'>" + category + "<button type='button' id='categoryBtnClose' class='close' aria-label='Close'><span aria-hidden='true' style='font-size: 100%' >&times;</span></button></p>").insertAfter("#categoryLabel");
            }

            for(var natureParty of naturePartyArr) {
                // natureParty = natureParty.replace(/[\|&;\$%@"<>\(\)\+,]/g, "");
                natureParty = natureParty.replace("'", "");
                natureParty = natureParty.replace("'", "");
                natureParty = natureParty.replace("[", "");
                natureParty = natureParty.replace("]", "");
                // console.log("np: " + natureParty);
                $("<p class='naturePartyBtn'>" + natureParty + "<button type='button' id='naturePartyBtnClose' class='close' aria-label='Close'><span aria-hidden='true' style='font-size: 100%' >&times;</span></button></p>").insertAfter("#naturePartyLabel");
            }
            
            // $("<p class='naturePartyBtn'>" + prevPrev.attr('data-naturePartyList') + "</p>").insertAfter("#naturePartyLabel");

            var popOverVisible = $(".hide");
            if (popOverVisible) {
                // popover is visible
                popOverVisible.prev().popover("hide");
                // console.log("IN: " + popOverVisible.attr("visible"));
            }
        // });
    });    


    // on load, check if jquery is loaded
    window.onload = function() {
        if (window.jQuery) {  
            // jQuery is loaded  
            console.log("jQuery is loaded");
        } else {
            // jQuery is not loaded
            console.log("jQuery is not loaded");
        }
    };

    // $(function () {
    //     $(".suggestions").on("click", function(e) {
    //         e.preventDefault();
    //         alert("Hey it's working");
    //         console.log("hide");
    //         //  $(".suggestions-popover-content").css('display', 'block');
    //         if($(".suggestions-popover-content").is(":hidden")) {
    //             $(".suggestions-popover-content").css("visibility", "visible");
    //         } else {
    //             $(".suggestions-popover-content").css("visibility", "hidden");
    //         }
    //     });
    // });
    

    // on click filter pane checkbox, highlight category and/or nature party
    $(function () {
        $(".filterPaneCheckBox").on("click", function(e) {
            var $lis = $(".click"),
                $checked = $("input:checked");	
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
                // $('.click').filter(selector).show();	
                $lis.css({"background": ""});                      
                $('.click').filter(selector).css({"background": "#9ad7ff"});			   
            }
            else
            {
                // $lis.show();
                $lis.css({"background": ""});
            }
        });
    });
});
