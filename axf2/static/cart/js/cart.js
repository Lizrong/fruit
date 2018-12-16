$(function(){
    $(".ischose").click(function(){
        var $outer_span=$(this);
        var cartid=$outer_span.parents("li.menuList").attr("cartid");
        $.getJSON("/changeselect/",{"cartid":cartid},function(data){
            if(data["selected"]){
                $outer_span.children("span").html("√");
                $outer_span.attr("is_select","true")
            }else{
                $outer_span.children("span").html("");
                $outer_span.attr("is_select","false")
            }
        })

    })
    $("#selectall").click(function(){
        var select_array=[];
        var not_select_array=[];
        $(".ischose").each(function(){
            if($(this).attr("is_select").toLowerCase()=="true"){
                select_array.push($(this).parents("li.menuList").attr("cartid"));
            }if($(this).attr("is_select").toLowerCase()=="false"){
                not_select_array.push($(this).parents("li.menuList").attr("cartid"));
            }
        });
        if(not_select_array.length!=0){
            var notselects=not_select_array.join("#");
            $.getJSON("/changeallselect/",{"notselects":notselects},function(data){
                if(data["status"]=="200"){
                    $(".ischose").each(function(){
                        if($(".ischose").attr("is_select")=="false"){
                            $(this).children("span").html("√")
                        }
                    });
                    $("#selectall").children("span").html("√")

                }
            })
        }
    })



})











//
//     var ok = document.getElementById("ok")
//     ok.addEventListener("click", function(){
//         var f = confirm("是否确认下单？")
//         if (f){
//             $.post("/saveorder/", function(data){
//                 if (data.status = "success"){
//                     window.location.href = "http://127.0.0.1:8001/cart/"
//                 }
//             })
//         }
//     },false)
// })