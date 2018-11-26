jQuery("document").ready(function(){
    jQuery(".likecomm").on('click', function(){
        console.log("hello");
            var id = $(this).attr('id');
            //var id = $(this).getAttribute("id").value;
            jQuery.ajax({
                type: "GET",

                url: "/games/addliketocomment/ajax/",

                data:{ "addlike" : id,},

                dataType: "text",

                catch: false,

                success: function(data){

                    jQuery("#" + id + 'count').html(data);

                }
            });
    });
});
