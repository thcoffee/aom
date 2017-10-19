

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
//获取默认路径
/*
function getdefautlpath(){
        $.post("/aom/postData/",{'page':'installjdkadd',
                                 'type':'defautlpath',        
                                 'softversion':$("#softversion").val()},function(result){
             //alert(b);
             $("#remotepath").prop("value",result.result.defaultpath);
        });
    }
*/



//是否自定义文本框
function check2input($check,$input){
    if($check.prop("checked")){
        $input.prop("readOnly",false);               
        }    
    else{
        $input.prop("readOnly",true);  
        }     
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
