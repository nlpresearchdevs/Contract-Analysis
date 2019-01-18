$(function () {
    $("[data-toggle=popover]").popover({
        html: true,
        content: function() {
            return $(this).next("#popover-content").html();
        }
    });
});

$(function () {
    $("[class='suggestions']").popover({
        html: true,
        content: function() {
            console.log('click');
            return $(this).next("#suggestions-popover-content").html();
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
    $('.filterPaneCheckBox').on('click', function(e) {
        var checkBoxId = $(this).attr('id');
        // get all contract text elements where categoryList and naturePartyList contains checkboxID
        var contractText = $('.click[data-categoryList*="' + checkBoxId + '"], .click[data-naturePartyList*="' + checkBoxId + '"]');
        var categoryArr = new Array();

        contractText.each(function() {
            var categoryList = $(this).attr('data-categoryList');
            categoryList = categoryList.replace(/[\[\]']+/g,'').split(",");
            categoryArr =  categoryArr.concat(categoryList);
            // console.log(categoryArr);
        });

        categorySet = [...new Set(categoryArr)];

        // var categoryArrayFlat = categoryList.join().split(",");
        // var categorySet = new Set(categoryArr);
        // console.log("categorySet: " + [...categorySet].join(' '));
        console.log(categorySet);
        console.log("includes: " + categorySet.includes('Assignments'));

        // var categoryArr = new Array();
        // var disableCheckBox = true;
        // for(var text in contractText){
        //     var categoryList = text.attr('data-categoryList');
             
        //     var categorySet = categoryList.join().split(",");
            
        //     if(!categorySet.includes(category)) {
        //         categoryArr.push(category);
        //     }
        // }

        //  = !(categoryArr.includes(checkBoxId));

        // console.log('checkBoxID is not in the list: ' + disableCheckBox);
        
        var checkBoxClass = $(this).attr('class');
        var otherCheckBoxes = '';

        var otherCategories = $('.categoryCheckBox').not(this).not('.click[data-categoryList*="' + categorySet + '"]');
        var otherNatures = $('.natureCheckBox').not(this);
        var otherParties = $('.partyCheckBox').not(this);

        if(~checkBoxClass.indexOf('categoryCheckBox')) {
            otherCheckBoxes = otherCategories
        } else if(~checkBoxClass.indexOf('natureCheckBox')) {
            otherCheckBoxes = otherNatures
        } else {
            otherCheckBoxes = otherParties
        }

        // console.log('otherCheckBoxes: ' + otherCheckBoxes.data());
        // console.log('checkBoxClass: ' + checkBoxClass);

        // this = selected checkbox
        if ($(this).is(':checked')) {
            contractText.first($(this).focus());
            contractText.each(function(){
                // this = current contractText
                $(this).css({"background": "#9ad7ff"});
                $(this).popover({
                    html: true,
                    content: function() {
                        return $(this).next("#popover-content").html();
                    }
                });
            });

            otherCheckBoxes.each(function(){
                // this = all except selected checkbox
                if($(this).is(':checked')) {
                    $(this).prop('checked', false);
                } 
                $(this).prop('disabled', true);
                
            });
            
        } else {
            otherCheckBoxes.each(function(){
                // this = all except selected checkbox
                if($(this).is(':disabled')) {
                    $(this).prop('disabled', false);
                } 
            });
            contractText.each(function(){
                // this = current contractText
                $(this).css({"background": ""});
            })
        }


    });
});
