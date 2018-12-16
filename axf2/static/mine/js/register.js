$(document).ready(function(){
    var accunt = document.getElementById("accunt");
    var tip = document.getElementById("tip");

    accunt.addEventListener("blur", function(){
        inputstr = this.value;
        $.get("/checkusername/", {"username":inputstr}, function(data){
            tip.style.color = data["color"];
            tip.innerHTML = data["msg"];

            if (data.status == "fail"){
                $("[type='submit']").prop("disabled",true); // 禁用提交按钮
            }else{
                $("[type='submit']").prop("disabled",false); // 解禁提交按钮
            }
        })
    })

    var pass=document.getElementById("pass");
    var tip2= document.getElementById("tip2");
    pass.addEventListener("blur",function(){
        inputpass=this.value;
        if (inputpass.length < 6 ){
            tip2.style.color="red"
            tip2.innerHTML="密码不符合规范"
        }else{
            tip2.style.color="green"
            tip2.innerHTML="ok"
        }
    })

})