

//获取默认目录
/*
$(document).ready(function(){
    $("#remotepath").prop("readOnly",true);
});
*/
//select to select 
function select2select(x,y){
    if (x.value != ''){
        y.options[y.options.length]=new Option(x.value,x.text);
    x.options[x.selectedIndex]=null;}
}
//提交方法
function putdata(kwage){
    $.ajax({url:kwage.url,  
           data:kwage.data,
           dataType:"json",
           type:"POST",
           success:kwage.success,
           error:kwage.error,
           }
    );   
}
//清空select
function clearselect($s){
    $s.empty();
    //这么做是因为qq浏览器一类的，会有残留的图像
    $s.append("<option  value=0>-----</option>");
    $s.empty();
}
//初始化select信息
function initselect($s,table){  
    clearselect($s);
     //alert(table);
    for (var i=0; i<table.length; i++){
        var item = table[i];
          $s.append("<option  value=" + item[0] + ">" + item[1] + "</option>");
        }
}

//是否自定义文本框
function check2input($check,$input){
    if($check.prop("checked")){
        $input.prop("readOnly",false);               
        }    
    else{
        $input.prop("readOnly",true);  
        }     
}
//通用回调错误处理
function callbackerror(XMLHttpRequest, textStatus, errorThrown){
                 alert('访问网络失败！'+ errorThrown);
}
/*
$(document).ready(function(){
    $('#custom').click(function(){
        if($('input[name="custom"]').prop("checked")){
            $("#remotepath").prop("readOnly",false);               
            }    
        else{
            $("#remotepath").prop("readOnly",true);  
            }            
    });
})
*/
