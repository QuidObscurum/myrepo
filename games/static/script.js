jQuery("document").ready(function(){
    jQuery("#like").on('click', function(){
        console.log("hello");
            var href = document.getElementById('like').name;
            jQuery.ajax({
                type: "GET",

                url: "/games/addliketovideo/ajax/",

                data:{ "addlike" : href,},

                dataType: "text",

                catch: false,

                success: function(data){

                    jQuery("#count_likes").html(data);

                }
            });
    });
});